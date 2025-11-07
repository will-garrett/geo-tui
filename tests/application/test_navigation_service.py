"""Tests for navigation service."""

import pytest

from geo_tui.application.services.navigation_service import NavigationService
from geo_tui.domain.entities.viewport import Viewport


class TestNavigationService:
    """Test suite for NavigationService."""
    
    def test_navigation_service_initialization(self, navigation_service):
        """Test navigation service initialization."""
        assert navigation_service is not None
        assert navigation_service.viewport is not None
    
    def test_pan_left(self, navigation_service):
        """Test panning left."""
        initial_x = navigation_service.viewport.center_x
        navigation_service.pan_left()
        
        assert navigation_service.viewport.center_x < initial_x
    
    def test_pan_right(self, navigation_service):
        """Test panning right."""
        initial_x = navigation_service.viewport.center_x
        navigation_service.pan_right()
        
        assert navigation_service.viewport.center_x > initial_x
    
    def test_pan_up(self, navigation_service):
        """Test panning up."""
        initial_y = navigation_service.viewport.center_y
        navigation_service.pan_up()
        
        assert navigation_service.viewport.center_y > initial_y
    
    def test_pan_down(self, navigation_service):
        """Test panning down."""
        initial_y = navigation_service.viewport.center_y
        navigation_service.pan_down()
        
        assert navigation_service.viewport.center_y < initial_y
    
    def test_pan(self, navigation_service):
        """Test panning with deltas."""
        initial_x = navigation_service.viewport.center_x
        initial_y = navigation_service.viewport.center_y
        
        navigation_service.pan(100.0, 200.0)
        
        assert navigation_service.viewport.center_x == initial_x + 100.0
        assert navigation_service.viewport.center_y == initial_y + 200.0
    
    def test_zoom_in(self, navigation_service):
        """Test zooming in."""
        initial_scale = navigation_service.viewport.meters_per_pixel
        navigation_service.zoom_in()
        
        assert navigation_service.viewport.meters_per_pixel < initial_scale
    
    def test_zoom_out(self, navigation_service):
        """Test zooming out."""
        initial_scale = navigation_service.viewport.meters_per_pixel
        navigation_service.zoom_out()
        
        assert navigation_service.viewport.meters_per_pixel > initial_scale
    
    def test_reset(self, navigation_service):
        """Test resetting viewport."""
        # Modify viewport
        navigation_service.viewport.pan(1000.0, 2000.0)
        navigation_service.viewport.zoom(0.5)
        
        # Reset
        navigation_service.reset()
        
        assert navigation_service.viewport.center_x == 0.0
        assert navigation_service.viewport.center_y == 0.0
        assert navigation_service.viewport.meters_per_pixel == 1_000_000.0

