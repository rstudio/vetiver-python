def vetiver_meta(user:list = None, version = None,
            url = None, required_pkgs = None):

    meta = {
        'user': user,
        'version': version,
        'url': url,
        'required_pkgs': required_pkgs
        }
    return meta
