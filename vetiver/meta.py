def vetiver_meta(user: dict = None, version: str = None,
            url: str = None, required_pkgs: list = None):
    """Populate relevant metadata for VetiverModel

    Args
    ----
        user: dict
           Extra user-defined information
        version: str
            Model version, generally populated from pins
        url: str
            Discoverable URL for API
        required_pkgs: list
            Packages necessary to make predictions
    """
    meta = {
        'user': user,
        'version': version,
        'url': url,
        'required_pkgs': required_pkgs
        }
    return meta
