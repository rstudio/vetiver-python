from typing import List
from sklearn import metrics
from datetime import timedelta
import pandas as pd
import numpy
import vetiver

rng = pd.date_range("1/1/2012", periods=10, freq="S")
new = dict(x=range(len(rng)), y=range(len(rng)))
df = pd.DataFrame(new, index=rng)
td = timedelta(seconds=2)
metric_set = [metrics.mean_squared_error, metrics.mean_absolute_error]

def test_rolling():
    m = [_ for _ in vetiver._rolling_df(df, td)]
    assert len(m) == 5
    assert len(m[0]) == 2

def test_compute():
    df.reset_index(inplace=True)
    m = vetiver.compute_metrics(
        df, "index", td, metric_set=metric_set, truth="x", estimate="y"
    )
    assert isinstance(m, pd.DataFrame)
    assert m.shape == (10, 4)
    numpy.testing.assert_array_equal(
        m.metric.unique(),
        numpy.array(["mean_squared_error", "mean_absolute_error"], dtype=object),
    )

def test_monitor(snapshot):
    snapshot.snapshot_dir = './snapshots'
    m = vetiver.compute_metrics(
        df, "index", td, metric_set=metric_set, truth="x", estimate="y"
    )
    vetiver.plot_metrics(m)
    snapshot.assert_match(m.to_json(), 'test_monitor.json')