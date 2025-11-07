"""Tests for map service."""

import pytest

from geo_tui.application.services.map_service import MapService
from geo_tui.domain.entities.map_data import MapPoint, MapDataUpdate
from geo_tui.domain.entities.viewport import Viewport


class TestMapService:
    """Test suite for MapService."""
    
    def test_map_service_initialization(self, map_service):
        """Test map service initialization."""
        assert map_service is not None
        assert map_service.get_geometries() is None
    
    def test_load_geometries(self, map_service):
        """Test loading geometries."""
        map_service.load_geometries()
        geometries = map_service.get_geometries()
        
        assert geometries is not None
        assert len(geometries) > 0
    
    def test_add_point(self, map_service):
        """Test adding a point."""
        point = MapPoint(45.0, -30.0, {"test": "data"})
        map_service.add_point(point)
        
        points = map_service.get_points()
        assert len(points) == 1
        assert points[0] == point
    
    def test_update_map_data(self, map_service):
        """Test updating map data."""
        update = MapDataUpdate(45.0, -30.0, {"temperature": 25.0})
        map_service.update_map_data(update)
        
        points = map_service.get_points()
        assert len(points) == 1
        assert points[0].longitude == 45.0
        assert points[0].latitude == -30.0
        assert points[0].data == {"temperature": 25.0}
    
    def test_update_existing_point(self, map_service):
        """Test updating an existing point."""
        update1 = MapDataUpdate(45.0, -30.0, {"value": 1})
        update2 = MapDataUpdate(45.0, -30.0, {"value": 2})
        
        map_service.update_map_data(update1)
        map_service.update_map_data(update2)
        
        points = map_service.get_points()
        assert len(points) == 1
        assert points[0].data == {"value": 2}
    
    def test_clear_points(self, map_service):
        """Test clearing points."""
        map_service.add_point(MapPoint(45.0, -30.0))
        map_service.add_point(MapPoint(50.0, -35.0))
        
        assert len(map_service.get_points()) == 2
        
        map_service.clear_points()
        assert len(map_service.get_points()) == 0
    
    def test_render_without_geometries(self, map_service):
        """Test rendering without loaded geometries."""
        viewport = Viewport(0.0, 0.0, 1_000_000.0)
        result = map_service.render(viewport, 80, 24)
        
        assert result == ""
    
    def test_render_with_geometries(self, map_service):
        """Test rendering with loaded geometries."""
        map_service.load_geometries()
        viewport = Viewport(0.0, 0.0, 1_000_000.0)
        result = map_service.render(viewport, 80, 24)
        
        assert isinstance(result, str)
        assert len(result) > 0

