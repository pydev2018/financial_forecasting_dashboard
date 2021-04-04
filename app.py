import streamlit as st
from datetime import date
#from session_state import get_state
import pandas as pd
import yfinance as yf
from fbprophet import Prophet
from fbprophet.plot import plot_plotly , plot_components_plotly
from plotly import graph_objs as go
#from streamlit.script_request_queue import RerunData
#from streamlit.script_runner import RerunException
from SessionState import get


empty_df = pd.DataFrame(columns=['Date',  'Open'  , 'High',   'Low',   'Close' , 'Adj Close' , 'Volume'])
session_state = get(data=empty_df, prediction_years=1, fitted_m= '', stock_name = 'None')

st.set_page_config(

page_icon="🧊",
layout="wide",

 )


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

selected_stock = st.selectbox("Choose the stock that you want to predict", options=stocks)


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
        fig.layout.update(title_text=str('Showing Stock price data chart for Stock symbol: {}'.format(session_state.stock_name)), xaxis_rangeslider_visible=True,height=750)
        st.plotly_chart(fig, use_container_width=True)
    except:
        st.markdown(" ## Error plotting figure please make sure that you have loaded the data")



if st.button('Load and plot Symbol Data'):
    session_state.stock_name = selected_stock
    data_load_state = st.text('Loading data...')
    session_state.data = load_data(session_state.stock_name)
    data_load_state.text('Loading data... done!')
    st.subheader('Data downloaded from Jan 2015 till today , ready for prediction!')
    #st.table(session_state.data.tail())
    st.subheader('Plot of data, use rangeslider to view desired time range.')
    
plot_raw_data(session_state.data)
    
    


@st.cache(suppress_st_warning=True)
def fit_prophet_model(data):
    df_train = data[['Date','Close']]
    df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})
    m = Prophet()
    fitted_m = m.fit(df_train)
    return fitted_m


if st.button("Fit prophet model"):
    try:
        data_load_state = st.text('Fitting model on data...')
        session_state.fitted_m = fit_prophet_model(session_state.data)
        data_load_state = st.text('Model fitting complete...')
    except:
        st.markdown('## Have you loaded the data before fitting ?')
       


@st.cache(suppress_st_warning=True)
def predict_stock(data, fitted_m, period):
    future = fitted_m.make_future_dataframe(periods=period)
    forecast = fitted_m.predict(future)
    return future , forecast 


st.subheader('For how many year do you want to make the prediction of stock prices of selected stock')
predict_years = st.slider("Number of years for prediction",
                                min_value=1,
                                max_value=5)

session_state.prediction_years = predict_years

if st.button('Plot the prediction data'):

    try:
        data_predict_state = st.text('predicting stock prices for the next {} years'.format(session_state.prediction_years))
        data = session_state.data
        future, forecast = predict_stock(session_state.data, session_state.fitted_m , session_state.prediction_years * 365 )
        st.subheader('Forecast data')
        st.write(forecast.tail())
                    
        st.write(f'Forecast plot for {session_state.prediction_years} years')
        fig1 = plot_plotly(session_state.fitted_m, forecast)
        st.plotly_chart(fig1, use_container_width=True)

    except:
        st.markdown("## Have you loaded the data? Please press the load and plot button before running the forecast !")


