
import numpy as np
import pytest

from app.physics.rk4 import rk4_step


def test_rk4_exponential_growth():
    # Exact solution: y(lambda) = exp(lambda), with y(0) = 1.
    def derivative(parameter, state):
        return state

    result = rk4_step(
        derivative=derivative,
        parameter=0.0,
        state=np.array([1.0]),
        step_size=0.1,
    )

    assert result[0] == pytest.approx(np.exp(0.1), abs=1e-6)


def test_rk4_harmonic_oscillator():
    # x' = v, v' = -x; start at x=1, v=0.
    def derivative(parameter, state):
        x, v = state
        return np.array([v, -x])

    result = rk4_step(
        derivative=derivative,
        parameter=0.0,
        state=np.array([1.0, 0.0]),
        step_size=0.1,
    )

    assert result[0] == pytest.approx(np.cos(0.1), abs=1e-6)
    assert result[1] == pytest.approx(-np.sin(0.1), abs=1e-6)


def test_rk4_rejects_invalid_step_size():
    def derivative(parameter, state):
        return state

    with pytest.raises(ValueError):
        rk4_step(
            derivative=derivative,
            parameter=0.0,
            state=np.array([1.0]),
            step_size=0.0,
        )


def test_rk4_rejects_mismatched_derivative_shape():
    def bad_derivative(parameter, state):
        return np.array([1.0, 2.0])

    with pytest.raises(ValueError):
        rk4_step(
            derivative=bad_derivative,
            parameter=0.0,
            state=np.array([1.0]),
            step_size=0.1,
        )
