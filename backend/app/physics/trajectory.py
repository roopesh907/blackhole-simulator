
"""Photon trajectory integration around a Schwarzschild black hole."""

from dataclasses import dataclass
from typing import Literal

import numpy as np
from numpy.typing import NDArray

from app.physics.geodesics import (
    PhotonConstants,
    PhotonState,
    photon_derivatives,
)
from app.physics.rk4 import rk4_step
from app.physics.schwarzschild import SchwarzschildBlackHole


FloatArray = NDArray[np.float64]
TrajectoryStatus = Literal["captured", "escaped", "max_steps"]


@dataclass(frozen=True)
class TrajectoryResult:
    """Recorded photon path and the reason integration stopped."""

    states: FloatArray
    affine_parameters: FloatArray
    status: TrajectoryStatus

    @property
    def steps_taken(self) -> int:
        return len(self.states) - 1


def create_initial_state(
    black_hole: SchwarzschildBlackHole,
    constants: PhotonConstants,
    r: float,
    phi: float = 0.0,
    t: float = 0.0,
    radial_direction: Literal["inward", "outward"] = "inward",
) -> PhotonState:
    """
    Construct an initial photon state satisfying the null constraint.

    The radial velocity follows from:
        v_r^2 = E^2 - f(r) * L^2 / r^2
    """
    if not np.isfinite(r) or r <= black_hole.schwarzschild_radius:
        raise ValueError("Initial radius must be outside the event horizon.")

    if not all(np.isfinite(value) for value in (phi, t)):
        raise ValueError("Initial coordinates must be finite.")

    if radial_direction not in ("inward", "outward"):
        raise ValueError("Radial direction must be inward or outward.")

    f = black_hole.metric_factor(r)
    energy = constants.energy
    angular_momentum = constants.angular_momentum

    radial_speed_squared = (
        energy**2 - f * angular_momentum**2 / r**2
    )

    tolerance = 1e-12
    if radial_speed_squared < -tolerance:
        raise ValueError(
            "These energy and angular momentum values do not permit "
            "a photon at the specified radius."
        )

    radial_speed = np.sqrt(max(0.0, radial_speed_squared))

    if radial_direction == "inward":
        radial_speed = -radial_speed

    return PhotonState(
        t=t,
        r=r,
        v_r=float(radial_speed),
        phi=phi,
    )


def integrate_trajectory(
    black_hole: SchwarzschildBlackHole,
    constants: PhotonConstants,
    initial_state: PhotonState,
    step_size: float = 0.01,
    max_steps: int = 100_000,
    escape_radius: float | None = None,
) -> TrajectoryResult:
    """
    Integrate a photon trajectory using fixed-step RK4.

    The solver uses Schwarzschild coordinates outside the horizon.
    A trial RK4 step that reaches the horizon is treated as capture.
    """
    if not np.isfinite(step_size) or step_size <= 0:
        raise ValueError("Step size must be finite and positive.")

    if max_steps < 1:
        raise ValueError("max_steps must be at least 1.")

    horizon = black_hole.schwarzschild_radius

    if initial_state.r <= horizon:
        raise ValueError("Initial state must be outside the event horizon.")

    if escape_radius is None:
        escape_radius = 100.0 * black_hole.mass

    if not np.isfinite(escape_radius) or escape_radius <= horizon:
        raise ValueError("Escape radius must be finite and outside the horizon.")

    # Verify the initial state satisfies the photon null constraint.
    f = black_hole.metric_factor(initial_state.r)
    expected_vr_squared = (
        constants.energy**2
        - f * constants.angular_momentum**2 / initial_state.r**2
    )

    if expected_vr_squared < -1e-12:
        raise ValueError("Initial state violates the null constraint.")

    if not np.isclose(
        initial_state.v_r**2,
        max(0.0, expected_vr_squared),
        rtol=1e-8,
        atol=1e-10,
    ):
        raise ValueError("Initial radial velocity violates the null constraint.")

    state = initial_state.to_array()
    parameter = 0.0

    states: list[FloatArray] = [state.copy()]
    parameters: list[float] = [parameter]

    def derivative(
        lam: float,
        values: FloatArray,
    ) -> FloatArray:
        return photon_derivatives(lam, values, black_hole, constants)

    status: TrajectoryStatus = "max_steps"

    for _ in range(max_steps):
        radius = float(state[1])

        if radius <= horizon * (1.0 + 1e-7):
            status = "captured"
            break

        if radius >= escape_radius and state[2] > 0:
            status = "escaped"
            break

        try:
            next_state = rk4_step(
                derivative=derivative,
                parameter=parameter,
                state=state,
                step_size=step_size,
            )
        except ValueError as exc:
            # Schwarzschild coordinates are unsuitable at the horizon.
            if "outside the event horizon" in str(exc):
                status = "captured"
                break
            raise

        # Do not store a trial state that has crossed the horizon.
        if next_state[1] <= horizon:
            status = "captured"
            break

        state = next_state
        parameter += step_size

        states.append(state.copy())
        parameters.append(parameter)

    return TrajectoryResult(
        states=np.vstack(states),
        affine_parameters=np.asarray(parameters, dtype=np.float64),
        status=status,
    )
