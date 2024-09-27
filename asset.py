from datetime import datetime, timedelta

from yfinance import Ticker
from pandas import DataFrame, to_datetime
from numpy import datetime64

class Asset:

    def __init__(self, name: str, cache_history: bool = True, days_before: int = 30):
        self.asset = Ticker(name)
        self.cache_history = cache_history
        self.days_before = days_before
        self.history = None

    def get_history(self, days=-1):
        if days == -1 and self.cache_history:
            if self.history is not None:
                return self.history

        days = self.days_before if days == -1 else days
        start_date = datetime.now() - timedelta(days=days)
        history = self.asset.history(start=start_date, rounding=True).reset_index()
        self._transform_history(history)

        if self.cache_history:
            self.history = history

        return history

    def update_history(self):
        if not self.cache_history:
            return

        self.history = None
        self.get_history()

    def get_accumulated_return(self):
        data = (self.get_history()
                .filter(items=['date', 'close'])
                .assign(daily_return=lambda x: round(x['close'].pct_change(), 6))
        )
        data['accumulated_return'] = (1 + data['daily_return']).cumprod() - 1
        accumulated_return = round((data.tail(1)['accumulated_return']).item() * 100, 2)

        return accumulated_return, data

    def get_moving_mean(self):
        return (self.get_history()
                .filter(items=['date', 'close'])
                .assign(mean=lambda x: round(x['close'].mean(), 2))
                .assign(above_average=lambda x: x['close'] >= x['mean'])
        )

    def get_standart_deviation(self):
        return (self.get_history()
                .filter(items=['date','close'])
                .assign(standart_deviant=lambda x: x['close'].std())
        )

    def _classify_situation(self, close, superior, inferior):
        if close > superior:
            return 'Overvalued'
        elif close < inferior:
            return 'Undervalued'
        else:
            return 'Normal'

    def get_outlier_bollinger_band_check(self):
        data = self.get_history().filter(items=['date', 'open', 'close', 'volume'])
        bollinger_superior = data['close'].mean() + (2 * data['close'].std())
        bollinger_inferior = data['close'].mean() - (2 * data['close'].std())

        data['situation'] = data.apply(lambda row: self._classify_situation(row['close'], bollinger_superior, bollinger_inferior), axis=1)

        return data
    
    def get_sharpe_ratio(self):

        df = (self.get_history(days=365)
              .filter(items=['date', 'close'])
              .assign(daily_return=lambda x: round(x['close'].pct_change(), 6))
        )

        monthly_return = DataFrame(df.groupby(df['date'].dt.month)['daily_return'].sum()).reset_index()
        std = monthly_return['daily_return'].std()

        monthly_return['accumulated_return'] = (1 + monthly_return['daily_return']).cumprod() - 1
        accumulated_return = (monthly_return.tail(1)['accumulated_return']).item()

        risk_free_rate = 0.1375 

        sharpe_ratio = (accumulated_return - risk_free_rate) / std

        return round(sharpe_ratio, 2)

    def _transform_history(self, history):
        history.columns = history.columns.str.lower()

        date_object = history['date'].dtype != datetime64
        if date_object:
            history['date'] = to_datetime(history['date'])

        history['date'] = to_datetime(history['date'].dt.strftime('%Y-%m-%d'))

    def _add_percentage(self, data_frame: DataFrame, columns: list[str]):
        for column in columns:
            data_frame[column] = data_frame[column].astype(str) + '%'

    def ranking(self):
        data = self.get_outlier_bollinger_band_check()
        data_5_best = data.sort_values(by='close', ascending=False).head(5)

        data_5_worst = data.sort_values(by='close', ascending=False).tail(5)

        return data_5_best, data_5_worst, data
