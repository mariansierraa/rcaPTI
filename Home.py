import streamlit as st 
import yfinance as yf
import pandas as pd
import datetime
from plotly.subplots import make_subplots
import plotly.graph_objects as go

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)
st.title('Perfect Trend Indicator by RCA Capital')

st.markdown(
    """
    RCA Capital Strategies App.
    
    **👈 Select a strategy from the sidebar** to select the perfect assets

    ### Want to learn more?
    - Contact us: +573143172966
"""
)
