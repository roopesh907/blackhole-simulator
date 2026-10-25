
"""Validated request and response models for photon simulations."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class SimulationRequest(BaseModel):
    """Parameters supplied by the frontend."""

    model_config = ConfigDict(extra="forbid")

    black_hole_mass: float = Field(gt=0, le=1_000_000)
    impact_parameter: float = Field(ge=0, le=1_000_000)
    initial_radius: float = Field(gt=0, le=1_000_000)
    radial_direction: Literal["inward", "outward"] = "inward"
    initial_phi: float = Field(default=0.0, ge=-1_000_000, le=1_000_000)
    step_size: float = Field(default=0.005, gt=0, le=0.1)
    max_steps: int = Field(default=100_000, ge=1, le=100_000)
    escape_radius: float | None = Field(default=None, gt=0, le=1_000_000)

    # Maximum number of trajectory points included in the response.
    # None returns every recorded point.
    max_output_points: int | None = Field(
        default=2000,
        ge=2,
        le=100_000,
    )

    @model_validator(mode="after")
    def validate_radii(self) -> "SimulationRequest":
        horizon = 2.0 * self.black_hole_mass

        if self.initial_radius <= horizon:
            raise ValueError(
                "initial_radius must be outside the event horizon "
                "(initial_radius > 2 * black_hole_mass)."
            )

        if self.escape_radius is not None and self.escape_radius <= horizon:
            raise ValueError(
                "escape_radius must be outside the event horizon."
            )

        return self


class TrajectoryPoint(BaseModel):
    """One spatial point, using Three.js-friendly Y-up coordinates."""

    x: float
    y: float
    z: float
    r: float
    phi: float


class SimulationResponse(BaseModel):
    """Simulation outcome and its sampled trajectory."""

    status: Literal["captured", "escaped", "max_steps"]
    steps_taken: int
    closest_approach: float
    final_radius: float
    points: list[TrajectoryPoint]
