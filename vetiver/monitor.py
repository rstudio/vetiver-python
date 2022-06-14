import pins
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

def compute_metrics(data, 
                    date_var, 
                    period,
                    metric_set, 
                    truth, 
                    pred):
    
    output = pd.DataFrame()
    rol = data.set_index(date_var)
    rol = rol.rolling(window=period)

    for metric in metric_set:
        rol.apply(
            _compute, 
            raw=False, 
            kwargs = {'df':output,
            'truth': truth,
            'pred': pred,
            'metric': metric}
            )
    
    return output

def _compute(window, 
            df, 
            truth, 
            pred, 
            metric):
    output = metric(y_true=window, 
                    # TO DO: change y pred to correct piece
                    y_pred=np.random.randint(0,1000,size=(len(window),1)))
    df.loc[window.index.max(), metric.__name__] = output
    return output


# def pin_metrics(board,
#                                 df_metrics,
#                                 metrics_pin_name,
#                                 #.index = .index,
#                                 overwrite = True):
    
# #    date_var <- quo_name(enquo(date_var)) #enquo?

#     new_metrics = df_metrics.sort()

#     new_dates = df_metrics.index.unique()

#     old_metrics = pins.pin_read(board, metrics_pin_name)
#     overlapping_dates = old_metrics.index in new_dates

#     if overwrite is True:
#         old_metrics = old_metrics not in overlapping_dates
#     else:
#         if overlapping_dates:
#             raise ValueError(f"The new metrics overlap with dates \
#                      already stored in {repr(metrics_pin_name)} \
#                      Check the aggregated dates or use `overwrite = True`"
#             )

#     new_metrics = old_metrics + df_metrics
#     new_metrics <- vec_slice(
#         new_metrics,
#         vctrs::vec_order(new_metrics.index)
#     )

#     pins.pin_write(board, new_metrics, metrics_pin_name)


def vetiver_plot_metrics(df_metrics,
                        date_var,
                        metric):

    ncols = 1
    nrows = len(metric)

    fig, axes = plt.subplots(
        nrows=nrows,
        ncols=ncols
    )

    # loop for plotting each column
    for i, col in enumerate(df_metrics.columns):
        sns.lineplot(
            x=df_metrics[date_var], 
            y=df_metrics[col], 
            ax=axes[i], 
            color='royalblue'
            )\
            .set_title(col)

    fig.tight_layout()