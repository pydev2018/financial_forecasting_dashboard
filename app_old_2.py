# pip install streamlit fbprophet yfinance plotly
import streamlit as st
from datetime import date
import SessionState as ss
import pandas as pd
import yfinance as yf
from fbprophet import Prophet
from fbprophet.plot import plot_plotly , plot_components_plotly
from plotly import graph_objs as go
from streamlit.script_request_queue import RerunData
from streamlit.script_runner import RerunException

st.set_page_config(

page_icon="🧊",
layout="wide",

 )


query_params = st.experimental_get_query_params()

session_state = ss.get(session_id=0, data='', fited_prophet='',first_query_params=st.experimental_get_query_params())

first_query_params = session_state.first_query_params


START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.title('NIFTY 100 Stocks Price Forecast App')


list_df = pd.read_csv('ind_nifty100list.csv')
kk = list_df['Symbol']
new_list = list()

for i in list(kk):
    i = i + ".NS"
    new_list.append(i)
    

 
stocks = new_list


default_values = {
    "stock_selectbox": int(session_state.first_query_params.get("stock_selectbox", [0])[0]),
    "year_slider": int(session_state.first_query_params.get("year_slider", [1])[0]),
}

stock_selectbox = st.selectbox(
    "Select stock symbol for predicting stock prices",
    stocks,
    key=session_state.session_id,
    index=default_values["stock_selectbox"],
)
query_params["stock_selectbox"] = stocks.index(stock_selectbox)

@st.cache(suppress_st_warning=True)
def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data



def plot_raw_data(data):
    try:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
        fig.layout.update(title_text=str('Time Series data with Rangeslider for : {}').format(stock_selectbox), xaxis_rangeslider_visible=True)
        st.plotly_chart(fig, use_container_width=True)
    except:
        st.markdown(" ## Error plotting figure please make sure that you have loaded the data")
#session_state = SessionState.get(data='')
#session_state.data = load_data(selected_stock)

st.subheader('For how many year do you want to make the prediction of stock prices of selected stock')
year_slider = st.slider(
    "Number of years for prediction",
    min_value=1,
    max_value=5,
    key=session_state.session_id,
    value=default_values["year_slider"],
)
query_params["year_slider"] = year_slider
period = year_slider * 365

if st.button('Load and plot Symbol Data'):
    data_load_state = st.text('Loading data...')
    session_state.data = load_data(stock_selectbox)
    data_load_state.text('Loading data... done!')
    st.subheader('Five latest rows from stock symbol, data downloaded from 2015 till today , ready for prediction!')
    st.table(session_state.data.tail())
    st.subheader('Plot of data')
    data = session_state.data
    plot_raw_data(data)
    


@st.cache(suppress_st_warning=True)
def fit_prophet_model(data):
    df_train = data[['Date','Close']]
    df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})
    m = Prophet()
    fitted_m = m.fit(df_train)
    return fitted_m
    
    
fitted_m = fit_prophet_model(session_state.data)


@st.cache(suppress_st_warning=True)
def predict_stock(data, fitted_m):
    future = m.make_future_dataframe(periods=period)
    forecast = m_1.predict(future)
    return m , forecast 


    
    
    
if st.checkbox('Plot the prediction data'):

    try:
        data_predict_state = st.text('predicting stock prices for the next {} years'.format(query_params["year_slider"]))
        data = session_state.data
        m, forecast = predict_stock(data, m_1)
        st.subheader('Forecast data')
        st.write(forecast.tail())
                
        st.write(f'Forecast plot for {query_params["year_slider"]} years')
        fig1 = plot_plotly(m, forecast)
        st.plotly_chart(fig1, use_container_width=True)

        st.write("Forecast components")
        fig2 = plot_components_plotly(m, forecast)
        #fig2 = m.plot_components(forecast)
        st.write(fig2, use_container_width=True)
    except:
        st.markdown("## Have you loaded the data? Please press the load and plot button before running the forecast !")




    




st.experimental_set_query_params(**query_params)
