import streamlit as st
from tabs.stock_tab import render_stocks_tab
from tabs.layout_tryout_tab import render_layout_tryout_tab


stocksTab, layoutTryoutTab = st.tabs(['Stocks', 'Layouts'])

with stocksTab:
    render_stocks_tab()

with layoutTryoutTab:
    render_layout_tryout_tab()
