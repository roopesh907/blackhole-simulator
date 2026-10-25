
"""HTTP endpoint for photon trajectory simulations."""

from fastapi import APIRouter, HTTPException
from pydantic import ValidationError

from app.schemas.simulation import SimulationRequest, SimulationResponse
from app.services.simulation_service import run_simulation

router = APIRouter(tags=["Simulation"])


@router.post("/simulate", response_model=SimulationResponse)
def simulate_photon(request: SimulationRequest) -> SimulationResponse:
    """Calculate a photon trajectory around a Schwarzschild black hole."""

    try:
        return run_simulation(request)
    except (ValueError, ValidationError) as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc
