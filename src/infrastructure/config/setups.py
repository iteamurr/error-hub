import flask_restful

import src.presentation.api.resources as api_resources


def setup_resources(api: flask_restful.Api):
    for resource, path in api_resources.v1_resources.items():
        api.add_resource(resource, "/v1" + path)
