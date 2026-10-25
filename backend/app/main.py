
from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.simulation import router as simulation_router

app = FastAPI(
    title="Black Hole Photon Simulator",
    description=(
        "A computational physics backend for simulating "
        "photon trajectories around black holes."
    ),
    version="0.1.0",
)

app.include_router(health_router, prefix="/api")
app.include_router(simulation_router, prefix="/api")
