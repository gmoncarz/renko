import unittest
import pandas as pd

from renko_fast import RenkoFixBrickSize_Fast
from renko_fast import Renko
from renko_fast import GridPrice


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

        self.expected_symetric_prices = [
            95.0,
            105.0, 95.0,
            85.0,
            75.0,
            65.0, 75.0,
            65.0, 55.0,
            45.0, 35.0, 45.0,
            55.0,
            65.0, 75.0, 85.0, 95.0, 105.0, 115.0, 125.0, 135.0, 145.0, 155.0,
            145.0, 135.0, 125.0, 115.0, 105.0, 95.0,
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

        self.expected_symetric_trend = [
            0.0,
            1.0, -1.0,
            -1.0,
            -1.0,
            -1.0, 1.0,
            -1.0, -1.0,
            -1.0, -1.0, 1.0,
            1.0,
            1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
            -1.0, -1.0, -1.0, -1.0, -1.0, -1.0,
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

    def test_renko_symetric_with_only_quotes(self):
        # subject = RenkoFixBrickSize_Fast(10, 'test', renko_type=Renko.TypeGrid)
        subject = RenkoFixBrickSize_Fast(10, 'test', renko_type=Renko.TypeRenkoSymetric)
        subject.new_quotes(self.data.price.tolist(),)

        self.assertListEqual(subject.get_renko()[:, subject.col_price_renko].tolist(), self.expected_symetric_prices)
        self.assertListEqual(subject.get_renko()[:, subject.col_trend].tolist(), self.expected_symetric_trend)

    def test_renko_grid_with_only_quotes(self):
        data = pd.DataFrame({
            'price': [
                91, 90.1, 99, 94,
                100, 100.1, 100.0, 109, 86,
                85, 84, 86, 76,
                74,
                65, 77,
                54,
                33, 45, 54,
                55, 64,
                100,
                100.0001,
                94, 93, 92, 91, 90, 89,
            ],
        })

        expected_grid_avg_prices = [
            95.0,
            105.0, 95.0, 85.0,
            75,

            65, 75,
            65, 55,
            45, 35, 45, 55,
            65,
            75, 85,95,

            105,
            95, 85,
        ]

        expected_grid_min_prices = [
            90.0,
            100.0, 90.0, 80.0,
            70,

            60, 70,
            60, 50,
            40, 30, 40, 50,
            60,
            70, 80, 90,

            100,
            90, 80,
        ]

        expected_grid_max_prices = [
            100.0,
            110.0, 100.0, 90.0,
            80,

            70, 80,
            70, 60,
            50, 40, 50, 60,
            70,
            80, 90, 100,

            110,
            100, 90,
        ]

        expected_grid_trend = [
            0,
            1, -1, -1,
            -1,

            -1, 1,
            -1, -1,
            -1, -1, 1, 1,
            1,
            1, 1, 1,
            1,
            -1, -1,
        ]

        subject_avg = RenkoFixBrickSize_Fast(10, 'test', renko_type=Renko.TypeGrid, grid_price = GridPrice.AVG)
        subject_avg.new_quotes(data.price.tolist(),)

        self.assertListEqual(subject_avg.get_renko()[:, subject_avg.col_price_renko].tolist(), expected_grid_avg_prices)
        self.assertListEqual(subject_avg.get_renko()[:, subject_avg.col_trend].tolist(), expected_grid_trend)

        subject_min = RenkoFixBrickSize_Fast(10, 'test', renko_type=Renko.TypeGrid, grid_price = GridPrice.MIN)
        subject_min.new_quotes(data.price.tolist(),)

        self.assertListEqual(subject_min.get_renko()[:, subject_min.col_price_renko].tolist(), expected_grid_min_prices)
        self.assertListEqual(subject_min.get_renko()[:, subject_min.col_trend].tolist(), expected_grid_trend)

        subject_max = RenkoFixBrickSize_Fast(10, 'test', renko_type=Renko.TypeGrid, grid_price = GridPrice.MAX)
        subject_max.new_quotes(data.price.tolist(),)

        self.assertListEqual(subject_max.get_renko()[:, subject_max.col_price_renko].tolist(), expected_grid_max_prices)
        self.assertListEqual(subject_max.get_renko()[:, subject_max.col_trend].tolist(), expected_grid_trend)


    def test_renko_grid_thresholds(self):
        data = [
            91, 90, 99, 100, 90, 100,
            100.001,
            100, 110, 100, 110,
            99.9999,
            59.99,
            60, 50, 60, 50,
        ]

        expected_grid_avg_prices = [
            95.0, 95, 95, 95, 95, 95,
            105,
            105, 105, 105, 105,
            95,
            55,
            55, 55, 55, 55,
        ]

        expected_grid_min_prices = [
            90.0, 90, 90, 90, 90, 90,
            100,
            100, 100, 100, 100,
            90,
            50,
            50, 50, 50, 50,
        ]

        expected_grid_max_prices = [
            100.0, 100, 100, 100, 100, 100,
            110,
            110, 110, 110, 110,
            100,
            60,
            60, 60, 60, 60,
        ]

        expected_grid_trend = [
            0, 0, 0, 0, 0, 0,
            1,
            1, 1, 1, 1,
            -1,
            -1,
            -1, -1, -1, -1,
        ]


        subject_avg = RenkoFixBrickSize_Fast(10, 'test', renko_type=Renko.TypeGrid, grid_price = GridPrice.AVG)
        subject_min = RenkoFixBrickSize_Fast(10, 'test', renko_type=Renko.TypeGrid, grid_price = GridPrice.MIN)
        subject_max = RenkoFixBrickSize_Fast(10, 'test', renko_type=Renko.TypeGrid, grid_price = GridPrice.MAX)

        # Evaluate step by step
        for index, quote in enumerate(data):
            subject_avg.new_quotes([quote])
            subject_min.new_quotes([quote])
            subject_max.new_quotes([quote])

            self.assertEqual(subject_avg.get_renko()[:, subject_avg.col_price_renko][-1], expected_grid_avg_prices[index])
            self.assertEqual(subject_min.get_renko()[:, subject_min.col_price_renko][-1], expected_grid_min_prices[index])
            self.assertEqual(subject_max.get_renko()[:, subject_max.col_price_renko][-1], expected_grid_max_prices[index])

            self.assertEqual(subject_avg.get_renko()[:, subject_avg.col_trend][-1], expected_grid_trend[index])
            self.assertEqual(subject_min.get_renko()[:, subject_min.col_trend][-1], expected_grid_trend[index])
            self.assertEqual(subject_max.get_renko()[:, subject_max.col_trend][-1], expected_grid_trend[index])
