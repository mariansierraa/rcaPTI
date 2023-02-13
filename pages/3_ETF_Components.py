import streamlit as st
import time
import numpy as np
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import datetime as dt
from datetime import timedelta as td
import datetime
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import requests
import re


st.set_page_config(page_title="ETF Components", page_icon="📈")

st.title("ETF Comp Strategy ")


st.sidebar.subheader('Date parameters')
start_date = st.sidebar.date_input("Start date", datetime.date(2022, 8, 4))
#end_date = st.sidebar.date_input("End date", datetime.date(2023, 2, 9))

#tickers data
ticker=st.text_input('ETF','DIA')
ticker=ticker.split(",")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0"
}

print(ticker)

allofit=pd.DataFrame()
malas=[]
def main(url,start):
    with requests.Session() as req:
        req.headers.update(headers)
        for key in ticker:
            r = req.get(url.format(key))
            print(f"Extracting: {r.url}")
            goal = re.findall(r'etf\\\/(.*?)\\', r.text)
            print(goal)
        for x in goal:
            try:
                data=yf.download(x,start)
                data=data['Close']
                allofit[x]=data
            except:
                malas.append(x)
                
            
main("https://www.zacks.com/funds/etf/{}/holding",start_date)

allofit_copy=allofit.mean(axis=1)   
datareturn=(allofit_copy/allofit_copy.shift())-1
data_mean=datareturn.rolling(10).mean()
data_desv=datareturn.rolling(10).std()
all_d=datareturn
all_mean=data_mean
all_desv=data_desv
all_desv=all_desv.dropna()
all_mean=all_mean.dropna()
sample_mean=all_mean*100
sample_desv=all_desv*100
sample_tot=(sample_mean/sample_desv)*100


st.header('**ETF Data**')

fig=make_subplots(rows=2, cols=1,subplot_titles=(ticker[0], "mean/desv", "Desv_10"))
fig.append_trace(go.Scatter(x=allofit_copy[10:].index,y=allofit_copy[10:]), row=1, col=1)
fig.append_trace(go.Scatter(x=sample_tot.index,y=sample_tot), row=2, col=1)
fig.add_hline(y=-20, line_width=3, line_dash="dash", line_color="green",row=2,col=1)
fig.add_hline(y=0, line_width=3, line_dash="dash", line_color="orange",row=2,col=1)
fig.add_hline(y=20, line_width=3, line_dash="dash", line_color="black",row=2,col=1)
fig.update_layout(height=900, width=1000, title_text="Stacked Subplots")
st.plotly_chart(fig, use_container_width=True)

datareturn_all=(allofit/allofit.shift())-1
data_mean_all=datareturn_all.rolling(10).mean()
data_desv_all=datareturn_all.rolling(10).std()
all_d_all=datareturn_all
all_mean_all=data_mean_all
all_desv_all=data_desv_all
all_desv_all=all_desv_all.dropna()
all_mean_all=all_mean_all.dropna()
sample_mean_all=all_mean_all*100
sample_desv_all=all_desv_all*100
sample_tot_all=(sample_mean_all/sample_desv_all)*100

finales=sample_tot_all.iloc[[-1]].T
finales.columns=['PT']
finales=finales.sort_values('PT',ascending=False)

st.write(finales)
st.sidebar.header("Swing Strategy")

progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()

progress_bar.empty()


# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")