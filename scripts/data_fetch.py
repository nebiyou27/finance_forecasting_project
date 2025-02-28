import yfinance as yf

def fetch_data(ticker, start, end):
    data = yf.download(ticker, start=start, end=end)
    return data
