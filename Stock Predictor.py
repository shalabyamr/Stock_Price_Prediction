import yfinance as yf
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

# -----------------------------------------
# 1. Download DSV.TO stock historical data
# -----------------------------------------
ticker = input("Yahoo Finance Ticker: " ).strip().upper() #"DSV.TO"
df = yf.download(ticker, period="5y", interval="1d", auto_adjust=True)

# Prepare data for Prophet
df = df.reset_index()[["Date", "Close"]]
df.columns = ["ds", "y"]        # Prophet requires ds (date) and y (value)

# -----------------------------------------
# 2. Build Prophet Model
# -----------------------------------------
model = Prophet(
    daily_seasonality=True,
    weekly_seasonality=True,
    yearly_seasonality=True,
    changepoint_prior_scale=0.50   # adjust sensitivity

)

model.fit(df)

# -----------------------------------------
# 3. Forecast into the future
# -----------------------------------------
forecast_period = int(input("Forecast Number of Days: "))
future = model.make_future_dataframe(periods=forecast_period, freq='D', include_history=True)
forecast = model.predict(future)
forecast["ds"] = pd.to_datetime(forecast['ds'])
forecast["ds"] = forecast["ds"].dt.normalize() #here
today = pd.to_datetime('today').normalize()
forecast["yhat"] = forecast["yhat"].round(2)
forecast[["ds", "yhat"]].to_csv(f"{ticker}_historical_and_forecast.csv", index=False)
forecast = forecast[forecast['ds'] >= today]
# -----------------------------------------
# 4. Show results
# -----------------------------------------
print("Future price prediction:")
print(forecast[["ds", "yhat"]].tail(90))
forecast[forecast['ds'] >= today][["ds", "yhat"]].to_csv(f"{ticker}_forecast.csv", index=False)

# Plot full forecast
forecast = forecast[forecast["ds"] >= today]
model.plot(forecast, xlabel="Date", ylabel="DSV STOCK PREDICTION", include_legend=True, plot_cap=True)
plt.title(f"DSV.TO Stock Forecast ({forecast_period} days forward)")
plt.savefig(f"{ticker}_forecast.png")
plt.show()
# Plot trends/components (seasonality, trend strength, etc.)
model.plot_components(forecast)
plt.savefig(f"{ticker}_components.png")
plt.show()

