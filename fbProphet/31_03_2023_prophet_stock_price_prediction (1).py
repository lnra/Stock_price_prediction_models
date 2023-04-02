# -*- coding: utf-8 -*-
"""31_03_2023_Prophet_stock_price_prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aS3m10sNPtMef--R06Of4eHMI0bzHStP

# Import Libraries
"""

# Install yfinance and prophet libraries
!pip install yfinance
!pip install prophet

# Import yfinance, datetime, pandas, plotly, prophet libraries
import yfinance as yf
from datetime import datetime
import pandas as pd
import plotly.express as px
from prophet import Prophet
from prophet.diagnostics import performance_metrics
from prophet.plot import plot_plotly
from prophet.diagnostics import cross_validation
from prophet.plot import plot_cross_validation_metric
import json
from prophet.serialize import model_to_json, model_from_json

"""In the code block above, we first install the yfinance and prophet libraries using pip, which allows us to access financial data from Yahoo Finance and to use the Prophet forecasting algorithm.

Then we import yfinance, datetime, pandas, plotly, prophet, and other relevant libraries using the import statement.

The plotly library is a popular library for creating interactive plots and visualizations in Python. The prophet library provides a powerful algorithm for time-series forecasting, which we will be using in this code block. We also import the json library to serialize and deserialize Prophet models.

# Data Analysis
"""

# Define the stock symbol and start date for data collection
symbol= 'TSLA'
start_date = datetime(2018, 1, 1)

# Download data from YahooFinance API for the given stock symbol and start date
df = yf.download(symbol, start=start_date)


# Save the downloaded data to a CSV file
df.to_csv('TSLA.csv')

# Read the saved CSV file into a Pandas DataFrame for further analysis
hist=pd.read_csv('TSLA.csv')

# Print the last 5 rows of hist dataframe
hist.tail()

# Print the first 5 rows of hist dataframe
hist.head()

# Select the Date and Close columns from hist dataframe
hist = hist[['Date', 'Close']].copy()

# Rename the Date and Close columns as 'ds' and 'y', respectively
hist = hist.rename({'Date': 'ds', 'Close': 'y'}, axis='columns')

# Print the last 5 rows of hist dataframe
hist.tail()

"""In the code block above, we select only the Date and Close columns from the hist dataframe using the double bracket indexing syntax. The .copy() method is used to make a copy of the resulting dataframe, so that any changes made to the new dataframe do not affect the original hist dataframe.

Next, we use the .rename() method to rename the Date column as ds and the Close column as y. The axis='columns' parameter is used to indicate that we are renaming column names rather than row names.

Finally, we print the last 5 rows of the hist dataframe using the .tail() method to confirm that the column names have been updated correctly.
"""

# Create a line plot using plotly express
fig = px.line(hist, x='ds', y='y', title='Stock Price change over time')
fig.show()

"""# Model training"""

# Create a Prophet model
m = Prophet()

# Fit the model to the historical data
m=m.fit(hist)

"""# Predict future based on trained model"""

# Generate a dataframe with future dates to forecast
future = m.make_future_dataframe(periods=30)

# Generate a forecast for the future dates
forecast = m.predict(future)

# Display all columns of the forecast dataframe
pd.options.display.max_columns = None

# Print the last 5 rows of the forecast dataframe
forecast.tail()

forecast[['ds','yhat']]

figure1 = m.plot(forecast)
figure2 = m.plot_components(forecast)

plot_plotly(m, forecast)

"""# Cross Validaton

In order for us to find out how our model performs and know if we are making progress we need some kind of validation. Prophet includes functionality for time series cross validation to measure forecast error using historical data.

This cross validation procedure can be done automatically for a range of historical cutoffs using the `cross_validation` function. We specify,

* `horizon` - the forecast horizon
* `initial` - the size of the initial training period
* `period `- the spacing between cutoff dates
By default, the initial training period is set to three times the horizon, and cutoffs (period) are made every half a horizon.

The resulting dataframe can now be used to compute error measures of yhat vs. y.

Here we do cross-validation to assess prediction performance on a horizon of 180 days, starting with 540 days of training data in the first cutoff and then making predictions every 31 days.
"""

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

df_p = performance_metrics(df_cv)
df_p.head()

df_p.tail()

"""Cross validation performance metrics can be visualized with `plot_cross_validation_metric`, here shown for `RMSE`. """

fig = plot_cross_validation_metric(df_cv, metric='rmse')

new_pred_plot = pd.DataFrame({
    'dates': forecast['ds'],
    'predicted price':forecast['yhat']
})

new_pred_plot= new_pred_plot[-30:]
new_pred_plot

jsonresult  = new_pred_plot.to_json(orient='records')

jsonresult

with open('data.json', 'w') as f:
    json.dump(jsonresult, f)