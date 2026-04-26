import streamlit as st
import yfinance as yf
import pandas as pd
import requests
from streamlit_autorefresh import st_autorefresh

st.set_page_config(layout="wide")

st_autorefresh(interval=3000)

# ---------------- CSS TERMINAL STYLE ----------------

st.markdown("""
<style>

body {
background-color:#0b0f14;
color:white;
}

.metric-container{
background:#111822;
padding:15px;
border-radius:8px;
box-shadow:0 0 8px #00ffae;
text-align:center;
}

.metric-title{
font-size:14px;
color:#9aa3ad;
}

.metric-price{
font-size:28px;
font-weight:bold;
}

.metric-change{
font-size:14px;
}

.section-title{
font-size:22px;
margin-top:30px;
margin-bottom:10px;
color:#00ffae;
}

</style>
""",unsafe_allow_html=True)

st.title("GLOBAL TRADING MONITOR")

# ---------------- FETCH FUNCTION ----------------

@st.cache_data(ttl=3)
def get_price(ticker):

    try:

        data=yf.Ticker(ticker).history(period="2d")

        last=data["Close"].iloc[-1]

        prev=data["Close"].iloc[-2]

        pct=((last-prev)/prev)*100

        return round(last,2),round(pct,2)

    except:

        return None,None


def tile(col,name,ticker):

    price,pct=get_price(ticker)

    if price is None:

        col.markdown(f"""
        <div class="metric-container">
        <div class="metric-title">{name}</div>
        <div class="metric-price">NA</div>
        </div>
        """,unsafe_allow_html=True)

    else:

        color="lime" if pct>0 else "red"

        col.markdown(f"""
        <div class="metric-container">
        <div class="metric-title">{name}</div>
        <div class="metric-price">{price}</div>
        <div class="metric-change" style="color:{color}">{pct}%</div>
        </div>
        """,unsafe_allow_html=True)


# ---------------- GLOBAL INDICES ----------------

st.markdown('<div class="section-title">GLOBAL INDICES</div>',unsafe_allow_html=True)

indices={
"NIFTY":"^NSEI",
"BANK NIFTY":"^NSEBANK",
"SENSEX":"^BSESN",
"GIFT NIFTY":"NIFTY50.NS",
"NASDAQ":"^IXIC",
"DOW JONES":"^DJI",
"S&P 500":"^GSPC",
"DAX":"^GDAXI",
"FTSE":"^FTSE",
"CAC":"^FCHI",
"ASX":"^AXJO",
"NIKKEI":"^N225",
"SHANGHAI":"000001.SS"
}

cols=st.columns(4)

i=0

for name,ticker in indices.items():

    tile(cols[i%4],name,ticker)

    i+=1


# ---------------- VOLATILITY ----------------

st.markdown('<div class="section-title">VOLATILITY</div>',unsafe_allow_html=True)

vol={
"INDIA VIX":"^INDIAVIX",
"US VIX":"^VIX"
}

cols=st.columns(2)

i=0

for name,ticker in vol.items():

    tile(cols[i%2],name,ticker)

    i+=1


# ---------------- COMMODITIES ----------------

st.markdown('<div class="section-title">COMMODITIES</div>',unsafe_allow_html=True)

commod={
"BRENT":"BZ=F",
"GOLD":"GC=F",
"SILVER":"SI=F"
}

cols=st.columns(3)

i=0

for name,ticker in commod.items():

    tile(cols[i%3],name,ticker)

    i+=1


# ---------------- MACRO ----------------

st.markdown('<div class="section-title">MACRO</div>',unsafe_allow_html=True)

macro={
"USDINR":"USDINR=X",
"US 10Y":"^TNX"
}

cols=st.columns(2)

i=0

for name,ticker in macro.items():

    tile(cols[i%2],name,ticker)

    i+=1


# ---------------- NIFTY STOCKS ----------------

st.markdown('<div class="section-title">TOP NIFTY STOCKS</div>',unsafe_allow_html=True)

nifty={
"Reliance":"RELIANCE.NS",
"HDFC Bank":"HDFCBANK.NS",
"ICICI Bank":"ICICIBANK.NS",
"Infosys":"INFY.NS",
"TCS":"TCS.NS"
}

cols=st.columns(5)

i=0

for name,ticker in nifty.items():

    tile(cols[i%5],name,ticker)

    i+=1


# ---------------- NASDAQ STOCKS ----------------

st.markdown('<div class="section-title">TOP NASDAQ STOCKS</div>',unsafe_allow_html=True)

nasdaq={
"Apple":"AAPL",
"Microsoft":"MSFT",
"Nvidia":"NVDA",
"Amazon":"AMZN",
"Google":"GOOGL"
}

cols=st.columns(5)

i=0

for name,ticker in nasdaq.items():

    tile(cols[i%5],name,ticker)

    i+=1


# ---------------- OPTION CHAIN ----------------

st.markdown('<div class="section-title">NIFTY OPTION CHAIN</div>',unsafe_allow_html=True)

try:

    url="https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"

    headers={
    "User-Agent":"Mozilla/5.0",
    "Accept-Language":"en-US,en;q=0.9"
    }

    session=requests.Session()

    session.get("https://www.nseindia.com",headers=headers)

    data=session.get(url,headers=headers).json()

    records=data["records"]["data"]

    rows=[]

    for r in records:

        strike=r["strikePrice"]

        if "CE" in r and "PE" in r:

            rows.append({

            "Strike":strike,

            "Call OI":r["CE"]["openInterest"],
            "Put OI":r["PE"]["openInterest"]

            })

    df=pd.DataFrame(rows)

    st.dataframe(df)

except:

    st.write("Option chain unavailable (NSE block)")

import os
os.system("pip install yfinance pandas requests streamlit-autorefresh lxml")
    
