"""Benchmarks results of solving Linear Programming problems with different sizes."""
import logging

import numpy as np
from pulp import LpMaximize
from pulp import LpProblem
from pulp import LpVariable
from pulp import lpSum

from solvers import solve_pulp_problem
from decorators import timeit


@timeit
def build_knapsack_problem(
        n_items: int,
        max_weight: float,
        random_seed: int = 42) -> LpProblem:
    """Creates a 0-1 knapsack problem."""
    rng = np.random.default_rng(random_seed)
    values = rng.lognormal(mean=1.0, sigma=1.0, size=n_items)
    weights = rng.lognormal(mean=0.0, sigma=1.0, size=n_items)

    model = LpProblem(name="01-knapsack", sense=LpMaximize)

    # Decision variables
    xs = [LpVariable(name=f"x_{i}", lowBound=0, upBound=1)
          for i in range(n_items)]

    # Define objective function
    model += lpSum([v * x for v, x in zip(values, xs)])

    # Add the constraints to the model
    model += (lpSum([w * x for w, x in zip(weights, xs)])
              <= max_weight, "max_weight_constraint.")

    return model


if __name__ == "__main__":
    logging.info("hello world!")

    for x in np.logspace(start=1, stop=6, num=11):
        test_items = int(x)
        logging.info(
            f"Solving the knapsack problem with {test_items:,} items.")
        knapsack_problem = build_knapsack_problem(
            n_items=test_items, max_weight=10)

        for test_solver in ("cbc", "gurobi"):
            logging.info(f"Use the {test_solver} solver.")
            _ = solve_pulp_problem(
                model=knapsack_problem, solver=test_solver, verbose=False)
