# Stock Market Analysis Dashboard

## Project Overview

This project presents an interactive financial dashboard that tracks and compares the performance of seven major technology stocks (Apple, Microsoft, Google, Amazon, NVIDIA, Meta, and Tesla) against the S&P 500 benchmark index. The central question the dashboard is designed to answer is: *How have the most influential tech companies performed over the past year, and how do they compare to the broader market?*

The motivation behind choosing this topic was the sustained dominance of large-cap technology companies in driving overall market returns. For a non-technical stakeholder such as a retail investor, portfolio manager, or business analyst, understanding how individual stocks move relative to each other and against the market benchmark provides immediate, actionable context. Rather than reporting static figures, the dashboard allows the user to dynamically select any combination of stocks, filter by time period, and drill into specific dimensions of performance, all within a single interface.

---

## Data Source

Data was collected entirely through the **Yahoo Finance API** via the open-source Python library `yfinance`. The fetch script (`fetch_data.py`) pulls two years of daily historical price and volume data for each ticker from February 2024 to February 2026. The resulting dataset contains OHLCV records (Open, High, Low, Close, Volume) for the following:

| Ticker | Company |
|--------|---------|
| AAPL | Apple |
| MSFT | Microsoft |
| GOOGL | Google |
| AMZN | Amazon |
| NVDA | NVIDIA |
| META | Meta |
| TSLA | Tesla |
| ^GSPC | S&P 500 |

Yahoo Finance was selected for its reliability, zero-cost access, and breadth of historical data. Each record represents one trading day. The raw dataset contains approximately 4,000 rows across all tickers, stored locally as `data/stock_data_raw.csv` before transformation.

---

## Steps and Methodology

### Data Collection

The data pipeline begins with (fetch_data.py) file, which calls `yfinance.Ticker.history()` for each symbol and normalizes the output into a flat tabular format. Timezone information is stripped from the Date column to ensure compatibility across platforms, and only the required columns (Date, Open, High, Low, Close, Volume, Ticker, and Company) are retained. All tickers are concatenated into a single raw CSV file.

### Data Cleaning and Feature Engineering

The cleaning and transformation logic lives in `clean_data.py`. After loading the raw file, records are sorted by ticker and date to ensure chronological ordering, which is a prerequisite for all rolling window calculations. The following derived features are computed for each ticker independently using Pandas `groupby` and `transform` operations:

**Daily Return** is the percentage change in the closing price from one trading day to the next, giving a normalized day-over-day performance measure.

**Cumulative Return** is computed as the percentage gain from the very first date in the dataset to each subsequent date, anchored at zero. This is the primary metric used in the Total Gains chart and directly answers the question of how much an investment would have grown.

**50-Day and 200-Day Moving Averages** are rolling means of the closing price, computed with a minimum of one period to avoid leading null values. These are standard technical analysis indicators used in the Price History tab to identify trend direction and crossover signals.

**30-Day Rolling Volatility** measures the annualized standard deviation of daily returns over a trailing 30-day window. Higher volatility indicates greater price instability, which is visualized in the Price Swings tab.

**Year-to-Date (YTD) Return** is computed by dividing the latest closing price by the first closing price of the current calendar year, providing a snapshot of performance since January 1st.

A summary statistics file (`data/summary_stats.csv`) is generated containing the latest price, YTD return, one-year cumulative return, average daily volume, and 30-day volatility for each stock. This summary feeds the KPI bar and the watchlist panel.

### Tool Selection

The dashboard is built with **Streamlit** as the application framework, **Plotly** for interactive charting, and **Pandas** for all data manipulation. Streamlit was chosen over alternatives like Tableau because it allows a Python-first development workflow with no front-end boilerplate, supports deployment as a shareable web application, and integrates natively with Plotly for interactive visualizations. The entire application is contained in a single `dashboard.py` file, making it easy to maintain and extend.

### Design Decisions

The visual design follows a dark, finance-terminal aesthetic using a deep green color palette, a deliberate choice to evoke professional trading interfaces while remaining visually distinct from generic dashboards. The layout divides into a narrow left sidebar for global controls and a wide main panel, with the right side reserved for a persistent watchlist that mirrors the selected stocks and their key metrics at a glance.

Interactivity was designed to be progressive: the user first selects which stocks to watch via the sidebar multiselect, then explores each analytical dimension through four tabs (Total Gains, Price History, Trading Activity, Price Swings). The watchlist panel on the right provides constant context regardless of which chart tab is active. All stock filters cascade correctly — removing a stock from the sidebar immediately removes it from the watchlist and all charts without any orphaned state.

---

## Dashboard Screenshots

### Total Gains — Cumulative Return Over Time
<img width="1909" height="984" alt="totalGains" src="https://github.com/user-attachments/assets/3ca0e1ee-f75d-4b00-8e65-780818ea99f3" />

The Total Gains tab displays the cumulative percentage return for all selected stocks since the start of the analysis period. NVIDIA's dramatic outperformance is immediately visible, separating itself far above the cluster of other names and the S&P 500 baseline.

### Price History — Technical Analysis View
<img width="1917" height="985" alt="priceHistory" src="https://github.com/user-attachments/assets/97643d21-8306-45c9-a668-bd4b41e7bc8e" />


The Price History tab shows individual stock price action with a 50-day and 200-day moving average overlay. Users can select any stock from the dropdown. The chart enables quick identification of trend reversals and golden/death cross events.

### Trading Activity — Volume Analysis
<img width="1914" height="994" alt="tradingActivity" src="https://github.com/user-attachments/assets/c4cf7d03-11a6-42e0-a639-9953b365a6ce" />

The Trading Activity tab presents daily trading volume as a grouped bar chart across all selected stocks. Notable volume spikes around earnings periods and major macro events are visible, particularly for NVIDIA in mid-2025.

### Price Swings — 30-Day Rolling Volatility
<img width="1919" height="980" alt="priceSwings" src="https://github.com/user-attachments/assets/00b3e11f-a03c-4cbc-91e4-d47f3745e4c9" />

The Price Swings tab plots the rolling 30-day volatility for each stock. NVIDIA and Tesla consistently exhibit the highest volatility, while Apple and the S&P 500 remain the most stable throughout the period.

---

## Key Insights

The dashboard reveals several findings that would be actionable for a non-technical stakeholder.

NVIDIA was the standout performer of the period with a one-year cumulative return exceeding 163%, more than four times the S&P 500's return of 37.4%. This was driven primarily by explosive demand for AI infrastructure, with GPU revenue accelerating sharply from mid-2025 onward. A stakeholder managing a tech-tilted portfolio would be well-served to understand that this outperformance came with correspondingly higher volatility,NVIDIA's 30-day volatility regularly exceeded 4–5% compared to under 2% for Apple and the benchmark.

Microsoft and Amazon delivered modest positive returns of approximately 1% and 19% respectively over the year, significantly underperforming the sector average of 70.82%. This divergence is worth noting for any investor benchmarking against a broad technology index, as passive exposure to the sector would have captured strong average returns, but individual stock selection would have mattered substantially.

Apple and Meta showed stable but below-average performance, with Apple returning approximately 42% and Meta 37%. Both stocks demonstrated lower volatility relative to their sector peers, suggesting they served more as defensive positions within a tech allocation.

Tesla experienced significant price swings with a one-year return of approximately 115%, placing it second among individual names. However, its 30-day volatility was among the highest in the group, consistently above 2.4%, indicating that the gains came with meaningful short-term uncertainty.

The S&P 500 benchmark at 37.4% demonstrates that while the index performed well in absolute terms, every individual tech stock in this analysis either matched or exceeded it — a reminder that concentrated tech exposure has historically rewarded investors willing to tolerate sector-specific risk during periods of AI-driven growth.

**Recommendation to stakeholders:** Given the spread in risk-adjusted performance across these names, a portfolio constructed with equal weighting across all seven stocks would have generated stronger risk-adjusted returns than any single position except NVIDIA. Monitoring 30-day rolling volatility as a forward-looking risk indicator, rather than relying solely on historical returns, would provide earlier signals of changing market conditions.

---

## Live Dashboard Link

🔗 **https://stocks-analysis-dashboard.streamlit.app/**

To run locally:
```bash
pip install -r requirements.txt
python fetch_data.py
python clean_data.py
streamlit run dashboard.py
```

---

## Assumptions and Limitations

**Data freshness.** The dataset was collected at a single point in time and is not automatically refreshed. The dashboard reflects market conditions as of the last fetch date (February 13, 2026). For production use, the fetch script would need to be scheduled to run on a daily basis to maintain current data.

**Adjusted close prices.** The `yfinance` library returns adjusted closing prices that account for stock splits and dividend distributions. This means cumulative return calculations reflect total return inclusive of capital events, which is the correct basis for investment comparison but may differ from raw price charts seen on other platforms.

**Market hours and trading calendars.** The dataset uses business day data only. Non-trading days (weekends, public holidays) are absent from the date axis. Rolling calculations use actual trading days rather than calendar days, meaning a "30-day" volatility window represents approximately six calendar weeks.

**S&P 500 representation.** The S&P 500 is represented by the `^GSPC` index rather than an ETF such as SPY. Index values do not account for dividend reinvestment, so the benchmark return shown is a price return rather than a total return. This slightly understates S&P 500 performance relative to a fund that reinvests dividends.

**Survivorship bias.** The seven companies selected are among the largest and most successful technology firms by market capitalization. Including only successful companies in a retrospective analysis tends to overstate the expected returns of the sector as a whole, since failed or underperforming companies of the same period are not represented.

**Forward-looking caution.** Past performance as visualized in this dashboard does not predict future results. The analysis is descriptive and does not constitute investment advice.

---

*Data Source: Yahoo Finance via yfinance | Analysis Period: February 2024 – February 2026 |
