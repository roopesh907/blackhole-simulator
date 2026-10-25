
import pytest

from app.physics.schwarzschild import SchwarzschildBlackHole


def test_schwarzschild_radius():
    black_hole = SchwarzschildBlackHole(mass=1.0)

    assert black_hole.schwarzschild_radius == 2.0


def test_metric_factor():
    black_hole = SchwarzschildBlackHole(mass=1.0)

    assert black_hole.metric_factor(4.0) == pytest.approx(0.5)
    assert black_hole.metric_factor(10.0) == pytest.approx(0.8)


def test_horizon_detection():
    black_hole = SchwarzschildBlackHole(mass=1.0)

    assert black_hole.is_outside_horizon(3.0)
    assert not black_hole.is_outside_horizon(2.0)


def test_invalid_mass():
    with pytest.raises(ValueError):
        SchwarzschildBlackHole(mass=0.0)


def test_invalid_radius():
    black_hole = SchwarzschildBlackHole(mass=1.0)

    with pytest.raises(ValueError):
        black_hole.metric_factor(0.0)
