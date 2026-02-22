import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os

def fetch_stock_data():
    tickers = {
        'AAPL': 'Apple',
        'MSFT': 'Microsoft',
        'GOOGL': 'Google',
        'AMZN': 'Amazon',
        'NVDA': 'NVIDIA',
        'META': 'Meta',
        'TSLA': 'Tesla',
        '^GSPC': 'S&P 500'
    }

    end_date = datetime.now()
    start_date = end_date - timedelta(days=730)

    print(f"Fetching data from {start_date.date()} to {end_date.date()}...")

    os.makedirs('data', exist_ok=True)
    all_data = []

    for ticker_sym, name in tickers.items():
        print(f"Downloading {name} ({ticker_sym})...")
        try:
            ticker_obj = yf.Ticker(ticker_sym)
            data = ticker_obj.history(start=start_date, end=end_date)

            if data.empty:
                print(f"  ⚠ No data returned for {ticker_sym}")
                continue

            # Flatten MultiIndex columns if present
            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.get_level_values(0)

            data = data.reset_index()

            # Ensure Date column is clean (strip timezone info)
            data['Date'] = pd.to_datetime(data['Date']).dt.tz_localize(None)

            data['Ticker'] = ticker_sym
            data['Company'] = name

            # Keep only needed columns
            keep_cols = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Ticker', 'Company']
            data = data[[c for c in keep_cols if c in data.columns]]

            all_data.append(data)
            print(f"  ✓ {len(data)} rows downloaded")

        except Exception as e:
            print(f"  ✗ Error fetching {ticker_sym}: {e}")

    if not all_data:
        print("\n❌ No data was fetched. Try:")
        print("   pip install --upgrade yfinance")
        return pd.DataFrame()

    df = pd.concat(all_data, ignore_index=True)
    df.to_csv('data/stock_data_raw.csv', index=False)
    print(f"\n✅ Done! Total records: {len(df)}")
    print(f"   Date range: {df['Date'].min().date()} to {df['Date'].max().date()}")
    print(f"   Stocks: {df['Company'].unique().tolist()}")
    return df


if __name__ == "__main__":
    df = fetch_stock_data()
    if not df.empty:
        print("\nSample data:")
        print(df.head())
