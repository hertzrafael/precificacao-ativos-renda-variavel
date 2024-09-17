import yfinance as yf

class Asset:

    def __init__(self, name: str):
        self.asset = yf.Ticker(name)
