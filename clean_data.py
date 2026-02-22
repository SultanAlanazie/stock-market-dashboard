import pandas as pd
import numpy as np

def clean_and_transform_data(input_file='data/stock_data_raw.csv'):
    """Clean data and calculate metrics"""
    
    print("Loading raw data...")
    df = pd.read_csv(input_file)
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Sort by ticker and date
    df = df.sort_values(['Ticker', 'Date'])
    
    # Calculate daily returns
    df['Daily_Return'] = df.groupby('Ticker')['Close'].pct_change() * 100
    
    # Calculate cumulative returns (from start date)
    df['Cumulative_Return'] = df.groupby('Ticker')['Close'].transform(
        lambda x: ((x / x.iloc[0]) - 1) * 100
    )
    
    # Calculate moving averages
    df['MA_50'] = df.groupby('Ticker')['Close'].transform(
        lambda x: x.rolling(window=50, min_periods=1).mean()
    )
    df['MA_200'] = df.groupby('Ticker')['Close'].transform(
        lambda x: x.rolling(window=200, min_periods=1).mean()
    )
    
    # Calculate volatility (30-day rolling standard deviation of returns)
    df['Volatility_30D'] = df.groupby('Ticker')['Daily_Return'].transform(
        lambda x: x.rolling(window=30, min_periods=1).std()
    )
    
    # Add year, month, quarter
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Quarter'] = df['Date'].dt.quarter
    df['Year_Month'] = df['Date'].dt.to_period('M').astype(str)
    
    # Calculate year-to-date (YTD) return
    current_year = df['Date'].dt.year.max()
    ytd_start = df[df['Year'] == current_year].groupby('Ticker')['Close'].first()
    ytd_latest = df[df['Year'] == current_year].groupby('Ticker')['Close'].last()
    ytd_returns = ((ytd_latest / ytd_start) - 1) * 100
    
    # Save cleaned data
    df.to_csv('data/stock_data_cleaned.csv', index=False)
    print(f"✓ Cleaned data saved! Total records: {len(df)}")
    
    # Create summary statistics
    create_summary_stats(df, ytd_returns)
    
    return df

def create_summary_stats(df, ytd_returns):
    """Create summary statistics file"""
    
    latest_date = df['Date'].max()
    latest_data = df[df['Date'] == latest_date]
    
    # Calculate metrics for each stock
    summary = []
    for ticker in df['Ticker'].unique():
        stock_data = df[df['Ticker'] == ticker]
        latest_stock = latest_data[latest_data['Ticker'] == ticker].iloc[0]
        
        summary.append({
            'Ticker': ticker,
            'Company': latest_stock['Company'],
            'Latest_Price': round(latest_stock['Close'], 2),
            'YTD_Return_%': round(ytd_returns.get(ticker, 0), 2),
            '1Y_Return_%': round(latest_stock['Cumulative_Return'], 2),
            'Avg_Volume': int(stock_data['Volume'].mean()),
            '30D_Volatility_%': round(latest_stock['Volatility_30D'], 2),
            'Latest_Date': latest_date.strftime('%Y-%m-%d')
        })
    
    summary_df = pd.DataFrame(summary)
    summary_df = summary_df.sort_values('1Y_Return_%', ascending=False)
    summary_df.to_csv('data/summary_stats.csv', index=False)
    
    print("\n=== Summary Statistics ===")
    print(summary_df.to_string(index=False))
    print(f"\nSummary saved to data/summary_stats.csv")

if __name__ == "__main__":
    df = clean_and_transform_data()
