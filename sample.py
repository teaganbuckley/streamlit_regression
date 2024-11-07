import streamlit as st
from camera_input_live import camera_input_live


st.write(" ## Overwatch")
f_character = st.text_input("Who is your favourite Overwatch character?")
st.write(f"Your favourite Overbitch character is: {f_character}")
st.button("Click Me Bitch")
color = st.color_picker("Pick Your Fave Overbitch Color")
st.write(f"Your favourite Overbitch color is: {color}")
st.radio("Pick Me", ["Meow", "Woof"])
bitch_mode = st.toggle("Active Bitch Mode")
if bitch_mode == True:
    st.write("Bitch Mode is Activated")
    st.balloons()

image = camera_input_live()

if image:
    st.image(image)
