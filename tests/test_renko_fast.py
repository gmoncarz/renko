import unittest
import pandas as pd

from renko_fast import RenkoFixBrickSize_Fast


class RenkoFixBrickSize_FastTest(unittest.TestCase):
    def setUp(self):
        self.data = pd.DataFrame({
            'price': [
                95,
                105, 95, 86,
                85, 84, 86, 76,
                74,
                65, 77,
                54,
                33, 40, 45, 50, 54,
                55, 64,
                156,
                94, 93, 92, 91, 90, 89,
            ],
            'volume': [
                1,
                2, 3, 4,
                5, 6, 7, 8,
                9,
                10, 11,
                12,
                13, 14, 15, 16, 17,
                18, 19,
                20,
                21, 22, 23, 24, 25, 26
            ],
            'date': [
                1,
                2, 3, 4,
                5, 6, 7, 8,
                9,
                10, 11,
                12,
                13, 14, 15, 16, 17,
                18, 19,
                20,
                21, 22, 23, 24, 25, 26,
            ],
        })

        self.expected_renko_prices = [
            95.0,
            105.0,
            85.0,
            75.0,
            65.0,
            55.0,
            45.0, 35.0,
            55.0, 65.0, 75.0, 85.0, 95.0, 105.0, 115.0, 125.0, 135.0, 145.0, 155.0,
            135.0, 125.0, 115.0, 105.0, 95.0
        ]

        self.expected_trend = [
            0.0,
            1.0,
            -1.0,
            -1.0,
            -1.0,
            -1.0,
            -1.0, -1.0,
            1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
            -1.0, -1.0, -1.0, -1.0, -1.0
        ]

        self.expected_performance = {
            'count': 26.0,
            'renko_bricks': 24,
            'price_to_brick_ratio': 1.0833333333333333,
            'sign_changes': 3,
            'balance': 13,
            'score': 0.13398960632476625
        }

    def test_renko_with_volume_and_dates(self):
        subject = RenkoFixBrickSize_Fast(10, 'test')
        # subject.new_quotes(self.data.price[:].tolist(), volumes=self.data.volume[:].tolist(), dates=self.data.date.tolist())
        subject.new_quotes(
            self.data.price.tolist(),
            volumes=self.data.volume.tolist(),
            dates=self.data.date.tolist(),
        )
        self.assertListEqual(subject.get_renko()[:, subject.col_price_renko].tolist(), self.expected_renko_prices)
        self.assertListEqual(subject.get_renko()[:, subject.col_trend].tolist(), self.expected_trend)

    def test_renko_performance_metrics(self):
        subject = RenkoFixBrickSize_Fast(10, 'test')
        subject.new_quotes(
            self.data.price.tolist(),
            volumes=self.data.volume.tolist(),
            dates=self.data.date.tolist()
        )

        self.assertDictEqual(subject.performance(), self.expected_performance)
        pass

    def test_renko_with_only_volume(self):
        subject = RenkoFixBrickSize_Fast(10, 'test')
        # subject.new_quotes(self.data.price[:].tolist(), volumes=self.data.volume[:].tolist(), dates=self.data.date.tolist())
        subject.new_quotes(
            self.data.price.tolist(),
            volumes=self.data.volume.tolist(),
        )

        self.assertListEqual(subject.get_renko()[:, subject.col_price_renko].tolist(), self.expected_renko_prices)
        self.assertListEqual(subject.get_renko()[:, subject.col_trend].tolist(), self.expected_trend)

    def test_renko_with_with_only_dates(self):
        subject = RenkoFixBrickSize_Fast(10, 'test')
        # subject.new_quotes(self.data.price[:].tolist(), volumes=self.data.volume[:].tolist(), dates=self.data.date.tolist())
        subject.new_quotes(
            self.data.price.tolist(),
            dates=self.data.date.tolist()
        )

        self.assertListEqual(subject.get_renko()[:, subject.col_price_renko].tolist(), self.expected_renko_prices)
        self.assertListEqual(subject.get_renko()[:, subject.col_trend].tolist(), self.expected_trend)

    def test_renko_with_with_only_quotes(self):
        subject = RenkoFixBrickSize_Fast(10, 'test')
        subject.new_quotes(self.data.price.tolist(),)

        self.assertListEqual(subject.get_renko()[:, subject.col_price_renko].tolist(), self.expected_renko_prices)
        self.assertListEqual(subject.get_renko()[:, subject.col_trend].tolist(), self.expected_trend)

    def test_dates(self):
        data = pd.DataFrame({
            'price': [
                95,
                105, 95, 86,
                85, 84, 86, 76,
                74,
                65, 77,
                54,
                33, 40, 45, 50, 54,
                55, 64,
                156,
                94, 93, 92, 91, 90, 89,
            ],
            'date': pd.date_range(pd.to_datetime('2015-01-01'), periods=26, freq='D').tolist(),
        })

        self.expected_renko_prices = [
            95.0,
            105.0,
            85.0,
            75.0,
            65.0,
            55.0,
            45.0, 35.0,
            55.0, 65.0, 75.0, 85.0, 95.0, 105.0, 115.0, 125.0, 135.0, 145.0, 155.0,
            135.0, 125.0, 115.0, 105.0, 95.0
        ]

        subject = RenkoFixBrickSize_Fast(10, 'test')
        # subject.new_quotes(self.data.price[:].tolist(), volumes=self.data.volume[:].tolist(), dates=self.data.date.tolist())
        subject.new_quotes(
            data.price.tolist(),
            dates=data.date.tolist()
        )

        self.assertListEqual(subject.get_renko()[:, subject.col_price_renko].tolist(), self.expected_renko_prices)
        self.assertListEqual(subject.get_renko()[:, subject.col_trend].tolist(), self.expected_trend)

    def test_renko_initial_size(self):
        subject = RenkoFixBrickSize_Fast(10, 'test', initial_size=1, increment_pct=1)
        subject.new_quotes(self.data.price.tolist(),)

        self.assertListEqual(subject.get_renko()[:, subject.col_price_renko].tolist(), self.expected_renko_prices)
        self.assertListEqual(subject.get_renko()[:, subject.col_trend].tolist(), self.expected_trend)


