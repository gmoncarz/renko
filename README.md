# Renko

Renko library that transforms stock market prices to Renko bricks. This library has two
current implementations. One is a user friendly class, which is easy to use, and another
which is much more efficient in CPU, ideal for reinfocement learning, but not as
friendly.

```python
In [1]: from renko_fast import RenkoFixBrickSize_Fast

In [2]: renko = RenkoFixBrickSize_Fast(10)

In [3]: renko.new_quotes([95])

In [4]: renko.new_quotes([105, 95, 86, 85])
   ...: renko.new_quotes([84, 86, 76, 74, 65, 77, 54, 33, 40, 45])
   ...: renko.new_quotes([50, 54, 55, 64, 156, 94, 93, 92, 91, 90, 89])

In [5]: renko.get_renko()
Out[5]:
array([[ 95.,  95.,  85., 105.,  nan,  nan,   0.,  nan,   1.,   0.,   0.],
       [ 86., 105.,  85., 115.,  nan,  nan,   1.,   0.,   3.,   1.,   0.],
       [ 76.,  85.,  75., 105.,  nan,  nan,  -1.,   0.,   4.,   0.,   1.],
       [ 74.,  75.,  65.,  95.,  nan,  nan,  -1.,   0.,   1.,   0.,   2.],
       [ 77.,  65.,  55.,  85.,  nan,  nan,  -1.,   0.,   2.,   0.,   3.],
       [ 54.,  55.,  45.,  75.,  nan,  nan,  -1.,   0.,   1.,   0.,   4.],
       [ 33.,  45.,  35.,  65.,  nan,  nan,  -1.,   0.,   0.,   0.,   5.],
       [ 54.,  35.,  25.,  55.,  nan,  nan,  -1.,   0.,   5.,   0.,   6.],
       [ 64.,  55.,  35.,  65.,  nan,  nan,   1.,   0.,   2.,   1.,   0.],
       [156.,  65.,  45.,  75.,  nan,  nan,   1.,   0.,   0.,   2.,   0.],
       [156.,  75.,  55.,  85.,  nan,  nan,   1.,   0.,   0.,   3.,   0.],
       [156.,  85.,  65.,  95.,  nan,  nan,   1.,   0.,   0.,   4.,   0.],
       [156.,  95.,  75., 105.,  nan,  nan,   1.,   0.,   0.,   5.,   0.],
       [156., 105.,  85., 115.,  nan,  nan,   1.,   0.,   0.,   6.,   0.],
       [156., 115.,  95., 125.,  nan,  nan,   1.,   0.,   0.,   7.,   0.],
       [156., 125., 105., 135.,  nan,  nan,   1.,   0.,   0.,   8.,   0.],
       [156., 135., 115., 145.,  nan,  nan,   1.,   0.,   0.,   9.,   0.],
       [156., 145., 125., 155.,  nan,  nan,   1.,   0.,   0.,  10.,   0.],
       [156., 155., 135., 165.,  nan,  nan,   1.,   0.,   1.,  11.,   0.],
       [ 94., 135., 125., 155.,  nan,  nan,  -1.,   0.,   0.,   0.,   1.],
       [ 94., 125., 115., 145.,  nan,  nan,  -1.,   0.,   0.,   0.,   2.],
       [ 94., 115., 105., 135.,  nan,  nan,  -1.,   0.,   0.,   0.,   3.],
       [ 94., 105.,  95., 125.,  nan,  nan,  -1.,   0.,   0.,   0.,   4.],
       [ 89.,  95.,  85., 115.,  nan,  nan,  -1.,   0.,   6.,   0.,   5.]])

In [6]: renko.get_renko(renko.AS_DATAFRAME)
Out[6]:
   price_last price_renko price_min price_max dt_start dt_end trend volume count cons_up cons_down
0        95.0        95.0      85.0     105.0      NaN    NaN   0.0    NaN   1.0     0.0       0.0
1        86.0       105.0      85.0     115.0      NaN    NaN   1.0    0.0   3.0     1.0       0.0
2        76.0        85.0      75.0     105.0      NaN    NaN  -1.0    0.0   4.0     0.0       1.0
3        74.0        75.0      65.0      95.0      NaN    NaN  -1.0    0.0   1.0     0.0       2.0
4        77.0        65.0      55.0      85.0      NaN    NaN  -1.0    0.0   2.0     0.0       3.0
5        54.0        55.0      45.0      75.0      NaN    NaN  -1.0    0.0   1.0     0.0       4.0
6        33.0        45.0      35.0      65.0      NaN    NaN  -1.0    0.0   0.0     0.0       5.0
7        54.0        35.0      25.0      55.0      NaN    NaN  -1.0    0.0   5.0     0.0       6.0
8        64.0        55.0      35.0      65.0      NaN    NaN   1.0    0.0   2.0     1.0       0.0
9       156.0        65.0      45.0      75.0      NaN    NaN   1.0    0.0   0.0     2.0       0.0
10      156.0        75.0      55.0      85.0      NaN    NaN   1.0    0.0   0.0     3.0       0.0
11      156.0        85.0      65.0      95.0      NaN    NaN   1.0    0.0   0.0     4.0       0.0
12      156.0        95.0      75.0     105.0      NaN    NaN   1.0    0.0   0.0     5.0       0.0
13      156.0       105.0      85.0     115.0      NaN    NaN   1.0    0.0   0.0     6.0       0.0
14      156.0       115.0      95.0     125.0      NaN    NaN   1.0    0.0   0.0     7.0       0.0
15      156.0       125.0     105.0     135.0      NaN    NaN   1.0    0.0   0.0     8.0       0.0
16      156.0       135.0     115.0     145.0      NaN    NaN   1.0    0.0   0.0     9.0       0.0
17      156.0       145.0     125.0     155.0      NaN    NaN   1.0    0.0   0.0    10.0       0.0
18      156.0       155.0     135.0     165.0      NaN    NaN   1.0    0.0   1.0    11.0       0.0
19       94.0       135.0     125.0     155.0      NaN    NaN  -1.0    0.0   0.0     0.0       1.0
20       94.0       125.0     115.0     145.0      NaN    NaN  -1.0    0.0   0.0     0.0       2.0
21       94.0       115.0     105.0     135.0      NaN    NaN  -1.0    0.0   0.0     0.0       3.0
22       94.0       105.0      95.0     125.0      NaN    NaN  -1.0    0.0   0.0     0.0       4.0
23       89.0        95.0      85.0     115.0      NaN    NaN  -1.0    0.0   6.0     0.0       5.0

In [7]: renko.graph()
```

<img src="docs/\_static/img/renko_readme_chart.png" width="100%"/>
