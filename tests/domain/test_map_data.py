"""Tests for map data entities."""

import pytest

from geo_tui.domain.entities.map_data import MapPoint, MapDataUpdate


class TestMapPoint:
    """Test suite for MapPoint entity."""
    
    def test_map_point_initialization(self):
        """Test map point initialization."""
        point = MapPoint(45.0, -30.0)
        assert point.longitude == 45.0
        assert point.latitude == -30.0
        assert point.data is None
    
    def test_map_point_with_data(self):
        """Test map point with associated data."""
        data = {"name": "Test", "value": 123}
        point = MapPoint(45.0, -30.0, data=data)
        assert point.data == data
    
    def test_map_point_validation_longitude(self):
        """Test longitude validation."""
        with pytest.raises(ValueError, match="Longitude must be between"):
            MapPoint(200.0, 0.0)
        
        with pytest.raises(ValueError, match="Longitude must be between"):
            MapPoint(-200.0, 0.0)
    
    def test_map_point_validation_latitude(self):
        """Test latitude validation."""
        with pytest.raises(ValueError, match="Latitude must be between"):
            MapPoint(0.0, 100.0)
        
        with pytest.raises(ValueError, match="Latitude must be between"):
            MapPoint(0.0, -100.0)
    
    def test_map_point_boundary_values(self):
        """Test boundary values are accepted."""
        point1 = MapPoint(180.0, 90.0)
        assert point1.longitude == 180.0
        assert point1.latitude == 90.0
        
        point2 = MapPoint(-180.0, -90.0)
        assert point2.longitude == -180.0
        assert point2.latitude == -90.0


class TestMapDataUpdate:
    """Test suite for MapDataUpdate entity."""
    
    def test_map_data_update_initialization(self):
        """Test map data update initialization."""
        data = {"temperature": 25.5, "humidity": 60}
        update = MapDataUpdate(45.0, -30.0, data)
        
        assert update.longitude == 45.0
        assert update.latitude == -30.0
        assert update.data == data
    
    def test_to_point(self):
        """Test conversion to MapPoint."""
        data = {"value": 42}
        update = MapDataUpdate(45.0, -30.0, data)
        point = update.to_point()
        
        assert isinstance(point, MapPoint)
        assert point.longitude == 45.0
        assert point.latitude == -30.0
        assert point.data == data

