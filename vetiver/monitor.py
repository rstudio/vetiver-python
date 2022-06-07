import pins
import matplotlib as plt
import pandas as pd

# def vetiver_compute_metrics(data,
#                             date_var,
#                             .period,
#                             truth, estimate, **kw,
#                             metric_set = yardstick::metrics,
#                             .every = 1L,
#                             .origin = NULL,
#                             .before = 0L,
#                             .after = 0L,
#                             .complete = FALSE):

#     rlang::check_installed("slider")
#     metrics_dots = list2(...)
#     date_var = enquo(date_var)
#     slider::slide_period_dfr(
#         data,
#         .i = data[[quo_name(date_var)]],
#         .period = .period,
#         .f = ~ tibble::tibble(
#             !!date_var := min(.x[[quo_name(date_var)]]),
#             n = nrow(.x),
#             metric_set(.x, {{truth}}, {{estimate}}, !!!metrics_dots)
#         ),
#         .every = .every,
#         .origin = .origin,
#         .before = .before,
#         .after = .after,
#         .complete = .complete
#     )


def vetiver_create_pin_metrics(board,
                                df_metrics,
                                metrics_pin_name,
                                #.index = .index,
                                overwrite = True):
    
#    date_var <- quo_name(enquo(date_var)) #enquo?

    new_metrics = df_metrics.sort()

    new_dates = df_metrics.index.unique()

    old_metrics = pins.pin_read(board, metrics_pin_name)
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
    new_metrics <- vec_slice(
        new_metrics,
        vctrs::vec_order(new_metrics.index)
    )

    pins.pin_write(board, new_metrics, metrics_pin_name)



def compute_metrics(data, date_var,
                            metric_set,
                            truth_quo,
                            estimate_quo,
                            *kw):
    index = data.date_var
    index = min(index)

    n = len(data)

    metrics = metric_set(
        data = data,
        truth = truth_quo,
        estimate = estimate_quo
    )

    tibble::tibble(
        .index = index,
        .n = n,
        metrics
    )


# def eval_select_one(col, data, arg, *kw, call = caller_env()):
#     rlang::check_installed("tidyselect")
#     check_dots_empty()

#     # `col` is a quosure that has its own environment attached
#     env = empty_env()

#     loc = tidyselect::eval_select(
#         expr = col,
#         data = data,
#         env = env,
#         error_call = call
#     )

#     if (length(loc) != 1):
#         raise ValueError("`{arg}` must specify exactly one column from `data`.")

#     return loc


# def vetiver_plot_metrics(df_metrics,
#                         date_var,
#                         estimate = estimate,
#                         metric = metric,
#                         n = n):


#     plt.plot(x = df_metrics, y = date_var, marker=".")

#     ggplot2::ggplot(data = df_metrics,
#                     ggplot2::aes({{ date_var }}, {{.estimate}})) +
#         # ggplot2::geom_line(ggplot2::aes(color = !!.metric), alpha = 0.7) +
#         # ggplot2::geom_point(ggplot2::aes(color = !!.metric,
#         #                                  size = {{n}}),
#         #                     alpha = 0.9) +
#         ggplot2::facet_wrap(ggplot2::vars(!!.metric),
#                             scales = "free_y", ncol = 1) +
#         ggplot2::guides(color = "none") +
#         ggplot2::labs(x = NULL, y = NULL)