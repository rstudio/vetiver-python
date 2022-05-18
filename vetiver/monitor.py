import pins

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


def vetiver_create_pin_metrics(df_metrics,
                                date_var,
                                board,
                                metrics_pin_name):
    
    date_var <- quo_name(enquo(date_var))

    new_metrics = df_metrics.sort()

    pins.pin_write(board, new_metrics, metrics_pin_name)


def vetiver_update_pin_metrics(df_metrics,
                                date_var,
                                board,
                                metrics_pin_name):
    
    new_dates = df_metrics[date_var].unique()
    old_metrics = pins.pin_read(board, metrics_pin_name)
    old_metrics = vec_slice(
        old_metrics,
        old_metrics[date_var] not in new_dates
    )
    new_metrics <- vec_sort(vctrs::vec_rbind(old_metrics, df_metrics))

    pins.pin_write(board, new_metrics, metrics_pin_name)
    
    return new_metrics

def vetiver_plot_metrics(df_metrics,
                        date_var,
                        estimate = estimate,
                        metric = metric,
                        n = n):


    plt.plot(x = df_metrics, y = date_var, marker=".")

    ggplot2::ggplot(data = df_metrics,
                    ggplot2::aes({{ date_var }}, {{.estimate}})) +
        # ggplot2::geom_line(ggplot2::aes(color = !!.metric), alpha = 0.7) +
        # ggplot2::geom_point(ggplot2::aes(color = !!.metric,
        #                                  size = {{n}}),
        #                     alpha = 0.9) +
        ggplot2::facet_wrap(ggplot2::vars(!!.metric),
                            scales = "free_y", ncol = 1) +
        ggplot2::guides(color = "none") +
        ggplot2::labs(x = NULL, y = NULL)