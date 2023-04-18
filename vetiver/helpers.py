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


@api_data_to_frame.register(pd.DataFrame)
def _pd_frame(pred_data):

    return pred_data


@api_data_to_frame.register(dict)
def _dict(pred_data):
    return api_data_to_frame([pred_data])


def response_to_frame(response: dict) -> pd.DataFrame:
    """Convert API JSON response to data frame

    Parameters
    ----------
    response : dict
        Response from API endpoint

    Returns
    -------
    pd.DataFrame
        Response translated into DataFrame
    """
    response_df = pd.DataFrame.from_dict(response.json())

    return response_df
