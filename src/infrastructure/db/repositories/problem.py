from typing import Any

import pymongo.errors as pymongo_errors
from pymongo.collection import Collection

import src.application.common.exceptions as common_exceptions
import src.application.problem.interfaces.reader as problem_reader
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


class ProblemReaderImpl(problem_reader.ProblemReader):
    def __init__(self, collection: Collection) -> None:
        self.collection = collection

    def find(self, filters: dict[str, Any]) -> list[dict[str, Any]]:
        clauses: list[dict[str, Any]] = []
        for k, v in filters.items():
            sval = str(v)
            clauses.append(
                {
                    "$or": [
                        {f"header.{k}": sval},
                        {f"body.{k}": sval},
                    ]
                }
            )
        query: dict[str, Any] = {"$and": clauses} if clauses else {}
        try:
            cursor = self.collection.find(query)
        except pymongo_errors.PyMongoError as e:
            raise common_exceptions.RepositoryError(
                f"Failed to find problems: {e}"
            ) from e

        return list(cursor)

    def find_by_hash(self, h: str) -> list[dict[str, Any]]:
        try:
            cursor = self.collection.find({"hash": h})
        except pymongo_errors.PyMongoError as e:
            raise common_exceptions.RepositoryError(
                f"Failed to find by hash: {e}"
            ) from e

        return list(cursor)
