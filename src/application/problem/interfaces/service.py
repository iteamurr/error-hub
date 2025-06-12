import abc
from typing import Any

import flask


class AbstractProblemService(abc.ABC):
    @abc.abstractmethod
    def create_problem(self) -> tuple[dict[str, Any], int]: ...

    @abc.abstractmethod
    def find_problems(self) -> flask.Response: ...

    @abc.abstractmethod
    def find_by_hash(self) -> flask.Response: ...
