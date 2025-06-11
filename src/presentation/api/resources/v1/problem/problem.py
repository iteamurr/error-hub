import flask_restful

import src.domain.services.problem as problem_services

service = problem_services.ProblemService()


class ProblemsResource(flask_restful.Resource):
    def post(self):
        return service.create_problem()


class FindResource(flask_restful.Resource):
    def post(self):
        return service.find_problems()


class FindByHashResource(flask_restful.Resource):
    def get(self):
        return service.find_by_hash()
