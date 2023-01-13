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
    python_version: "str | None" = None

    def to_dict(self) -> Mapping:
        data = asdict(self)

        return data

    @classmethod
    def from_dict(cls, metadata, pip_name=None) -> "VetiverMeta":

        metadata = {} if metadata is None else metadata

        user = metadata.get("user", metadata)
        version = metadata.get("version", None)
        url = metadata.get("url", None)
        required_pkgs = metadata.get("required_pkgs", [])
        python_version = metadata.get("python_version", sys.version)

        if pip_name:
            if not list(filter(lambda x: pip_name in x, required_pkgs)):
                required_pkgs = required_pkgs + [f"{pip_name}"]

        return cls(user, version, url, required_pkgs, python_version)
