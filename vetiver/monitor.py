import datetime
import pins
from pins.errors import PinsError
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta


def compute_metrics(
    data: pd.DataFrame,
    date_var: str,
    period: timedelta,
    metric_set: list,
    truth: str,
    estimate: str,
) -> pd.DataFrame:
    """
    Compute metrics for given time period

    Parameters
    ----------
    data : DataFrame
        Pandas dataframe
    date_var:
        Column in `data` containing dates
    period: datetime.timedelta
        Defining period to group by
    metric_set: list
        List of metrics to compute, that have the parameters `y_true` and `y_pred`
    truth:
        Column name for true results
    estimate:
        Column name for predicted results

    Example
    -------
    from sklearn import metrics
    rng = pd.date_range("1/1/2012", periods=10, freq="S")
    new = dict(x=range(len(rng)), y = range(len(rng)))
    df = pd.DataFrame(new, index = rng).reset_index(inplace=True)
    td = timedelta(seconds = 2)
    metric_set = [sklearn.metrics.mean_squared_error, sklearn.metrics.mean_absolute_error]
    compute_metrics(df, "index", td, metric_set=metric_set, truth="x", estimate="y")

    """

    df = data[[truth, estimate, date_var]].set_index(date_var).sort_index()
    lst = [_ for _ in _rolling_df(df=df, td=period)]

    rows = []
    for i in lst:
        for m in metric_set:
            rows = rows + [
                {
                    "index": i.index[0],
                    "n": len(i),
                    "metric": m.__qualname__,
                    "estimate": m(y_pred=i[truth], y_true=i[estimate]),
                }
            ]

    outdf = pd.DataFrame.from_dict(rows)

    return outdf


def _rolling_df(df: pd.DataFrame, td: timedelta):
    first = df.index[0]
    last = df.index[-1]

    while first < last:
        stop = first + td
        boolidx = (first <= df.index) & (df.index < stop)
        yield df[boolidx].copy()
        first = stop


def pin_metrics(board, df_metrics, metrics_pin_name, overwrite=False):
    pass


#     """
#     Update an existing pin storing model metrics over time

#     Parameters
#     ----------
#     board :
#         Pins board
#     df_metrics: pd.DataFrame
#         Dataframe of metrics over time, such as created by `vetiver_compute_metrics()`
#     metrics_pin_name:
#         Pin name for where the metrics are stored
#     overwrite: bool
#         If TRUE (the default), overwrite any metrics for
#         dates that exist both in the existing pin and
#         new metrics with the new values. If FALSE, error
#         when the new metrics contain overlapping dates with
#         the existing pin.
#     """
#     date_types = (datetime.date, datetime.time, datetime.datetime)
#     if not isinstance(df_metrics.index, date_types):
#         try:
#             df_metrics = df_metrics.index.astype("datetime")
#         except TypeError:
#             raise TypeError(f"Index of {df_metrics} must be a date type")

#     new_metrics = df_metrics.sort_index()

#     new_dates = df_metrics.index.unique()

#     try:
#         old_metrics = board.pin_read(metrics_pin_name)
#     except PinsError:
#         board.pin_write(metrics_pin_name)

#     overlapping_dates = old_metrics.index in new_dates

#     if overwrite is True:
#         old_metrics = old_metrics not in overlapping_dates
#     else:
#         if overlapping_dates:
#             raise ValueError(
#                 f"The new metrics overlap with dates \
#                      already stored in {repr(metrics_pin_name)} \
#                      Check the aggregated dates or use `overwrite = True`"
#             )

#     new_metrics = old_metrics + df_metrics
#     new_metrics = new_metrics.sort_index()

#     pins.pin_write(board, new_metrics, metrics_pin_name)


def plot_metrics(
    df_metrics, date="index", estimate="estimate", metric="metric", n="n", **kw
) -> px.line:
    """
    Plot metrics over a given time period

    Parameters
    ----------
    df_metrics : DataFrame
        Pandas dataframe of metrics over time, such as created by `compute_metircs()`
    date: str
        Column in `df_metrics` containing dates
    estimate: str
        Column in `df_metrics` containing metric output
    metric: str
       Column in `df_metrics` containing metric name
    n: str
        Column in `df_metrics` containing number of observations
    """

    fig = px.line(
        df_metrics,
        x=date,
        y=estimate,
        color=metric,
        facet_row=metric,
        markers=dict(size=n),
        hover_data={"n": ':'},
        **kw,
    )

    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig.update_layout(showlegend=False)

    return fig
