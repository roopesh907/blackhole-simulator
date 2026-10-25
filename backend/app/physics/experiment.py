
"""Run a first numerical experiment with a Schwarzschild black hole."""

import numpy as np

from app.physics.geodesics import PhotonConstants
from app.physics.schwarzschild import SchwarzschildBlackHole
from app.physics.trajectory import (
    create_initial_state,
    integrate_trajectory,
)


def main() -> None:
    black_hole = SchwarzschildBlackHole(mass=1.0)

    # Impact parameter b = L / E = 6.
    constants = PhotonConstants(
        energy=1.0,
        angular_momentum=6.0,
    )

    initial_state = create_initial_state(
        black_hole=black_hole,
        constants=constants,
        r=20.0,
        phi=0.0,
        radial_direction="inward",
    )

    result = integrate_trajectory(
        black_hole=black_hole,
        constants=constants,
        initial_state=initial_state,
        step_size=0.005,
        max_steps=100_000,
        escape_radius=100.0,
    )

    radii = result.states[:, 1]
    angles = result.states[:, 3]

    x = radii * np.cos(angles)
    y = radii * np.sin(angles)

    print("=== Schwarzschild Photon Experiment ===")
    print(f"Black-hole mass:        {black_hole.mass:.3f}")
    print(f"Event-horizon radius:   {black_hole.schwarzschild_radius:.3f}")
    print(f"Photon impact parameter:{constants.angular_momentum / constants.energy: .3f}")
    print(f"Initial radius:         {initial_state.r:.3f}")
    print(f"Final radius:           {radii[-1]:.6f}")
    print(f"Final angle:            {angles[-1]:.6f} rad")
    print(f"Trajectory points:      {len(result.states)}")
    print(f"Outcome:                {result.status}")
    print(f"Final Cartesian point:  ({x[-1]:.6f}, {y[-1]:.6f})")


if __name__ == "__main__":
    main()
