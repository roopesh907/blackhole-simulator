
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)



def test_simulation_limits_returned_points_without_changing_summary():
    payload = {
        "black_hole_mass": 1.0,
        "impact_parameter": 6.0,
        "initial_radius": 20.0,
        "radial_direction": "inward",
        "step_size": 0.01,
        "max_steps": 100000,
        "escape_radius": 100.0,
        "max_output_points": 100,
    }

    response = client.post("/api/simulate", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "escaped"
    assert data["steps_taken"] > 100
    assert len(data["points"]) == 100

    # First and last points must be retained.
    assert data["points"][0]["r"] == 20.0
    assert abs(data["points"][-1]["r"] - data["final_radius"]) < 1e-9

    # The summary must describe the complete integration, not just
    # the sampled points.
    assert data["closest_approach"] > 2.0
