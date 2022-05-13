from vetiver.handlers import pytorch_vt, sklearn_vt
import sklearn 

torch_exists = True
try:
    import torch
except ImportError:
    torch_exists = False

def create_translator(model, ptype_data, save_ptype):
    """check for model type to handle prediction

    Parameters
    ----------
    model
        Description of parameter `x`.

    Returns
    -------
    pytorch_vt.TorchHandler or sklearn_vt.SKLearnHandler
        Handler class for specified model type
    """
    if torch_exists:
        if isinstance(model, torch.nn.Module):
            return pytorch_vt.TorchHandler(model, ptype_data, save_ptype)

    if isinstance(model, sklearn.base.BaseEstimator):
        return sklearn_vt.SKLearnHandler(model, ptype_data, save_ptype)

    else:
        raise NotImplementedError
