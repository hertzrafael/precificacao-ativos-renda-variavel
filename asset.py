from datetime import datetime, timedelta

import yfinance as yf
from pandas import DataFrame, to_datetime

class Asset:

    def __init__(self, name: str, period: str = '1mo'):
        self.asset = yf.Ticker(name)
        self.history = self.asset.history(period, rounding=True).reset_index()
        self._transform_history(self.history)

    def get_history(self):
        return self.history

    def get_trend_price(self):
        data = (self.get_history()
                .filter(items=['date', 'open', 'close'])
                .assign(diff_percentage=lambda x: round((100 - (x['close'] * 100) / x['open']), 2) * -1)
                .assign(diff_sum=lambda x: round(x['diff_percentage'].sum(), 2))
        )
        self._add_percentage(data, columns=['diff_percentage', 'diff_sum'])

        return data

    def get_moving_mean(self, days: int = 1):
        start_date = datetime.now() - timedelta(days=days)

        history = self.asset.history(start=start_date, rounding=True).reset_index()
        self._transform_history(history)

        return (history
                .filter(items=['date', 'close'])
                .assign(mean=lambda x: round(x['close'].mean(), 2))
                .assign(above_average=lambda x: x['close'] >= x['mean'])
        )

    def _transform_history(self, history):
        history.columns = history.columns.str.lower()
        history['date'] = to_datetime(history['date'].dt.strftime('%Y-%m-%d'))

    def _add_percentage(self, data_frame: DataFrame, columns: list[str]):
        for column in columns:
            data_frame[column] = data_frame[column].astype(str) + '%'
