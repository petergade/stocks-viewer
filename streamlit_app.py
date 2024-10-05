import streamlit as st
from polygon import RESTClient
import pandas as pd
from polygon.rest.models import Timeframe
from datetime import datetime, timedelta

date_from = datetime.today() - timedelta(days = (365 * 5) - 7)
date_to = datetime.today()

st.header('Polygon + Streamlit Demo App')
symbol = st.text_input('Enter a stock symbol', 'AAPL')

polygon_api_key = st.secrets['polygon_api_key']
client = RESTClient(polygon_api_key)

rows = [st.columns(3) for _ in range(2)]

if rows[0][0].button('Get details'):
    try:
        details = client.get_ticker_details(symbol)
        st.success(f'Ticker: {details.ticker}\n\n'
                   f'Company Address: {details.address}\n\n'
                   f'Market Cap: ${details.market_cap:,}')
    except Exception as e:
        st.exception(f'Exception: {e}')

# Current bid info
if rows[0][1].button('Get quote'):
    try:
        aggs = client.get_previous_close_agg(symbol)
        for agg in aggs:
            st.success(
                f'Ticker: {agg.ticker}\n\n'
                f'Close: ${agg.close}\n\n'
                f'High: ${agg.high}\n\n'
                f'Low: ${agg.low}\n\n'
                f'Volume: {agg.volume:,}\n\n'
            )
    except Exception as e:
        st.exception(f'Exception: {e}')
if rows[0][2].button('Get historical'):
    try:
        dataRequest = client.list_aggs(
            ticker = symbol,
            multiplier = 1,
            timespan = 'day',
            from_ = '2020-01-01',
            to = '2024-10-05'
        )
        chart_data = pd.DataFrame(dataRequest)
        chart_data['date_formatted'] = chart_data['timestamp'].apply(lambda x: pd.to_datetime(x*1000000))

        st.line_chart(chart_data, x = 'date_formatted', y = 'close', x_label = 'date', y_label = 'price')
    except Exception as e:
        st.exception(f'Exception: {e}')



if rows[1][0].button('Get SMA'):
    try:
        sma_10 = client.get_sma(
            ticker = symbol,
            timestamp_gte = date_from,
            timespan = 'day',
            window = 10,
            series_type = 'close',
            limit = 5000
        )
        chart_data_sma10 = pd.DataFrame(sma_10.values)
        chart_data_sma10['date'] = chart_data_sma10['timestamp'].apply(lambda x: pd.to_datetime(x * 1000000))
        chart_data_sma10.rename(columns = {'value': 'SMA_10'}, inplace = True)

        sma_50 = client.get_sma(
            ticker = symbol,
            timestamp_gte = date_from,
            timespan = 'day',
            window = 50,
            series_type = 'close',
            limit = 5000
        )
        chart_data_sma50 = pd.DataFrame(sma_50.values)
        chart_data_sma50['date'] = chart_data_sma50['timestamp'].apply(lambda x: pd.to_datetime(x*1000000))
        chart_data_sma50.rename(columns = {'value': 'SMA_50'}, inplace = True)

        sma_100 = client.get_sma(
            ticker = symbol,
            timestamp_gte = date_from,
            timespan = 'day',
            window = 100,
            series_type = 'close',
            limit = 5000
        )
        chart_data_sma100 = pd.DataFrame(sma_100.values)
        chart_data_sma100['date'] = chart_data_sma100['timestamp'].apply(lambda x: pd.to_datetime(x * 1000000))
        chart_data_sma100.rename(columns = {'value': 'SMA_100'}, inplace = True)

        sma_200 = client.get_sma(
            ticker = symbol,
            timestamp_gte = date_from,
            timespan = 'day',
            window = 200,
            series_type = 'close',
            limit = 5000
        )
        chart_data_sma200 = pd.DataFrame(sma_200.values)
        chart_data_sma200['date'] = chart_data_sma200['timestamp'].apply(lambda x: pd.to_datetime(x * 1000000))
        chart_data_sma200.rename(columns = {'value': 'SMA_200'}, inplace = True)

        prices = client.list_aggs(
            ticker = symbol,
            multiplier = 1,
            timespan = 'day',
            from_ = date_from,
            to = date_to
        )
        chart_data_prices = pd.DataFrame(prices)
        chart_data_prices['date'] = chart_data_prices['timestamp'].apply(lambda x: pd.to_datetime(x * 1000000))
        chart_data_prices.rename(columns = {'close': 'Price'}, inplace = True)



        chart_data = pd.merge(chart_data_sma50[['date', 'SMA_50']], chart_data_sma200[['date', 'SMA_200']], on = 'date', how = 'inner')
        chart_data = pd.merge(chart_data, chart_data_sma10[['date', 'SMA_10']], on = 'date', how = 'inner')
        chart_data = pd.merge(chart_data, chart_data_sma100[['date', 'SMA_100']], on = 'date', how = 'inner')
        chart_data = pd.merge(chart_data, chart_data_prices[['date', 'Price']], on = 'date', how = 'inner')

        chart_data

        st.line_chart(chart_data.set_index('date'), y = ['SMA_10', 'SMA_50', 'Price'], x_label = 'Date', y_label = 'Price')
    except Exception as e:
        st.exception(f'Exception: {e}')

if rows[1][1].button('Get financials'):
    try:
        financials = []
        for f in client.vx.list_stock_financials(
            ticker = symbol,
            period_of_report_date_gte = '2020-01-01',
            timeframe = Timeframe.ANNUAL
        ):
            financials.append(f)
        st.success(financials)
    except Exception as e:
        st.exception(f'Exception: {e}')