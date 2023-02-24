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

st.set_page_config(page_title="Swing 90 min", page_icon="📈")

st.title("Swing 90 min Strategy ")

st.sidebar.subheader('Date parameters')
start_date = st.sidebar.date_input("Start date", datetime.date(2023, 1, 1))
#end_date = st.sidebar.date_input("End date", datetime.date(2023, 2, 9))

#tickers data
ticker=st.text_input('Ticker','ROKU,COIN')
ticker=ticker.split(",")

print(ticker)

def ninetyswing(item,startdate):
    all_d=pd.DataFrame()
    all_mean=pd.DataFrame()
    all_desv=pd.DataFrame()
    closeprice=pd.DataFrame()
    for i in item:
        data=yf.download(i,startdate,interval='90m')
        datacl=data['Close']
        #factor_E=datacl[77:78][0]/datacl[78:79][0]
        #datacl[78:]= (datacl[78:])*factor_E
        closeprice[i]=datacl
    
    datareturn=(closeprice/closeprice.shift())-1
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
    sample_tot.index=(sample_tot.index.strftime('%m/%d/%Y, %r'))
    closeprice.index=(closeprice.index.strftime('%m/%d/%Y, %r'))
    finales=sample_tot.iloc[[-1]].T
    finales.columns=['PT']
    finales=finales.sort_values('PT',ascending=False)
    return finales,closeprice,sample_tot


st.header('**Tickers Data**')
allof=ninetyswing(ticker,start_date)

st.write(allof[0])

for w in ticker:
    fig=make_subplots(rows=2, cols=1,subplot_titles=(w, "PTI"))
    fig.append_trace(go.Scatter(x=allof[1][w][9:].index,y=allof[1][w][9:]), row=2, col=1)
    fig.append_trace(go.Scatter(x=allof[2][w].index,y=allof[2][w]), row=1, col=1)
    fig.add_hline(y=-20, line_width=3, line_dash="dash", line_color="green",row=1,col=1)
    fig.add_hline(y=0, line_width=3, line_dash="dash", line_color="orange",row=1,col=1)
    fig.add_hline(y=20, line_width=3, line_dash="dash", line_color="black",row=1,col=1)
    fig.update_layout(height=900, width=1000, title_text="Stacked Subplots")
    fig.update_layout(xaxis={'visible': False, 'showticklabels': False})
    st.plotly_chart(fig, use_container_width=True)

st.sidebar.header("Swing Strategy")

progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()


progress_bar.empty()


# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")