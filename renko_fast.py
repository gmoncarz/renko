import datetime
import calendar

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

'''
Renko library optimized for Reinforcement Learning.

This library transform any stock market quote to Renko bricks. The main feature
is that it was developed to work fast, to be possible to use it
in a reinforcement learning models. The profiling tests show that a
reinforcement learning agent that use this library, spends only 1.87% of the
time transforming quotes to Renko, while the remaining 98.13% is training
the model.

This library is still on development.
'''


class Renko():
    def __init__(self, name=None):
        self.name = name


class RenkoFixBrickSize_Fast(Renko):
    '''Fix Brick Renko with fast execution'''

    # Columns that return renko's brick and status
    col_price_last = 0
    col_price_renko = 1
    col_price_min = 2
    col_price_max = 3
    col_dt_start = 4
    col_dt_end = 5
    col_trend = 6
    col_volume = 7
    col_count = 8
    col_cons_up = 9
    col_cons_down = 10

    as_dataframe_colnames = [
        'price_last',
        'price_renko',
        'price_min',
        'price_max',
        'dt_start',
        'dt_end',
        'trend',
        'volume',
        'count',
        'cons_up',
        'cons_down',
    ]

    AS_NUMPY = 'numpy'
    AS_DATAFRAME = 'dataframe'

    def __init__(self, brick_size, name=None, initial_size=10000, increment_pct=.5):
        '''Renko Constructor

        :param brick_size: fix size of the Renko brick
        :type brick_size: int or float
        :param name: Renko name
        :type name: str
        :param initial_size: initial size of the numpy main structure that stores
            the renko bricks. The higher, less time is spend resizing the
            internal structure, but more memory is consumed.
        :type initial_size: int
        :param increment_pct: The percentage of increase of the internal
            numpy data structure that stores Renko's bricks, when it needs
            to be resized.
        :type increment_pct: float
        '''
        Renko.__init__(self, name)

        self.brick_size = float(brick_size)
        self.initial_size = initial_size
        self.increment_pct = increment_pct

        self._renko = np.zeros([self.initial_size, 11])
        self._index = -1

    def _initial_brick(self, price, date, volume):
        '''Stores the first renko brick'''
        (brick_lower_limit, brick_upper_limit) = (price - self.brick_size, price + self.brick_size)

        new_brick = [
            price,                  # price_last
            price,                  # price_renko
            brick_lower_limit,      # price_min
            brick_upper_limit,      # price_max
            np.nan,                 # dt_start
            np.nan,                 # dt_end
            0,                      # trend
            np.nan,                 # volume
            1,                      # count
            0,                      # cons_up
            0,                      # cons_down
        ]

        # Add optional info
        if date is not None:
            new_brick[self.col_dt_start] = date
            new_brick[self.col_dt_end] = date
        if volume is not None:
            new_brick[self.col_volume] = volume

        self._index = 0
        self._renko[self._index] = new_brick

        return

    def _new_brick(self, price, date, volume):
        '''Add a new Renko Brick'''
        while True:
            last_brick = self._renko[self._index]

            if price >= last_brick[self.col_price_max]:
                cons_down = 0
                if last_brick[self.col_trend] < 0:
                    multiplier = 2
                    cons_up = 1
                else:
                    multiplier = 1
                    cons_up = last_brick[self.col_cons_up] + 1

                new_price_renko = last_brick[self.col_price_renko] + multiplier * self.brick_size
                brick_upper_limit = new_price_renko + self.brick_size
                brick_lower_limit = new_price_renko - 2 * self.brick_size
                new_trend = 1

            elif price <= last_brick[self.col_price_min]:

                cons_up = 0
                if last_brick[self.col_trend] > 0:
                    multiplier = 2
                    cons_down = 1
                else:
                    multiplier = 1
                    cons_down = last_brick[self.col_cons_down] + 1

                new_price_renko = last_brick[self.col_price_renko] - multiplier * self.brick_size
                brick_upper_limit = new_price_renko + 2 * self.brick_size
                brick_lower_limit = new_price_renko - self.brick_size
                new_trend = -1
            else:
                last_brick[self.col_count] = 1
                if volume is not None:
                    last_brick[self.col_volume] = volume

                break

            new_brick = [
                price,                  # price_last
                new_price_renko,                  # price_renko
                brick_lower_limit,      # price_min
                brick_upper_limit,      # price_max
                np.nan,                 # dt_start
                np.nan,                 # dt_end
                new_trend,              # trend
                0,                      # volume
                0,                      # count
                cons_up,                # cons_up
                cons_down,              # cons_down
            ]

            # Add optional info
            if date is not None:
                new_brick[self.col_dt_start] = date
                new_brick[self.col_dt_end] = date

            try:
                self._index += 1
                self._renko[self._index] = new_brick
            except IndexError as e:
                # Extend the renko numpy array
                old_rows, old_columns = self._renko.shape
                new_rows  = int(old_rows * ( self.increment_pct))
                if new_rows < 1:
                    new_rows = 100

                new_empty_renko = np.empty((new_rows, old_columns),
                                           dtype=self._renko.dtype)
                self._renko = np.concatenate((self._renko, new_empty_renko))

                # Store the new brick
                self._renko[self._index] = new_brick

                pass

    def new_quotes(self, prices, dates=None, volumes=None):
        '''Set a new underlying quote

        :param prices: list of the prices  to convert to Renko
        :type prices: list of float
        :param dates: date of the quotes
        :type dates: list of int, pandasd.Timestamp or datetime.date
        :param volumes: Volume of the underlying quote
        :type volumes: list of int or float
        '''
        if dates is None:
            dates = [None] * len(prices)
        else:
            dates = [self._convert_dates_to_timestamp(date) for date in dates]
        if volumes is None:
            volumes = [None] * len(prices)

        if self._index == -1:
            self._initial_brick(prices[0], dates[0], volumes[0])
            return self.new_quotes(prices[1:], dates[1:], volumes[1:])

        for (price, date, volume) in zip(prices, dates, volumes):
            last_brick = self._renko[self._index]

            if price >= last_brick[self.col_price_max]:
                if date is not None:
                    last_brick[self.col_dt_end] = date
                self._new_brick(price, date, volume)
            elif price <= last_brick[self.col_price_min]:
                if date is not None:
                    last_brick[self.col_dt_end] = date
                self._new_brick(price, date, volume)
            else:
                # The quote is in the same renko brick
                last_brick[self.col_price_last] = price
                last_brick[self.col_count] += 1
                if date is not None:
                    last_brick[self.col_dt_end] = date
                if volume is not None:
                    last_brick[self.col_volume] += volume

        pass

    def get_renko(self, ret_type=AS_NUMPY):
        '''Return a renko representation

        :param ret_type: representation to return. Could have the following
            possibilities:
            - self.AS_NUMPY: returns a numpy structure, where each column
                has a different meaning. It is the fastest approach.
            - self.AS_DATAFRAME: returns a Pandas.DataFrame, which is more
                friendly and easy to process, but slower. Avoid this method
                on Reinforcement Learning.
        :type ret_type: str
        '''
        if ret_type == self.AS_NUMPY:
            ret = self._renko[:self._index + 1]
        elif ret_type == self.AS_DATAFRAME:
            ret = pd.DataFrame(
                self._renko[:self._index + 1],
                columns=[self.as_dataframe_colnames]
            )

        return ret

    def performance(self):
        '''
        Some performance metrics that could be useful to evaluate in a
        Reinforcement Learning model. This function should be extended
        by the user.
        :return: dictionary with the following keys:
            - count: count of underlying quotes
            - renko_bricks: count of renko bricks
            - price_to_brick_ratio: Average density of the Renko bricks
            - sign_changes: amount of trend changes
            - balance: scoring function
            - score: scoring function
        '''
        renko = self.get_renko()

        count = renko[:, self.col_count].sum()
        renko_bricks = self._index + 1

        try:
            price_to_brick_ratio = count / renko_bricks
        except ZeroDivisionError:
            price_to_brick_ratio = 0

        trend = renko[:, self.col_trend]
        sign_changes = (trend != self._shift(trend, 1)).sum() - 2
        if sign_changes < 0:
            sign_changes = 0

        equal_trend = trend[2:] == trend[1:-1]
        equal_trend_true = equal_trend.sum()
        equal_trend_false = equal_trend.shape[0] - equal_trend_true
        balance = 1 * equal_trend_true - 2 * equal_trend_false

        if sign_changes == 0:
            score = balance
        else:
            score = balance / sign_changes

        if score >= 0 and price_to_brick_ratio >= 1:
            score = np.log(score + 1) * np.log(price_to_brick_ratio)
        else:
            score = -1.0

        ret = {
            'count': count,
            'renko_bricks': renko_bricks,
            'price_to_brick_ratio': price_to_brick_ratio,
            'sign_changes': sign_changes,
            'balance': balance,
            'score': score,
        }

        return ret

    def graph(self, col_up='green', col_down='red'):
        '''Draw a Renko representation'''

        fig, ax = plt.subplots(1, figsize=(20, 10))
        ax.set_title('Renko chart')
        ax.set_xlabel('Renko bars')
        ax.set_ylabel('Price')

        renko = self.get_renko()
        renko_prices = renko[:, self.col_price_renko]
        renko_trends = renko[:, self.col_trend]

        # Calculate the limits of axes
        ax.set_xlim(0.0, len(renko_prices) + 1.0)

        if renko.shape[0] > 0:
            ax.set_ylim(np.min(renko_prices) - 3.0 * self.brick_size,
                        np.max(renko_prices) + 3.0 * self.brick_size)

        # Plot each renko bar
        for index in range(1, len(renko_prices)):
            # Set basic params for patch rectangle
            col = col_up if renko_trends[index] == 1 else col_down
            x = index
            y = renko_prices[index] - self.brick_size \
                if renko_trends[index] == 1 else renko_prices[index]

            # Draw bar with params
            ax.add_patch(patches.Rectangle(
                (x, y),   # (x,y)
                1.0,     # width
                self.brick_size, # height
                facecolor = col,
            ))

        plt.show()

    def _convert_dates_to_timestamp(self, date):
        if date is None:
            ret = None
        elif isinstance(date, float) or isinstance(date, int):
            ret = date
        elif isinstance(date, pd.Timestamp):
            ret = date.timestamp()
        elif isinstance(date, datetime.date):
            ret = calendar.timegm(date.timetuple())
        else:
            raise Exception('Date class not supported')

        return ret

    def _shift(self, arr, num, fill_value=np.nan):
        '''https://stackoverflow.com/questions/30399534/shift-elements-in-a-numpy-array'''

        result = np.empty_like(arr)
        if num > 0:
            result[:num] = fill_value
            result[num:] = arr[:-num]
        elif num < 0:
            result[num:] = fill_value
            result[:num] = arr[-num:]
        else:
            result[:] = arr

        return result
