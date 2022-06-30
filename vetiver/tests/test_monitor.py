from sklearn import metrics
from datetime import timedelta
import pandas as pd
import numpy

import vetiver

rng = pd.date_range("1/1/2012", periods=10, freq="S")
new = dict(x=range(len(rng)), y=range(len(rng)))
df = pd.DataFrame(new, index=rng)
df.reset_index(inplace=True)
td = timedelta(seconds=2)
metric_set = [metrics.mean_squared_error, metrics.mean_absolute_error]


def test_compute():
    m = vetiver.compute_metrics(
        df, "index", td, metric_set=metric_set, truth="x", estimate="y"
    )
    assert isinstance(m, pd.DataFrame)
    assert m.shape == (10, 4)
    numpy.testing.assert_array_equal(
        m.metric.unique(),
        numpy.array(["mean_squared_error", "mean_absolute_error"], dtype=object),
    )
