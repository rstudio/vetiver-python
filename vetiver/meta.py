from dataclasses import dataclass


@dataclass
class VetiverMeta:
    """Metadata in a VetiverModel"""

    user: "dict | None" = None
    version: "str | None" = None
    url: "str | None" = None
    required_pkgs: "list | None" = None

    @classmethod
    def from_dict(cls, metadata, pip_name, pkg) -> "VetiverMeta":

        if metadata:
            user = metadata.get("user", metadata)
            version = metadata.get("version", None)
            url = metadata.get("url", None)
            required_pkgs = metadata.get("required_pkgs", [])
        else:
            user, version, url, required_pkgs = None, None, None, []

        if not list(filter(lambda x: pip_name in x, required_pkgs)):
            required_pkgs = required_pkgs + [f"{pip_name}=={pkg.__version__}"]

        return cls(user, version, url, required_pkgs)
