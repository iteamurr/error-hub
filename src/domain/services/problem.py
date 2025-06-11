import flask
import flask_restful

import src.application.common.exceptions as repo_exceptions
import src.infrastructure.db.drivers.mongo as mongo_driver
import src.infrastructure.db.repositories.problem as problem_repos
import src.infrastructure.hashing.hash_calculator as hash_calc


class ProblemService:
    def __init__(self) -> None:
        mongo = mongo_driver.MongoDriver()
        coll = mongo.get_collection()
        self.repo = problem_repos.ProblemRepoImpl(coll)
        self.read = problem_repos.ProblemReaderImpl(coll)
        self.hashc = hash_calc.HashCalculator()

    def create_problem(self):
        data = flask.request.get_json(force=True)
        header = data.get("header")
        body = data.get("body")

        if not isinstance(header, dict) or not isinstance(body, dict):
            flask_restful.abort(400, message="Ожидаются объекты header и body")

        h = self.hashc.compute(header, body)
        try:
            self.repo.create(h, header, body)
        except repo_exceptions.RepositoryError as e:
            flask_restful.abort(500, message=str(e))

        return {"hash": h}, 201

    def find_problems(self):
        filters = flask.request.get_json(force=True)
        if not isinstance(filters, dict):
            flask_restful.abort(400, message="Фильтры должны быть JSON-объектом")

        try:
            docs = self.read.find(filters)
        except repo_exceptions.RepositoryError as e:
            flask_restful.abort(500, message=str(e))

        results = [
            {
                "id": str(d["_id"]),
                "hash": d["hash"],
                "header": d["header"],
                "body": d["body"],
            }
            for d in docs
        ]

        resp = flask.make_response(flask.jsonify(results), 200)
        resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        return resp

    def find_by_hash(self):
        h = flask.request.args.get("h")
        if not h:
            flask_restful.abort(400, message="Не задан параметр hash")

        try:
            docs = self.read.find_by_hash(h)
        except repo_exceptions.RepositoryError as e:
            flask_restful.abort(500, message=str(e))

        results = [
            {
                "id": str(d["_id"]),
                "hash": d["hash"],
                "header": d["header"],
                "body": d["body"],
            }
            for d in docs
        ]
        return flask.jsonify(results)
