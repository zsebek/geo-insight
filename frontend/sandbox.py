import streamlit as st
import random

# Initialize session state variables if they do not exist
if "operand_slider_history" not in st.session_state:
    st.session_state.operand_slider_history = []
if "op1" not in st.session_state:
    st.session_state.op1 = 1  # Default slider value
if "op2" not in st.session_state:
    st.session_state.op2 = 1  # Default slider value

# Function to multiply operands
@st.cache_data
def multiply(op1: int, op2: int):
    return op1 * op2

# Function to update sliders with random values
def random_op_button():
    st.session_state.op1 = random.randint(1, 10)
    st.session_state.op2 = random.randint(1, 10)
    # Mark as changed so the history updates
    st.session_state.slider_changed = True  

# Button to trigger random operand changes
st.button("Random ops", on_click=random_op_button)

# Sliders directly tied to session state
op1 = st.slider("Operand 1", min_value=1, max_value=10, step=1, value=st.session_state.op1)
op2 = st.slider("Operand 2", min_value=1, max_value=10, step=1, value=st.session_state.op2)

# Detect manual slider movement
if op1 != st.session_state.op1 or op2 != st.session_state.op2:
    st.session_state.op1 = op1
    st.session_state.op2 = op2
    st.session_state.slider_changed = True  

# Append history only if values changed
if st.session_state.get("slider_changed", False):  
    result = multiply(st.session_state.op1, st.session_state.op2)
    st.session_state.operand_slider_history.append(result)
    st.session_state.slider_changed = False  # Reset flag

# Display the expanding line chart
st.line_chart(st.session_state.operand_slider_history)
