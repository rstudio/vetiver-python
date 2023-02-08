from functools import singledispatch
import pandas as pd
import pydantic


@singledispatch
def api_data_to_frame(pred_data) -> pd.DataFrame:
    """Convert prototype to dataframe data

    Parameters
    ----------
    pred_data : pydantic.BaseModel
        User data from given to API endpoint

    Returns
    -------
    pd.DataFrame
        BaseModel data translated into DataFrame
    """

    raise TypeError("Data should be list, pydantic.BaseModel, pd.DataFrame")


@api_data_to_frame.register(pydantic.BaseModel)
@api_data_to_frame.register(list)
def _(pred_data):

    return pd.DataFrame([dict(s) for s in pred_data])


@api_data_to_frame.register(dict)
def _dict(pred_data):
    return api_data_to_frame([pred_data])


# possible other names
# prototype_to_frame
# prototype_to_data
# prototype_to_dataframe
# prototype_to_datatype
# prototype_to_type
# api_data_to_
# json_to_
# server_data_to_
# transport_data_to_
# request
# query
# transit
# interchange/exchange
# transfer
# through
