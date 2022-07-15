from sklearn import metrics
from datetime import timedelta

import pandas as pd
import pins
import numpy
import time
import vetiver

import pytest

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


def test_compute_coerce_datetime():

    df_metrics = pd.DataFrame(
        {
            "index": ["2021-01-01", "2021-01-02", "2021-01-03"],
            "truth": [200, 201, 199],
            "pred": [198, 200, 199],
        }
    )
    td = timedelta(days=1)
    m = vetiver.compute_metrics(
        df_metrics, "index", td, metric_set=metric_set, truth="truth", estimate="pred"
    )
    assert isinstance(m, pd.DataFrame)
    assert m.shape == (4, 4)
    numpy.testing.assert_array_equal(
        m.metric.unique(),
        numpy.array(["mean_squared_error", "mean_absolute_error"], dtype=object),
    )


def test_monitor(snapshot):
    snapshot.snapshot_dir = "./vetiver/tests/snapshots"
    m = vetiver.compute_metrics(
        df, "index", td, metric_set=metric_set, truth="x", estimate="y"
    )
    vetiver.plot_metrics(m)
    snapshot.assert_match(m.to_json(), "test_monitor.json")


@pytest.fixture
def df_metrics_old():
    return pd.DataFrame(
        {
            "index": pd.to_datetime(["2021-01-01", "2021-01-02"]),
            "n": [1, 2],
            "metric": ["x", "x"],
            "estimate": [0.1, 0.2],
        }
    )


def test_vetiver_pin_metrics_simple(df_metrics_old):
    board = pins.board_temp()
    board.pin_write(df_metrics_old, "test_metrics", type="csv")
    time.sleep(1)

    df_metrics_new = pd.DataFrame(
        {
            "index": pd.to_datetime(["2021-01-03", "2021-01-04"]),
            "n": [3, 4],
            "metric": ["x", "x"],
            "estimate": [0.8, 0.9],
        }
    )

    df_res = vetiver.pin_metrics(board, df_metrics_new, "test_metrics")

    assert len(df_res) == 4
    assert df_res.equals(pd.concat([df_metrics_old, df_metrics_new], ignore_index=True))


def test_vetiver_pin_metrics_overlap_error(df_metrics_old):
    board = pins.board_temp()
    board.pin_write(df_metrics_old, "test_metrics", type="csv")
    time.sleep(0.1)

    with pytest.raises(ValueError) as exc_info:
        vetiver.pin_metrics(board, df_metrics_old, "test_metrics")

    assert "The new metrics overlap" in exc_info.value.args[0]


def test_vetiver_pin_metrics_overwrite(df_metrics_old):
    board = pins.board_temp()
    board.pin_write(df_metrics_old, "test_metrics", type="csv")
    time.sleep(1)

    # first row should update existing metrics
    df_metrics_new = pd.DataFrame(
        {
            "index": pd.to_datetime(["2021-01-01", "2021-01-03"]),
            "n": [200, 201],
            "metric": ["y", "y"],
            "estimate": [0.8, 0.9],
        }
    )

    df_res = vetiver.pin_metrics(board, df_metrics_new, "test_metrics", overwrite=True)
    assert len(df_res) == 3

    df_dst = pd.concat([df_metrics_old.iloc[[1], :], df_metrics_new], ignore_index=True)
    assert df_res.equals(df_dst.sort_values("index"))


def test_vetiver_pin_metrics_manual_pin_type(df_metrics_old):
    board = pins.board_temp()
    board.pin_write(df_metrics_old, "test_metrics", type="csv")
    time.sleep(1)

    df_res = vetiver.pin_metrics(
        board, df_metrics_old, "test_metrics", overwrite=True, pin_type="joblib"
    )

    assert len(df_res) == 2

    meta = board.pin_meta("test_metrics")

    assert meta.type == "joblib"
