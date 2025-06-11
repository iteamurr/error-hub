import abc
from typing import Any


class ProblemRepo(abc.ABC):
    @abc.abstractmethod
    def create(
        self,
        hash: str,
        header: dict[str, Any],
        body: dict[str, Any],
    ) -> None: ...
