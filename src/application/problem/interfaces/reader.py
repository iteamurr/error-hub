import abc
from typing import Any


class ProblemReader(abc.ABC):
    @abc.abstractmethod
    def find(
        self,
        filters: dict[str, Any],
    ) -> list[dict[str, Any]]: ...

    @abc.abstractmethod
    def find_by_hash(
        self,
        hash: str,
    ) -> list[dict[str, Any]]: ...
