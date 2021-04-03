# pip install streamlit fbprophet yfinance plotly
import streamlit as st
from datetime import date
import SessionState
import yfinance as yf
#from fbprophet import Prophet
#from fbprophet.plot import plot_plotly
from plotly import graph_objs as go
from streamlit.script_request_queue import RerunData
from streamlit.script_runner import RerunException

st.set_page_config(

page_icon="🧊",
layout="wide",

 )

START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.title('NIFTY 100 Stocks Price Forecast App')




ll_stocks = '''
BPCL
BHARTIARTL
BIOCON
BOSCHLTD
BRITANNIA
CADILAHC
CIPLA
COALINDIA
COLPAL
CONCOR
DLF
DABUR
DIVISLAB
DRREDDY
EICHERMOT
GAIL
GICRE
GODREJCP
GRASIM
HCLTECH
HDFCAMC
HDFCBANK
HDFCLIFE
HAVELLS
HEROMOTOCO
HINDALCO
HINDPETRO
HINDUNILVR
HINDZINC
HDFC
ICICIBANK
ICICIGI
ICICIPRULI
ITC
IOC
IGL
INDUSTOWER
INDUSINDBK
NAUKRI
INFY
INDIGO
JSWSTEEL
KOTAKBANK
LTI
LT
LUPIN
M&M
MARICO
MARUTI
MOTHERSUMI
MUTHOOTFIN
NMDC
NTPC
NESTLEIND
ONGC
OFSS
PETRONET
PIDILITIND
PEL
PFC
POWERGRID
PGHH
PNB
RELIANCE
SBICARD
SBILIFE
SHREECEM
SIEMENS
'''


stock_list = []

for stock in ll_stocks.split('\n'):
    if len(stock) > 0:
        stock = stock + '.NS'
        stock_list.append(stock)
    
 
stocks = stock_list
 
selected_stock = st.selectbox('Select dataset for prediction', stocks)

@st.cache(suppress_st_warning=True)
def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    st.subheader('Raw data of stock symbol')
    st.write(data.tail())
    return data

session_state = SessionState.get(data='')
#session_state.data = load_data(selected_stock)

if st.button('Load Symbol Data'):
    data_load_state = st.text('Loading data...')
    session_state.data = load_data(selected_stock)
    data_load_state.text('Loading data... done!')
    
    

data =  session_state.data
# Plot raw data
@st.cache(suppress_st_warning=True)
def plot_raw_data():
    try:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
        fig.layout.update(title_text=str('Time Series data with Rangeslider for : {}').format(selected_stock), xaxis_rangeslider_visible=True)
        st.plotly_chart(fig, use_container_width=True)
    except:
        st.markdown(" ## Error plotting figure please make sure that you have loaded the data")
    
    
if st.button('Plot Raw Data'):
    
    plot_raw_data()
    raise RerunException(RerunData())
    
st.subheader('For how many year do you want to make the prediction of stock prices of selected stock')
n_years = st.slider('Years of prediction:', 1, 4)
period = n_years * 365

@st.cache
def predict_stock(data):
    df_train = data[['Date','Close']]
    df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})
    
    

'''

selected_stock = st.selectbox('Select dataset for prediction', stocks)

n_years = st.slider('Years of prediction:', 1, 4)
period = n_years * 365


@st.cache
def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data

	
data_load_state = st.text('Loading data...')
data = load_data(selected_stock)
data_load_state.text('Loading data... done!')

st.subheader('Raw data')
st.write(data.tail())

# Plot raw data
def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
    fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)
	
plot_raw_data()



# Predict forecast with Prophet.
df_train = data[['Date','Close']]
df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

m = Prophet()
m.fit(df_train)
future = m.make_future_dataframe(periods=period)
forecast = m.predict(future)

# Show and plot forecast
st.subheader('Forecast data')
st.write(forecast.tail())
    
st.write(f'Forecast plot for {n_years} years')
fig1 = plot_plotly(m, forecast)
st.plotly_chart(fig1)

st.write("Forecast components")
fig2 = m.plot_components(forecast)
st.write(fig2)
'''