import datetime
import pins
from pins.errors import PinsError
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def compute_metrics(data, 
                    date_var, 
                    period,
                    metric_set, 
                    truth, 
                    estimate):
    """
    Compute metrics for given time period

    Parameters
    ----------
    data : DataFrame
        Pandas dataframe
    date_var: 
        Column in `data` containing dates
    period:
        Defining period to group by 
        https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases
    metric_set: list
        List of metrics to compute 
        https://scikit-learn.org/stable/modules/classes.html#module-sklearn.metrics
    truth:
        Column identifier for true results
    estimate:
        Column identifier for predicted results

    """
    output = pd.DataFrame()
    dates_sorted = data.set_index(date_var).sort_index()
    rol = dates_sorted.set_index(truth).rolling(window=period)

    for metric in metric_set:
        rol[metric.__name__] =rol.apply(
            _compute, 
            raw=False, 
            kwargs = {
            'metric': metric}
            )
    
    rol.set_index(date_var)

    return output

def _compute(window, 
            metric):

    output = metric(y_true = window.index,
                    y_pred=window)
    return output


def pin_metrics(board,
                df_metrics,
                metrics_pin_name,
                overwrite = False):
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
    overwrite: bool
        If TRUE (the default), overwrite any metrics for 
        dates that exist both in the existing pin and 
        new metrics with the new values. If FALSE, error 
        when the new metrics contain overlapping dates with 
        the existing pin.
    """
    date_types = (datetime.date, datetime.time, datetime.datetime)
    if not isinstance(df_metrics.index, date_types):
        try: 
            df_metrics = df_metrics.index.astype('datetime')
        except TypeError:
            raise TypeError("Index must be a date type")

    new_metrics = df_metrics.sort_index()

    new_dates = df_metrics.index.unique()

    try:
        old_metrics = board.pin_read(metrics_pin_name)
    except PinsError:
        board.pin_write(metrics_pin_name)

    overlapping_dates = old_metrics.index in new_dates

    if overwrite is True:
        old_metrics = old_metrics not in overlapping_dates
    else:
        if overlapping_dates:
            raise ValueError(f"The new metrics overlap with dates \
                     already stored in {repr(metrics_pin_name)} \
                     Check the aggregated dates or use `overwrite = True`"
            )

    new_metrics = old_metrics + df_metrics
    new_metrics = new_metrics.sort_index()

    pins.pin_write(board, new_metrics, metrics_pin_name)


def plot_metrics(df_metrics,
                        date_var, metric):

    ncols = 1
    nrows = len(metric)

    fig, axes = plt.subplots(
        nrows=nrows,
        ncols=ncols
    )
    """
    Plot metrics over a given time period

    Parameters
    ----------
    df_metrics : DataFrame
        Pandas dataframe of metrics over time, such as created by `compute_metircs()`
    date_var: 
        Column in `data` containing dates
    metric_set: list
        List of metrics to compute

    """

    # loop for plotting each column
    for i, col in enumerate(df_metrics.columns):
        sns.lineplot(
            x=date_var, 
            y=df_metrics[col], 
            ax=axes[i], 
            color='royalblue'
            )\
            .set_title(col)

    fig.tight_layout()