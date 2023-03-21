import plotly.express as px
import pandas as pd
import numpy as np
from datetime import timedelta


def compute_metrics(
    data: pd.DataFrame,
    date_var: str,
    period: timedelta,
    metric_set: list,
    truth: str,
    estimate: str,
    **kw,
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

    Examples
    -------
    >>> from datetime import timedelta
    >>> import pandas as pd
    >>> from sklearn.metrics import mean_squared_error, mean_absolute_error
    >>> df = pd.DataFrame(
    ...   {
    ...        "index": ["2021-01-01", "2021-01-02", "2021-01-03"],
    ...        "truth": [200, 201, 199],
    ...        "pred": [198, 200, 199],
    ...   }
    ... )
    >>> td = timedelta(days = 1)
    >>> metric_set = [mean_squared_error, mean_absolute_error]
    >>> metrics = compute_metrics(df, "index", td, metric_set, "truth", "pred")

    """

    df = data[[truth, estimate, date_var]].copy()

    if not np.issubdtype(df[date_var], np.datetime64):
        df[date_var] = pd.to_datetime(df[date_var])

    df = df.set_index(date_var).sort_index()
    lst = [_ for _ in _rolling_df(df=df, td=period)]

    rows = []
    for i in lst:
        for m in metric_set:
            rows = rows + [
                {
                    "index": i.index[0],
                    "n": len(i),
                    "metric": m.__qualname__,
                    # TODO: non-y_pred and y_true metrics
                    # TODO: multioutput metrics
                    "estimate": m(y_pred=i[estimate], y_true=i[truth], **kw),
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


def pin_metrics(
    board,
    df_metrics: pd.DataFrame,
    metrics_pin_name: str,
    pin_type: "str | None" = None,
    index_name: str = "index",
    overwrite: bool = False,
) -> pd.DataFrame:
    """
    Update an existing pin storing model metrics over time

    Parameters
    ----------
    board :
        Pins board
    df_metrics: pd.DataFrame
        Dataframe of metrics over time, such as created by `vetiver_compute_metrics()`
    metrics_pin_name:
        Pin name for where the metrics are stored
    index_name:
        The column in df_metrics containing the aggregated dates or datetimes.
        Note that this defaults to a column named "index".
    overwrite: bool
        If True, overwrite any metrics for dates that exist both
        in the existing pin and new metrics with the new values.
        If False, error when the new metrics contain overlapping dates with
        the existing pin.

    Examples
    -------
    >>> import pins
    >>> import vetiver
    >>> df = pd.DataFrame(
    ... {'index': {0: pd.Timestamp('2021-01-01 00:00:00'),
    ...            1: pd.Timestamp('2021-01-01 00:00:00'),
    ...            2: pd.Timestamp('2021-01-02 00:00:00'),
    ...            3: pd.Timestamp('2021-01-02 00:00:00')},
    ...  'n': {0: 1, 1: 1, 2: 1, 3: 1},
    ...  'metric': {0: 'mean_squared_error',
    ...             1: 'mean_absolute_error',
    ...             2: 'mean_squared_error',
    ...             3: 'mean_absolute_error'},
    ...  'estimate': {0: 4.0, 1: 2.0, 2: 1.0, 3: 1.0}}
    ... )
    >>> board = pins.board_temp()

    >>> board.pin_write(df, "metrics", type = "csv") # doctest: +SKIP
    >>> df = pd.DataFrame(
    ... {'index': {0: pd.Timestamp('2021-01-02 00:00:00'),
    ...            1: pd.Timestamp('2021-01-02 00:00:00'),
    ...            2: pd.Timestamp('2021-01-03 00:00:00'),
    ...            3: pd.Timestamp('2021-01-03 00:00:00')},
    ...  'n': {0: 1, 1: 1, 2: 1, 3: 1},
    ...  'metric': {0: 'mean_squared_error',
    ...             1: 'mean_absolute_error',
    ...             2: 'mean_squared_error',
    ...             3: 'mean_absolute_error'},
    ...  'estimate': {0: 4.0, 1: 6.0, 2: 2.0, 3: 1.0}}
    ... )
    >>> vetiver.pin_metrics(     # doctest: +SKIP
    ...    board=board,
    ...    df_metrics=df2,
    ...    metrics_pin_name="metrics",
    ...    index_name="index",
    ...    overwrite=True)


    """

    old_metrics_raw = board.pin_read(metrics_pin_name)

    # need to coerce date index to a datetime, since pandas does not infer
    # date columns from CSV (but note that formats like arrow do)
    old_metrics = old_metrics_raw.copy()
    old_metrics[index_name] = pd.to_datetime(old_metrics[index_name])

    # handle overlapping dates ----
    dt_new = pd.to_datetime(df_metrics[index_name])
    dt_old = old_metrics[index_name]

    indx_old_overlap = dt_old.isin(dt_new)

    if overwrite:
        # get only rows specific to old metrics, so when we concat below
        # it effectively is an upsert
        old_metrics = old_metrics.loc[~indx_old_overlap, :]

    elif not overwrite and indx_old_overlap.any():
        raise ValueError(
            f"The new metrics overlap with dates already stored in {metrics_pin_name}."
            " Check the aggregated dates or use `overwrite=True`."
        )

    # update and pin ----
    combined_metrics = pd.concat([old_metrics, df_metrics], ignore_index=True)
    sorted_metrics = combined_metrics.sort_values(index_name)

    if pin_type is None:
        meta = board.pin_meta(metrics_pin_name)

        final_pin_type = meta.type
    else:
        final_pin_type = pin_type

    board.pin_write(sorted_metrics, metrics_pin_name, type=final_pin_type)

    return sorted_metrics


def plot_metrics(
    df_metrics, date="index", estimate="estimate", metric="metric", n="n", **kw
) -> px.line:
    """
    Plot metrics over a given time period

    Parameters
    ----------
    df_metrics : DataFrame
         Pandas dataframe of metrics over time, such as created by `compute_metrics()`
    date: str
         Column in `df_metrics` containing dates
    estimate: str
         Column in `df_metrics` containing metric output
    metric: str
         Column in `df_metrics` containing metric name
    n: str
         Column in `df_metrics` containing number of observations

    Examples
    -------
    >>> import vetiver
    >>> import pandas as pd
    >>> df = pd.DataFrame(
    ... {'index': {0: pd.Timestamp('2021-01-01 00:00:00'),
    ...            1: pd.Timestamp('2021-01-01 00:00:00'),
    ...            2: pd.Timestamp('2021-01-02 00:00:00'),
    ...            3: pd.Timestamp('2021-01-02 00:00:00')},
    ...  'n': {0: 1, 1: 1, 2: 1, 3: 1},
    ...  'metric': {0: 'mean_squared_error',
    ...             1: 'mean_absolute_error',
    ...             2: 'mean_squared_error',
    ...             3: 'mean_absolute_error'},
    ...  'estimate': {0: 4.0, 1: 2.0, 2: 1.0, 3: 1.0}}
    ... )
    >>> plot = vetiver.plot_metrics(
    ...     df_metrics = df,
    ...     date = "index",
    ...     estimate = "estimate",
    ...     metric = "metric",
    ...     n = "n")
    >>> plot.show()    # doctest: +SKIP
    """

    fig = px.line(
        df_metrics,
        x=date,
        y=estimate,
        color=metric,
        facet_row=metric,
        markers=dict(size=n),
        hover_data={"n": ":"},
        **kw,
    )

    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig.update_layout(showlegend=False)

    return fig
