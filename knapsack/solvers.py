"""Linear Programming solvers related functions."""
import logging

from pulp import LpProblem
from pulp import GUROBI_CMD
from pulp import PULP_CHOCO_CMD
from pulp import PULP_CBC_CMD
from decorators import timeit

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)


@timeit
def solve_pulp_problem(
        model: LpProblem,
        solver: str = "cbc",
        verbose: bool = True) -> int:
    """Solves a constructed pulp model."""
    solver_mapping = {
        "cbc": PULP_CBC_CMD,
        "gurobi": GUROBI_CMD,
        "choco": PULP_CHOCO_CMD,
    }
    if solver not in solver_mapping:
        raise KeyError(f"The solver {solver} is not supported.")

    status = model.solve(solver_mapping[solver](msg=0))
    if status == 1:
        logging.info(f"The optimal value is: {model.objective.value()}")
        if verbose:
            for var in model.variables():
                logging.info(f"{var.name} = {var.value()}")
    else:
        logging.info("Pulp fails to solve the problem.")
    return status
