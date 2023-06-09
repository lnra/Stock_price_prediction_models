# -*- coding: utf-8 -*-
"""31_03_2023_Prophet_stock_price_prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aS3m10sNPtMef--R06Of4eHMI0bzHStP
"""

! pip install yfinance
import yfinance as yf
from datetime import datetime 

# Define the stock symbol and start date for data collection
symbol= 'TSLA'
start_date = datetime(2018, 1, 1)

# Download data from YahooFinance API for the given stock symbol and start date
df = yf.download(symbol, start=start_date)


# Save the downloaded data to a CSV file
df.to_csv('TSLA.csv')

# Read the saved CSV file into a Pandas DataFrame for further analysis
hist=pd.read_csv('TSLA.csv')

hist.tail()

hist.head()

hist = hist[['Date', 'Close']].copy()
hist = hist.rename({'Date': 'ds', 'Close': 'y'}, axis='columns')
hist.tail()

import plotly.express as px

fig = px.line(hist, x='ds', y='y', title='Stock Price change over time')
fig.show()

!pip install prophet

from prophet import Prophet
m = Prophet()

m = Prophet()

m.fit(hist)

import pandas as pd
future = m.make_future_dataframe(periods=30)
forecast = m.predict(future)
pd.options.display.max_columns = None
forecast.tail()

forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

forecast[['ds','yhat']]

figure1 = m.plot(forecast)
figure2 = m.plot_components(forecast)

from prophet.plot import plot_plotly
plot_plotly(m, forecast)

"""# Cross Validaton

In order for us to find out how our model performs and know if we are making progress we need some kind of validation. Prophet includes functionality for time series cross validation to measure forecast error using historical data.

This cross validation procedure can be done automatically for a range of historical cutoffs using the `cross_validation` function. We specify,

`horizon` - the forecast horizon
`initial` - the size of the initial training period
`period `- the spacing between cutoff dates
By default, the initial training period is set to three times the horizon, and cutoffs (period) are made every half a horizon.

The resulting dataframe can now be used to compute error measures of yhat vs. y.

Here we do cross-validation to assess prediction performance on a horizon of 180 days, starting with 540 days of training data in the first cutoff and then making predictions every 31 days.
"""

from prophet.diagnostics import cross_validation

df_cv = cross_validation(m, initial='150 days', period='15 days', horizon = '50 days')

"""# Performance Metrics

https://facebook.github.io/prophet/docs/diagnostics.html

Prophet comes with some built-in performance metrics, The performance metrics available are:

* `mse:` mean absolute error
* `rmse:` mean squared error
* `mae:` Mean average error
* `mape:` Mean average percentage error
* `mdape:` Median average percentage error
The code for validating and gathering performance metrics is shown below:
"""

from prophet.diagnostics import performance_metrics
df_p = performance_metrics(df_cv)
df_p.head()

df_p.tail()

"""Cross validation performance metrics can be visualized with `plot_cross_validation_metric`, here shown for `RMSE`. """

from prophet.plot import plot_cross_validation_metric

fig = plot_cross_validation_metric(df_cv, metric='rmse')

import json
from prophet.serialize import model_to_json, model_from_json

with open('stock_price.json', 'w') as fout:
    json.dump(model_to_json(m), fout)  # Save model

with open('stock_price.json', 'rb') as fin:
    m = model_from_json(json.load(fin))  # Load model

new_pred_plot = pd.DataFrame({
    'dates': forecast['ds'],
    'predicted price':forecast['yhat']
})

new_pred_plot= new_pred_plot[-30:]
new_pred_plot

jsonresult  = new_pred_plot.to_json(orient='records')

jsonresult

import json
with open('data.json', 'w') as f:
    json.dump(jsonresult, f)