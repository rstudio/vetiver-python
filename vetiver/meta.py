import sys
from dataclasses import dataclass, asdict, field
from typing import Mapping


@dataclass
class VetiverMeta:
    """Metadata in a VetiverModel"""

    user: "dict | None" = field(default_factory=dict)
    version: "str | None" = None
    url: "str | None" = None
    required_pkgs: "list | None" = field(default_factory=list)
    python_version: "tuple | None" = None

    def to_dict(self) -> Mapping:
        data = asdict(self)

        return data

    @classmethod
    def from_dict(cls, metadata, pip_name=None) -> "VetiverMeta":

        metadata = {} if metadata is None else metadata

        user = metadata.get("user", metadata)
        version = metadata.get("version", None)
        url = metadata.get("url", None)
        # give correct value if key doesnt exist or if value is None
        required_pkgs = (
            []
            if not metadata.get("required_pkgs")
            else metadata.get("required_pkgs", [])
        )
        python_version = metadata.get("python_version", sys.version_info)
        python_version = python_version if not python_version else tuple(python_version)

        if pip_name:
            if not list(filter(lambda x: pip_name in x, required_pkgs)):
                required_pkgs = required_pkgs + [f"{pip_name}"]

        return cls(user, version, url, required_pkgs, python_version)
