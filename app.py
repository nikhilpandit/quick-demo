import streamlit as st


def square(x):
    return x + x


def cube(x):
    return x * 3


st.write("# Hello, world!")
st.write("Testing some quick stuff")
st.write("## A simple box")
col1, col2 = st.columns([2, 1])  # Adjust the ratios as needed
with col1:
    number = st.number_input(
        "Enter a number", min_value=0, max_value=100, key="number_input",
        step=1, format="%d", label_visibility="visible", disabled=False
    )
if st.button("Click me"):
    st.write(f"You've clicked the button! Square of the number you entered is: {square(number)}")
    st.write(f"You've clicked the button! Cube of the number you entered is: {cube(number)}")
