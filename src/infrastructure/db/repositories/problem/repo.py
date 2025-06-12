from typing import Any

import pymongo.errors as pymongo_errors
from pymongo.collection import Collection

import src.application.common.exceptions as common_exceptions
import src.application.problem.interfaces.repo as problem_repo


class ProblemRepoImpl(problem_repo.ProblemRepo):
    def __init__(self, collection: Collection) -> None:
        self.collection = collection

    def create(
        self,
        hash: str,
        header: dict[str, Any],
        body: dict[str, Any],
    ) -> None:
        doc = {"hash": hash, "header": header, "body": body}
        try:
            self.collection.insert_one(doc)
        except pymongo_errors.PyMongoError as e:
            raise common_exceptions.RepositoryError(
                f"Failed to insert problem: {e}"
            ) from e
