
"""
Schwarzschild geometry utilities.

Units:
    Geometrized units, G = c = 1.

In these units, mass and distance use the same units.
The Schwarzschild radius is therefore r_s = 2M.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class SchwarzschildBlackHole:
    """A non-rotating, uncharged black hole."""

    mass: float

    def __post_init__(self) -> None:
        if self.mass <= 0:
            raise ValueError("Black hole mass must be positive.")

    @property
    def schwarzschild_radius(self) -> float:
        """Event-horizon radius: r_s = 2M."""
        return 2.0 * self.mass

    def metric_factor(self, r: float) -> float:
        """
        Return f(r) = 1 - 2M/r.

        Schwarzschild coordinates are singular at r = 0.
        The exterior region is r > 2M.
        """
        if r <= 0:
            raise ValueError("Radial coordinate r must be positive.")

        return 1.0 - self.schwarzschild_radius / r

    def is_outside_horizon(self, r: float) -> bool:
        """Whether the radial coordinate is outside the event horizon."""
        return r > self.schwarzschild_radius
