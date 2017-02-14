import pandas as pd


class Renko():
    def __init__(self, name=None):
        self.name = name


class RenkoFixBrickSize(Renko):
    def __init__(self, brick_size, name=None):
        Renko.__init__(self, name)
        self.brick_size = brick_size
        self._df = pd.DataFrame(
            columns=['price_last', 'price_min', 'price_max',
                     'dt_start', 'dt_end', 'trend',
                     'volume'],
            dtype='int64',
        )
        self._df[['trend']] = self._df[['trend']].astype(int)
        self._df[['price_last', 'price_min', 'price_max', 'volume']] = self._df[
            ['price_last', 'price_min', 'price_max', 'volume']].astype(float)
        self._df[['dt_start', 'dt_end']] = self._df[
            ['dt_start', 'dt_end']].astype('datetime64')

        # import ipdb; ipdb.set_trace()

    def _brick_limits(self, price_ref):
        brick_size = float(self.brick_size)

        min = int(price_ref / self.brick_size) * brick_size
        max = min + brick_size

        return (min, max)


    def _new_brick(self, price, date, volume):
        (brick_lower_limit, brick_upper_limit) = self._brick_limits(price)

        new_brick = {
            'price_last': price,
            'price_min': brick_lower_limit,
            'price_max': brick_upper_limit,
        }

        # Add optional info
        if date is not None:
            new_brick['dt_start'] = date
        if volume is not None:
            new_brick['volume'] = volume

        self._df = self._df.append(new_brick, ignore_index=True)

    def new_quotes(self, prices, dates=None, volumes=None):
        if dates is None:
            dates = [None] * len(prices)
        if volumes is None:
            volumes = [None] * len(prices)

        if len(self._df) == 0:
            self._new_brick(prices[0], dates[0], volumes[0])
            self._df.loc[self._df.index[-1], 'trend'] = 0
            return self.new_quotes(prices[1:], dates[1:], volumes[1:])

        for (price, date, volume) in zip(prices, dates, volumes):
            last_brick = self._df.iloc[-1]

            if price >= last_brick.price_max:
                self._new_brick(price, date, volume)
                self._df.loc[self._df.index[-1], 'trend'] = 1
                pass
            elif price <= last_brick.price_min:
                self._new_brick(price, date, volume)
                self._df.loc[self._df.index[-1], 'trend'] = -1
                pass
            else:
                # The quote is in the same renko brick
                self._df.loc[self._df.index[-1], 'price_last'] = price
        pass
