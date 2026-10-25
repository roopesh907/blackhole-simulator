
"""
Classical fourth-order Runge-Kutta integrator.

This module is physics-independent: it can integrate any system
of ordinary differential equations of the form dy/dlambda = f(lambda, y).
"""

from collections.abc import Callable

import numpy as np
from numpy.typing import NDArray


FloatArray = NDArray[np.float64]
DerivativeFunction = Callable[[float, FloatArray], FloatArray]


def rk4_step(
    derivative: DerivativeFunction,
    parameter: float,
    state: FloatArray,
    step_size: float,
) -> FloatArray:
    """
    Advance a state by one classical RK4 step.

    Args:
        derivative: Function returning dy/dlambda.
        parameter: Current value of the independent parameter.
        state: Current state vector.
        step_size: Step size h.

    Returns:
        The estimated state after one step.
    """
    if not np.isfinite(parameter):
        raise ValueError("Parameter must be finite.")

    if not np.isfinite(step_size) or step_size <= 0:
        raise ValueError("Step size must be finite and positive.")

    state = np.asarray(state, dtype=np.float64)

    if state.ndim != 1 or state.size == 0:
        raise ValueError("State must be a non-empty one-dimensional array.")

    if not np.all(np.isfinite(state)):
        raise ValueError("State values must all be finite.")

    k1 = np.asarray(derivative(parameter, state), dtype=np.float64)
    k2 = np.asarray(
        derivative(parameter + step_size / 2, state + step_size * k1 / 2),
        dtype=np.float64,
    )
    k3 = np.asarray(
        derivative(parameter + step_size / 2, state + step_size * k2 / 2),
        dtype=np.float64,
    )
    k4 = np.asarray(
        derivative(parameter + step_size, state + step_size * k3),
        dtype=np.float64,
    )

    for k in (k1, k2, k3, k4):
        if k.shape != state.shape:
            raise ValueError("Derivative output must match the state shape.")
        if not np.all(np.isfinite(k)):
            raise ValueError("Derivative values must all be finite.")

    next_state = state + (step_size / 6) * (
        k1 + 2 * k2 + 2 * k3 + k4
    )

    if not np.all(np.isfinite(next_state)):
        raise ValueError("Integration produced a non-finite state.")

    return next_state
