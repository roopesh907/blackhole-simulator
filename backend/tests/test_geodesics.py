
import numpy as np
import pytest

from app.physics.geodesics import (
    PhotonConstants,
    PhotonState,
    photon_derivatives,
)
from app.physics.schwarzschild import SchwarzschildBlackHole


def test_photon_state_array_round_trip():
    original = PhotonState(t=0.0, r=10.0, v_r=-0.5, phi=0.2)

    reconstructed = PhotonState.from_array(original.to_array())

    assert reconstructed == original


def test_photon_derivatives():
    black_hole = SchwarzschildBlackHole(mass=1.0)
    constants = PhotonConstants(energy=1.0, angular_momentum=2.0)
    state = np.array([0.0, 10.0, -0.5, 0.0])

    derivatives = photon_derivatives(
        0.0, state, black_hole, constants
    )

    assert derivatives[0] == pytest.approx(1.25)
    assert derivatives[1] == pytest.approx(-0.5)
    assert derivatives[2] == pytest.approx(0.0028)
    assert derivatives[3] == pytest.approx(0.02)


def test_invalid_photon_energy():
    with pytest.raises(ValueError):
        PhotonConstants(energy=0.0, angular_momentum=1.0)


def test_reject_state_at_horizon():
    black_hole = SchwarzschildBlackHole(mass=1.0)
    constants = PhotonConstants(energy=1.0, angular_momentum=1.0)
    state = np.array([0.0, 2.0, 0.0, 0.0])

    with pytest.raises(ValueError):
        photon_derivatives(0.0, state, black_hole, constants)
