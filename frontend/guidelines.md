# Caching and Hashing
Python pickle module is behind the scenes serializing stuff.
"pickle-serializable", we mean calling pickle.dumps(obj) should not raise a PicklingError exception.
By default, Streamlit’s Session State allows you to persist any Python object for the duration of the session, irrespective of the object’s pickle-serializability. 
To that end, Streamlit provides a runner.enforceSerializableSessionState configuration option that, when set to true, only allows pickle-serializable objects in Session State. To enable the option, either create a global or project config file with the following or use it as a command-line flag:
``` python
# .streamlit/config.toml
[runner]
enforceSerializableSessionState = true
```

## @st.cache_data
Do it for your dataframes, images, external api calls.

```python
@st.cache(ttl=3600)
def db_update():
    return ...

@st.cache()
def api_call():
    return ...
```

## @st.cache_resource
Do it for your database connections, huge queries (5M), nonserializable charts / plots, polar.LazyFrame, threads
```python
@st.cache_resource
def db_conn():
    return ...

@st.cache_resource
def nonserializable_interactive_map():
    return ...
```

## Hash to cache a func with custom class import
Streamlit doesn't know how to handle structured objects (classes) when they are the inputs or outputs of cached functions.
To use a custom class with a cached function, you need to handle the `UnhashableParamError`.

1️⃣ Caching a Method Inside a Class
✔ You CAN cache a method, but Streamlit needs to know how to hash self.
✔ Use hash_funcs={MyClass: lambda x: hash(x.id)} to make self hashable.
✔ Ensure that the method is pure (i.e., doesn’t modify self).
✔ Avoid caching methods that rely on changing instance state.

2️⃣ Caching a Function That Takes & Returns a Custom Class
✔ You MUST use hash_funcs to allow Streamlit to cache a function with a custom object.
✔ Define a separate hash function (hash_func) for clarity & reuse.
✔ Use st.cache_data when the function deals with immutable, structured data.
✔ Use st.cache_resource instead if caching expensive-to-create objects (e.g., database connections, ML models).

```python
import streamlit as st

# Define the class
class MyClass:
    def __init__(self, unique_thing: int):
        self.id = unique_thing

    @st.cache_data(hash_funcs={"__main__.MyClass": lambda x: hash(x.id)})
    def multiply_id(self, multiplier: int) -> int:
        return self.id * multiplier

    def increment_id(self, addition: int = 1) -> int:
        return self.id + addition  # Correctly increment and return new value

# Custom hash function for MyClass
def hash_func(obj: MyClass) -> int:
    return hash(obj.id)  # Unique hash based on id

# Cache the function with a custom hash function
@st.cache_data(hash_funcs={MyClass: hash_func})
def cache_custom_object_with_incremented_id(obj: MyClass) -> MyClass:
    new_id = obj.increment_id()  # Get the incremented ID
    return MyClass(new_id)  # Return new instance with updated ID

# Create instance
inst = MyClass(1)

# Call cached function
copy = cache_custom_object_with_incremented_id(inst)

# call cached multiply method
copy.multiply_id(3)
# Display output
st.write(f"Original ID: {inst.id}, Cached Copy ID: {copy.id}")
```


# State

A `session` is one browser tab running the app.
Only state variables survive the rerun, which is triggered on each code change and app interaction.

Persist state with session_state and manipulate state with callbacks.

📌 General Design Guide for Stateful Streamlit Apps

## 1️⃣ Let Components Manage Their Own State
✅ **Use `key` in widgets** to directly bind their state to `st.session_state`.  
- This prevents conflicts where session state updates manually override UI behavior.  
🚨 What to avoid?
- Manually reassigning st.session_state.op1 = op1 after a slider update.
- This may cause UI flickering or "snapping back" issues.

## 2️⃣ Use a Common Shared Variable to Gate Updates to a Controlled Component
✅ Introduce an update flag (e.g., slider_changed) to track when an update should be processed.
- This prevents uncontrolled, repeated updates from multiple components.

🚨 What to avoid?
- Directly updating history every time the script reruns (e.g., append() without conditions).
- This leads to excessive history entries and duplicates.

## 3️⃣ As More Components Share Management of a Controlled Component, Let Them Hook Into the Shared Variable
✅ Multiple components should reference a single state flag (slider_changed) to coordinate updates.
- This ensures manual changes and button-triggered changes are processed correctly.
🚨 What to avoid?
- Each component managing its own version of a "changed" state separately.
- This can lead to race conditions or unexpected updates.

## 4️⃣ Minimize Redundant Computations with Caching
✅ Use @st.cache_data for expensive operations like calculations or API calls.
- This avoids recalculating the same results unnecessarily.
🚨 Should you cache the operand slider history?
- No. st.session_state.operand_slider_history is a mutable list, and caching it may cause unexpected behavior:

- Session state is already persistent within the session.
- Cached objects cannot be modified in-place, which could break updates.
- However, you could use caching if:

- You perform an expensive transformation on the history (e.g., aggregating results).
- You expect very large histories that benefit from optimized retrieval.

## 5️⃣ Keep State Management Simple & Predictable
✅ Reset state explicitly when necessary.
🚨 What to avoid?
- Over-complicating state logic with too many flags or nested conditions.
- Updating unrelated session state variables in different parts of the script.

## Slider and Button Cahrt example
``` python
# Initialize session state variables if they do not exist
if "operand_slider_history" not in st.session_state:
    st.session_state.operand_slider_history = []
if "op1" not in st.session_state:
    st.session_state.op1 = 1  # Default slider value
if "op2" not in st.session_state:
    st.session_state.op2 = 1  # Default slider value
if "slider_changed" not in st.session_state:
    st.session_state.slider_changed = False  # Track state changes

# Function to multiply operands
@st.cache_data
def multiply(op1: int, op2: int):
    return op1 * op2

# Function to update sliders with random values
def random_op_button():
    st.session_state.op1 = random.randint(1, 10)
    st.session_state.op2 = random.randint(1, 10)
    st.session_state.slider_changed = False

# Button to trigger random operand changes
st.button("Random ops", on_click=random_op_button)

# ✅ Use `key` to let sliders manage their own state properly
st.slider("Operand 1", min_value=1, max_value=10, step=1, key="op1")
st.slider("Operand 2", min_value=1, max_value=10, step=1, key="op2")

# Detect changes manually (for history tracking)
if not st.session_state.slider_changed:  # Prevent double updates
    result = multiply(st.session_state.op1, st.session_state.op2)
    st.session_state.operand_slider_history.append(result)
    st.session_state.slider_changed = True  

# Reset flag after adding history
st.session_state.slider_changed = False

# Display the expanding line chart
st.line_chart(st.session_state.operand_slider_history)

```


# Forms
All widgets will trigger a script rerun whenever a user changes its value, unless the widget is part of a form.
Before a form is submitted, all widgets within that form will have default values, just like widgets outside of a form have default values.

```python
form = st.form('my_form')
submit = form.form_submit_button('submit and update')
if "form_text" not in st.session_state:
    st.session_state["form_text"] = "Default text"
sentence = form.text_input("This text is in there", key="form_text")
form.text(body=st.session_state["form_text"])  # should update after text-box enter or button press

if "nonform_text" not in st.session_state:
    st.session_state["nonform_text"] = "Default text"


non_form = st.text_input("this updates automatically", key="nonform_text")
st.text(body=st.session_state["nonform_text"])  # updates on clickaway
```

## Form callback handling

``` python
# Initialize session state for column count
if "col-count" not in st.session_state:
    st.session_state["col-count"] = 1

with st.form('column_form'):
    rows = st.number_input('Rows', value=1, min_value=1)
    cols = st.number_input('Columns', min_value=1, max_value=5, key="col-count")
    st.form_submit_button('update_cols')

# if not st.session_state["col-count-updated"]:    
columns = st.columns(st.session_state["col-count"])
for idx, col in enumerate(columns):
    col.write(f"**col {idx + 1}**")

```

### 1️⃣ Start Without Forms ✅
- Widgets (like st.number_input, st.slider) already manage their own state when using key.
- If updates should happen instantly as the user interacts, don't use a form.
### 2️⃣ Introduce Forms Only When Needed ✅
Forms should be used when:
- You want to update multiple widgets at once (e.g., a group of related inputs that should be committed together).
- Continuous updates are too slow (e.g., expensive calculations, API calls).
- User experience benefits from batching changes (e.g., selecting multiple filters before applying them).


# Fragments
The rerun context is contained to the fragment.
Don't define return values for your fragments.

There are fragment reruns and fullscript reruns. 
- Elements drawn to containers outside the main body of fragment will not be cleared with each fragment rerun. Instead, Streamlit will draw them additively and these elements will accumulate until the next full-script rerun.

## UI Fragment
```python
@st.fragment
def fragment_function():
    if st.button("Hi!"):
        st.write("Hi back!")

with st.sidebar:
    fragment_function()
```

## Streaming fragment
https://docs.streamlit.io/develop/tutorials/execution-flow/start-and-stop-fragment-auto-reruns
```python
@st.fragment(run_every="10s")
def auto_function():
		# This will update every 10 seconds!
		df = get_latest_updates()
		st.line_chart(df)

auto_function()
```

# Compare fragments to other Streamlit features
## Fragments vs forms
*  Forms allow users to interact with widgets without rerunning your app. Streamlit does not send user actions within a form to your app's Python backend until the form is submitted. Widgets within a form can not dynamically update other widgets (in or out of the form) in real-time.
* Fragments run independently from the rest of your code. As your users interact with fragment widgets, their actions are immediately processed by your app's Python backend and your fragment code is rerun. Widgets within a fragment can dynamically update other widgets within the same fragment in real-time.
* A form batches user input without interaction between any widgets. A fragment immediately processes user input but limits the scope of the rerun.

## Fragments vs callbacks
* Callbacks allow you to execute a function at the beginning of a script rerun. A callback is a single prefix to your script rerun.
* Fragments allow you to rerun a portion of your script. A fragment is a repeatable postfix to your script, running each time a user interacts with a fragment widget, or automatically in sequence when run_every is set.
* When callbacks render elements to your page, they are rendered before the rest of your page elements. When fragments render elements to your page, they are updated with each fragment rerun (unless they are written to containers outside of the fragment, in which case they accumulate there).

## Fragments vs custom components
* Components are custom frontend code that can interact with the Python code, native elements, and widgets in your Streamlit app. Custom components extend what’s possible with Streamlit. They follow the normal Streamlit execution flow.
* Fragments are parts of your app that can rerun independently of the full app. Fragments can be composed of multiple Streamlit elements, widgets, or any Python code.
* A fragment can include one or more custom components. A custom component could not easily include a fragment!

## Fragments vs caching
* Caching: allows you to skip over a function and return a previously computed value. When you use caching, you execute everything except the cached function (if you've already run it before).
* Fragments: allow you to freeze most of your app and just execute the fragment. When you use fragments, you execute only the fragment (when triggering a fragment rerun).
* Caching saves you from unnecessarily running a piece of your app while the rest runs. Fragments save you from running your full app when you only want to run one piece.

## Limitations and unsupported behavior
* Fragments can't detect a change in input values. It is best to use Session State for dynamic input and output for fragment functions.
* Using caching and fragments on the same function is unsupported.
* Fragments can't render widgets in externally-created containers; widgets can only be in the main body of a fragment.