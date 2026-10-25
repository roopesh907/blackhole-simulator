
"""Connect API parameters to the Schwarzschild physics engine."""

import math

import numpy as np

from app.physics.geodesics import PhotonConstants
from app.physics.schwarzschild import SchwarzschildBlackHole
from app.physics.trajectory import (
    create_initial_state,
    integrate_trajectory,
)
from app.schemas.simulation import (
    SimulationRequest,
    SimulationResponse,
    TrajectoryPoint,
)


def run_simulation(request: SimulationRequest) -> SimulationResponse:
    """Run a photon simulation and return a sampled trajectory."""

    black_hole = SchwarzschildBlackHole(
        mass=request.black_hole_mass,
    )

    # Normalize photon energy to E=1, making impact parameter b=L.
    constants = PhotonConstants(
        energy=1.0,
        angular_momentum=request.impact_parameter,
    )

    initial_state = create_initial_state(
        black_hole=black_hole,
        constants=constants,
        r=request.initial_radius,
        phi=request.initial_phi,
        radial_direction=request.radial_direction,
    )

    result = integrate_trajectory(
        black_hole=black_hole,
        constants=constants,
        initial_state=initial_state,
        step_size=request.step_size,
        max_steps=request.max_steps,
        escape_radius=request.escape_radius,
    )

    # Calculate physical summary values from ALL integrated states,
    # before reducing the number of points returned to the client.
    closest_approach = float(np.min(result.states[:, 1]))
    final_state = result.states[-1]
    final_radius = float(final_state[1])

    # Choose evenly spaced indices, preserving the first and last points.
    states = result.states
    limit = request.max_output_points

    if limit is not None and len(states) > limit:
        indices = np.linspace(
            0,
            len(states) - 1,
            num=limit,
            dtype=np.int64,
        )
        states = states[indices]

    points: list[TrajectoryPoint] = []

    for state in states:
        r = float(state[1])
        phi = float(state[3])

        # Three.js uses Y as the vertical axis; the orbit lies in XZ.
        points.append(
            TrajectoryPoint(
                x=r * math.cos(phi),
                y=0.0,
                z=r * math.sin(phi),
                r=r,
                phi=phi,
            )
        )

    return SimulationResponse(
        status=result.status,
        steps_taken=result.steps_taken,
        closest_approach=closest_approach,
        final_radius=final_radius,
        points=points,
    )
