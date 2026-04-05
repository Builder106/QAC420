import pandas as pd

df = pd.read_csv('data/legislative_trades.csv')

# Let's find top traders and high-profile trades
df['transaction_date'] = pd.to_datetime(df['transaction_date'], errors='coerce')
df['amount_avg'] = pd.to_numeric(df['amount_avg'], errors='coerce')

top_traders = df.groupby('legislator_name')['amount_avg'].sum().sort_values(ascending=False).head(5)
print("Top 5 Traders by Total Volume:")
print(top_traders)

print("\n--- COVID Crash Timing (Jan-Mar 2020) ---")
covid_trades = df[(df['transaction_date'] >= '2020-01-01') & (df['transaction_date'] <= '2020-03-31')]
covid_sales = covid_trades[covid_trades['transaction_type'] == 'Sale']
top_covid_sellers = covid_sales.groupby('legislator_name')['amount_avg'].sum().sort_values(ascending=False).head(5)
print("Top 5 Sellers Before/During Covid Crash:")
print(top_covid_sellers)

print("\n--- Top Buyers in Tech (NVDA, MSFT, AAPL) during 2020-2022 ---")
tech_trades = df[df['ticker'].isin(['NVDA', 'MSFT', 'AAPL']) & (df['transaction_type'] == 'Purchase')]
top_tech_buyers = tech_trades.groupby('legislator_name')['amount_avg'].sum().sort_values(ascending=False).head(5)
print("Top 5 Buyers of Tech Stocks:")
print(top_tech_buyers)
