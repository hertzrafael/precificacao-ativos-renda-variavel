import yfinance as yf
from pandas import DataFrame, to_datetime

class Asset:

    def __init__(self, name: str, period: str = '1mo'):
        self.asset = yf.Ticker(name)
        self.history = self.asset.history(period).reset_index()
        self._transform_history()

    def get_history(self):
        return self.history

    def get_trend_price(self):
        data = (self.get_history()
                .filter(items=['date', 'open', 'close'])
                .assign(diff_percentage=lambda x: round((100 - (x['close'] * 100) / x['open']), 2) * -1)
                .assign(diff_sum=lambda x: round(x['diff_percentage'].sum(), 2))
        )

        self._add_percentage(data, columns=['diff_percentage', 'diff_sum'])
        self._round_columns(data, columns=['open', 'close'])

        return data

    def _transform_history(self):
        self.history.columns = self.history.columns.str.lower()
        self.history['date'] = to_datetime(self.history['date'].dt.strftime('%Y-%m-%d'))

    def _round_columns(self, data_frame: DataFrame, columns: list[str], decimal_places: int = 2):
        for column in columns:
            data_frame[column] = data_frame[column].map(lambda x: round(x, decimal_places))

    def _add_percentage(self, data_frame: DataFrame, columns: list[str]):
        for column in columns:
            data_frame[column] = data_frame[column].astype(str) + '%'