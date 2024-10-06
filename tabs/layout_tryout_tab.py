import streamlit as st

def render_layout_tryout_tab():
    with st.container(border = True):
        col1, col2, col3 = st.columns(3)
        col1.button('Button 1')
        col2.button('Button 2')
        col3.button('Button 3')

    with st.container(border = True):
        col4, col5 = st.columns(2)
        col4.button('Button 4')
        col5.button('Button 5')