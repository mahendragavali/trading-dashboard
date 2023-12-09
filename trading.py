import streamlit as st, pandas  as pd,numpy as np,yfinance as yf
import plotly.express as px


st.title('Stock,Futures and Option Dashboard')
st.markdown("<h2 style='color: goldenrod;'>by Mahendra Gavali</h2>", unsafe_allow_html=True)
ticker = st.sidebar.text_input('ticker')
start_date = st.sidebar.date_input('Start Date')
end_date = st.sidebar.date_input('End Date')
data = yf.download(ticker, start = start_date, end = end_date)
fig = px.line(data,x = data.index, y = data['Adj Close'],title = ticker)
st.plotly_chart(fig)

pricing_data,fundamental_data, news =st.tabs(["Pricing Data","Fundamental Data","Top 10 News"])

with pricing_data:
    st.header('Price Movements')
    data2 = data
    data2['%Change']=data['Adj Close']/data['Adj Close'].shift(1) - 1
    data2.dropna(inplace = True)
    st.write(data2)
    annual_return=data2['%Change'].mean()*252*100
    st.write('Annual Return is',annual_return,'%')
    stdev = np.std(data2['%Change'])*np.sqrt(252)
    st.write('Standard Deviation is',stdev*100,'%')
    st.write('Risk Adj. Return is',annual_return/(stdev*100))

## Fundamental Data tab
with fundamental_data:
    st.header('Fundamental Data')
    stock_info = yf.Ticker(ticker)


    # Display annual balance sheet
    st.subheader('Balance Sheet (Annual)')
    balance_sheet_annual = stock_info.balance_sheet
    st.write(balance_sheet_annual)

    # Display annual income statement (Profit and Loss Account)
    st.subheader('Income Statement (Annual)')
    income_statement_annual = stock_info.financials
    st.write(income_statement_annual)

    # Display annual cash flow statement
    st.subheader('Cash Flow Statement (Annual)')
    cash_flow_annual = stock_info.cashflow
    st.write(cash_flow_annual)

import streamlit as st
import requests

# Input box for stock ticker in the sidebar
ticker = st.sidebar.text_input('Enter Stock Ticker:')

if ticker:
    # Fetch news using News API (replace 'your_news_api_key' with an actual API key)
    news_api_key = '6ccac2f77ac44997b32e52d799a24097'
    news_api_url = f'https://newsapi.org/v2/everything?q={ticker}&apiKey={news_api_key}&pageSize=25'

    response = requests.get(news_api_url)
    news_data = response.json()

    # Display news articles sorted by publication date in descending order
    articles = sorted(news_data.get('articles', []), key=lambda x: x['publishedAt'], reverse=True)

    st.header(f'News and Analysis of {ticker}')

    for i, article in enumerate(articles):
        st.subheader(f'News {i + 1}')
        st.write(article['publishedAt'])
        st.write(article['title'])
        st.write(article['description'])

