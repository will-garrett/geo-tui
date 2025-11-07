"""Tests for viewport entity."""

import pytest

from geo_tui.domain.entities.viewport import Viewport


class TestViewport:
    """Test suite for Viewport entity."""
    
    def test_viewport_initialization(self):
        """Test viewport initialization."""
        viewport = Viewport(100.0, 200.0, 1000.0)
        assert viewport.center_x == 100.0
        assert viewport.center_y == 200.0
        assert viewport.meters_per_pixel == 1000.0
    
    def test_get_bounds(self):
        """Test getting viewport bounds."""
        viewport = Viewport(0.0, 0.0, 1000.0)
        minx, miny, maxx, maxy = viewport.get_bounds(100, 50)
        
        # Width: 100 pixels * 1000 m/px = 100000 m, half = 50000
        # Height: 50 pixels * 1000 m/px = 50000 m, half = 25000
        assert minx == -50000.0
        assert maxx == 50000.0
        assert miny == -25000.0
        assert maxy == 25000.0
    
    def test_pan(self):
        """Test panning the viewport."""
        viewport = Viewport(0.0, 0.0, 1000.0)
        viewport.pan(100.0, 200.0)
        
        assert viewport.center_x == 100.0
        assert viewport.center_y == 200.0
    
    def test_zoom(self):
        """Test zooming the viewport."""
        viewport = Viewport(0.0, 0.0, 1000.0)
        viewport.zoom(0.5)  # Zoom in
        
        assert viewport.meters_per_pixel == 500.0
        
        viewport.zoom(2.0)  # Zoom out
        assert viewport.meters_per_pixel == 1000.0
    
    def test_reset(self):
        """Test resetting the viewport."""
        viewport = Viewport(100.0, 200.0, 500.0)
        viewport.reset()
        
        assert viewport.center_x == 0.0
        assert viewport.center_y == 0.0
        assert viewport.meters_per_pixel == 1_000_000.0
    
    def test_reset_with_custom_values(self):
        """Test resetting with custom values."""
        viewport = Viewport(0.0, 0.0, 1000.0)
        viewport.reset(50.0, 75.0, 2000.0)
        
        assert viewport.center_x == 50.0
        assert viewport.center_y == 75.0
        assert viewport.meters_per_pixel == 2000.0

