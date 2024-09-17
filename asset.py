import yfinance as yf
from pandas import DataFrame

class Asset:

    def __init__(self, name: str, period: str = '1mo'):
        self.asset = yf.Ticker(name)
        self.history = self.asset.history(period).reset_index()
        self.history.columns = self.history.columns.str.lower()

    def get_history(self):
        return self.history

    def get_trend_price(self):
        data = (self.get_history()
                .filter(items=['date', 'open', 'close'])
                .assign(diff_percentage=lambda x: round((100 - (x['close'] * 100) / x['open']), 2) * -1)
        )
        data['diff_percentage'] = data['diff_percentage'].astype(str) + '%'

        self._round_columns(data, ['open', 'close'])

        return data

    # noinspection PyMethodMayBeStatic
    def _round_columns(self, data_frame: DataFrame, columns: list[str], decimal_places: int = 2):
        for column in columns:
            data_frame[column] = data_frame[column].map(lambda x: round(x, decimal_places))