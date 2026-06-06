"""Tests for the monocular distance estimator."""

import numpy as np
import pytest

from depthtrack.config import DistanceConfig
from depthtrack.perception.distance import estimate_distance


@pytest.fixture
def cfg():
    return DistanceConfig()


def test_degenerate_box_returns_fallback(cfg):
    depth = np.zeros((100, 100), dtype=np.float32)
    # x2 <= x1
    assert estimate_distance(depth, np.array([50, 50, 50, 60]), 100, 100, cfg) == 50.0


def test_result_is_clamped_to_range(cfg):
    depth = np.ones((100, 100), dtype=np.float32)  # far depth
    box = np.array([10, 10, 12, 12])  # tiny box -> large projection distance
    d = estimate_distance(depth, box, 100, 100, cfg)
    assert cfg.min_distance_m <= d <= cfg.max_distance_m


def test_closer_object_has_smaller_distance(cfg):
    # Lower normalised depth => nearer; wider box => nearer by projection too.
    depth = np.zeros((200, 200), dtype=np.float32)
    near_box = np.array([10, 10, 150, 150])   # large/near
    far_box = np.array([90, 90, 110, 110])    # small/far
    d_near = estimate_distance(depth, near_box, 200, 200, cfg)
    d_far = estimate_distance(depth, far_box, 200, 200, cfg)
    assert d_near < d_far


def test_box_clipped_to_frame_bounds(cfg):
    depth = np.full((100, 100), 0.5, dtype=np.float32)
    # box extends beyond frame; should not raise and stay in range
    d = estimate_distance(depth, np.array([-20, -20, 200, 200]), 100, 100, cfg)
    assert cfg.min_distance_m <= d <= cfg.max_distance_m


def test_depth_weight_one_ignores_projection():
    cfg = DistanceConfig(depth_weight=1.0, depth_near_m=1.0, depth_far_m=80.0)
    depth = np.zeros((100, 100), dtype=np.float32)  # median depth 0 -> near_m
    d = estimate_distance(depth, np.array([10, 10, 90, 90]), 100, 100, cfg)
    assert d == pytest.approx(1.0, abs=0.1)


def test_returns_one_decimal_place(cfg):
    depth = np.full((100, 100), 0.37, dtype=np.float32)
    d = estimate_distance(depth, np.array([10, 10, 60, 60]), 100, 100, cfg)
    assert d == round(d, 1)
