import yfinance as yf, pandas as pd

tickers = ["ISF.L", "VUKE.L"]
dfs = {}
for tkr in tickers:
    tk = yf.Ticker(tkr)
    df = pd.DataFrame(tk.news)           # to DataFrame if you like
    dfs[tkr] = df[["publisher","title","link"]]

# Example: first headline for each fund
for tkr, df in dfs.items():
    if df.empty:
        print(f"{tkr}: no Yahoo news feed")
    else:
        row = df.iloc[0]
        print(f"{tkr}: {row.publisher} – {row.title}")
