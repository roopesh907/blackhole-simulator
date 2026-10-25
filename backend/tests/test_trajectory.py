
import numpy as np
import pytest

from app.physics.geodesics import PhotonConstants
from app.physics.schwarzschild import SchwarzschildBlackHole
from app.physics.trajectory import (
    create_initial_state,
    integrate_trajectory,
)


def test_initial_state_satisfies_null_constraint():
    black_hole = SchwarzschildBlackHole(mass=1.0)
    constants = PhotonConstants(energy=1.0, angular_momentum=2.0)

    state = create_initial_state(
        black_hole,
        constants,
        r=10.0,
        radial_direction="inward",
    )

    f = black_hole.metric_factor(state.r)
    expected = constants.energy**2 - (
        f * constants.angular_momentum**2 / state.r**2
    )

    assert state.v_r**2 == pytest.approx(expected)
    assert state.v_r < 0


def test_outward_photon_moves_outward():
    black_hole = SchwarzschildBlackHole(mass=1.0)
    constants = PhotonConstants(energy=1.0, angular_momentum=2.0)

    initial_state = create_initial_state(
        black_hole,
        constants,
        r=10.0,
        radial_direction="outward",
    )

    result = integrate_trajectory(
        black_hole,
        constants,
        initial_state,
        step_size=0.01,
        max_steps=20,
        escape_radius=100.0,
    )

    assert result.states.shape[1] == 4
    assert result.states[-1, 1] > initial_state.r
    assert result.steps_taken > 0


def test_trajectory_respects_step_limit():
    black_hole = SchwarzschildBlackHole(mass=1.0)
    constants = PhotonConstants(energy=1.0, angular_momentum=2.0)

    initial_state = create_initial_state(
        black_hole,
        constants,
        r=10.0,
        radial_direction="outward",
    )

    result = integrate_trajectory(
        black_hole,
        constants,
        initial_state,
        step_size=0.001,
        max_steps=5,
        escape_radius=1000.0,
    )

    assert result.status == "max_steps"
    assert result.steps_taken == 5
    assert result.states.shape == (6, 4)


def test_invalid_initial_radius_is_rejected():
    black_hole = SchwarzschildBlackHole(mass=1.0)
    constants = PhotonConstants(energy=1.0, angular_momentum=1.0)

    with pytest.raises(ValueError):
        create_initial_state(
            black_hole,
            constants,
            r=2.0,
        )
