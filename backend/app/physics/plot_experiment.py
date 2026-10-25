
"""Plot a photon scattering trajectory around a Schwarzschild black hole."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from app.physics.geodesics import PhotonConstants
from app.physics.schwarzschild import SchwarzschildBlackHole
from app.physics.trajectory import (
    create_initial_state,
    integrate_trajectory,
)


def main() -> None:
    # 1. Define the black hole and photon.
    black_hole = SchwarzschildBlackHole(mass=1.0)
    constants = PhotonConstants(
        energy=1.0,
        angular_momentum=6.0,
    )

    # 2. Launch the photon inward from r = 20.
    initial_state = create_initial_state(
        black_hole=black_hole,
        constants=constants,
        r=20.0,
        phi=0.0,
        radial_direction="inward",
    )

    # 3. Integrate the trajectory.
    result = integrate_trajectory(
        black_hole=black_hole,
        constants=constants,
        initial_state=initial_state,
        step_size=0.005,
        max_steps=100_000,
        escape_radius=100.0,
    )

    # 4. Convert the equatorial trajectory to Cartesian coordinates.
    radii = result.states[:, 1]
    angles = result.states[:, 3]

    x = radii * np.cos(angles)
    y = radii * np.sin(angles)

    horizon_radius = black_hole.schwarzschild_radius
    photon_sphere_radius = 3.0 * black_hole.mass

    # 5. Create a full view and a close-up of the black hole.
    fig, (full_ax, close_ax) = plt.subplots(
        1,
        2,
        figsize=(14, 6),
    )

    fig.suptitle(
        "Photon Scattering Around a Schwarzschild Black Hole",
        fontsize=14,
    )

    for ax in (full_ax, close_ax):
        # Event horizon: r = 2M.
        horizon = plt.Circle( # pyright: ignore[reportPrivateImportUsage]
            (0, 0),
            horizon_radius,
            color="black",
            label="Event horizon",
            zorder=3,
        )
        ax.add_patch(horizon)

        # Photon sphere: r = 3M.
        photon_sphere = plt.Circle( # pyright: ignore[reportPrivateImportUsage]
            (0, 0),
            photon_sphere_radius,
            fill=False,
            linestyle="--",
            linewidth=1.5,
            label="Photon sphere (r = 3M)",
        )
        ax.add_patch(photon_sphere)

        ax.set_aspect("equal", adjustable="box")
        ax.set_xlabel("x / M")
        ax.set_ylabel("y / M")
        ax.grid(True, alpha=0.3)

    # Full trajectory.
    full_ax.plot(x, y, label="Photon trajectory", linewidth=1.5)
    full_ax.scatter(
        x[0], y[0],
        marker="o",
        label="Launch point",
        zorder=4,
    )
    full_ax.scatter(
        x[-1], y[-1],
        marker="x",
        label="Final point",
        zorder=4,
    )
    full_ax.set_title(f"Full trajectory — outcome: {result.status}")
    full_ax.legend(fontsize=8)
    full_ax.set_xlim(-105, 105)
    full_ax.set_ylim(-105, 105)

    # Close-up: show only the section near the black hole.
    near_bh = radii <= 12.0
    close_ax.plot(
        x[near_bh],
        y[near_bh],
        label="Photon trajectory",
        linewidth=1.8,
    )
    close_ax.set_title("Close-up near the black hole")
    close_ax.set_xlim(-12, 12)
    close_ax.set_ylim(-12, 12)
    close_ax.legend(fontsize=8)

    fig.tight_layout()

    output_path = (
        Path(__file__).resolve().parents[2]
        / "photon_trajectory.png"
    )
    fig.savefig(output_path, dpi=180, bbox_inches="tight")

    print(f"Outcome: {result.status}")
    print(f"Trajectory points: {len(result.states)}")
    print(f"Closest sampled radius: {radii.min():.6f} M")
    print(f"Plot saved to: {output_path}")

    plt.show()


if __name__ == "__main__":
    main()
