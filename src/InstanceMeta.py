from abc import ABC, abstractmethod
from typing import Any, Dict


class InstanceMeta(ABC):
    def __init__(self, version: Any) -> None:
        self._version = version

    @property
    def instance_version(self) -> Any:
        return self._version

    @abstractmethod
    def get_params(self) -> Dict[str, Any]:
        pass

    def __str__(self):
        return str(self.get_params())


class RealInstanceMeta(InstanceMeta):

    def __init__(self, version: int, number_of_projects: int):
        super().__init__(version)
        self._number_of_projects = number_of_projects

    @property
    def number_of_projects(self) -> int:
        return self._number_of_projects

    def get_params(self) -> Dict[str, Any]:
        return {
            "version": self.instance_version,
            "number_of_projects": self.number_of_projects
        }


class SyntheticInstanceMeta(InstanceMeta):

    def __init__(self, version: str, J: int, M: int, K: int) -> None:
        self._J = J
        self._M = M
        self._K = K
        super().__init__(version)

    @property
    def J(self) -> int:
        return self._J

    @property
    def M(self) -> int:
        return self._M

    @property
    def K(self) -> int:
        return self._K

    def get_params(self) -> Dict[str, Any]:
        return {
            "J": self.J,
            "M": self.M,
            "K": self.K,
            "version": self.instance_version
        }
