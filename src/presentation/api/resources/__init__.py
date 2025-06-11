from src.presentation.api.resources.v1.problem.problem import (
    FindByHashResource,
    FindResource,
    ProblemsResource,
)

v1_resources = {
    ProblemsResource: "/problems",
    FindResource: "/find",
    FindByHashResource: "/find2",
}

# For a future use
v2_resources = {}

all = [v1_resources, v2_resources]
