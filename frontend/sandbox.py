import streamlit as st
import random

st.title('Sliders and Charts')
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


st.title('Forms')
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
