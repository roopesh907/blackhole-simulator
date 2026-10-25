
"""
Photon geodesic equations for a Schwarzschild black hole.

Units:
    Geometrized units, G = c = 1.

Coordinates:
    t     : Schwarzschild coordinate time
    r     : radial coordinate
    v_r   : dr/d(lambda), radial velocity with respect to
            the photon's affine parameter
    phi   : azimuthal angle

The photon is restricted to the equatorial plane, theta = pi/2.
"""

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from app.physics.schwarzschild import SchwarzschildBlackHole


@dataclass(frozen=True)
class PhotonConstants:
    """Conserved energy and angular momentum parameters."""

    energy: float
    angular_momentum: float

    def __post_init__(self) -> None:
        if not np.isfinite(self.energy) or self.energy <= 0:
            raise ValueError("Photon energy must be finite and positive.")

        if (
            not np.isfinite(self.angular_momentum)
            or self.angular_momentum < 0
        ):
            raise ValueError(
                "Angular momentum must be finite and non-negative."
            )


@dataclass(frozen=True)
class PhotonState:
    """The photon's state at one integration point."""

    t: float
    r: float
    v_r: float
    phi: float

    def to_array(self) -> NDArray[np.float64]:
        """Convert the state into a NumPy array for numerical integration."""
        return np.array(
            [self.t, self.r, self.v_r, self.phi],
            dtype=np.float64,
        )

    @classmethod
    def from_array(cls, values: NDArray[np.float64]) -> "PhotonState":
        """Reconstruct a photon state from a four-element array."""
        if values.shape != (4,):
            raise ValueError("Photon state must contain exactly four values.")

        if not np.all(np.isfinite(values)):
            raise ValueError("Photon state values must all be finite.")

        return cls(
            t=float(values[0]),
            r=float(values[1]),
            v_r=float(values[2]),
            phi=float(values[3]),
        )


def photon_derivatives(
    _lambda: float,
    state: NDArray[np.float64],
    black_hole: SchwarzschildBlackHole,
    constants: PhotonConstants,
) -> NDArray[np.float64]:
    """
    Evaluate d(t, r, v_r, phi)/d(lambda).

    This function defines the differential equations.
    It does not advance the photon in time; an integrator such as RK4
    will use these derivatives to calculate the next state.
    """
    if state.shape != (4,):
        raise ValueError("State must contain exactly four values.")

    if not np.all(np.isfinite(state)):
        raise ValueError("State values must all be finite.")

    t, r, v_r, phi = state

    del t, v_r, phi  # These values do not enter every derivative directly.

    if r <= black_hole.schwarzschild_radius:
        raise ValueError(
            "This Schwarzschild-coordinate solver currently supports "
            "only the region outside the event horizon."
        )

    energy = constants.energy
    angular_momentum = constants.angular_momentum
    metric_factor = black_hole.metric_factor(r)

    dt_dlambda = energy / metric_factor
    dr_dlambda = state[2]

    dv_r_dlambda = (
        angular_momentum**2 / r**3
        - 3.0 * black_hole.mass * angular_momentum**2 / r**4
    )

    dphi_dlambda = angular_momentum / r**2

    return np.array(
        [
            dt_dlambda,
            dr_dlambda,
            dv_r_dlambda,
            dphi_dlambda,
        ],
        dtype=np.float64,
    )
