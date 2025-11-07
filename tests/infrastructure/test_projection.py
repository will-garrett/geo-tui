"""Tests for projection implementations."""

import pytest

from geo_tui.infrastructure.projection.mercator_projection import MercatorProjection


class TestMercatorProjection:
    """Test suite for MercatorProjection."""
    
    def test_projection_initialization(self):
        """Test projection initialization."""
        proj = MercatorProjection()
        assert proj is not None
    
    def test_project_origin(self):
        """Test projecting origin (0, 0)."""
        proj = MercatorProjection()
        x, y = proj.project(0.0, 0.0)
        
        # Origin should project to approximately (0, 0) in Web Mercator
        assert abs(x) < 1.0
        assert abs(y) < 1.0
    
    def test_project_known_point(self):
        """Test projecting a known point."""
        proj = MercatorProjection()
        # London: approximately 0°E, 51.5°N
        x, y = proj.project(0.0, 51.5)
        
        # Should be in reasonable range for Web Mercator
        assert -20000000 < x < 20000000
        assert 6000000 < y < 8000000
    
    def test_unproject_origin(self):
        """Test unprojecting origin."""
        proj = MercatorProjection()
        lon, lat = proj.unproject(0.0, 0.0)
        
        # Should be close to (0, 0)
        assert abs(lon) < 0.1
        assert abs(lat) < 0.1
    
    def test_round_trip(self):
        """Test round-trip projection."""
        proj = MercatorProjection()
        
        # Test with various coordinates
        test_points = [
            (0.0, 0.0),
            (45.0, 30.0),
            (-120.0, 40.0),
            (180.0, 0.0),
        ]
        
        for lon, lat in test_points:
            x, y = proj.project(lon, lat)
            lon2, lat2 = proj.unproject(x, y)
            
            # Should be close to original (allowing for projection errors)
            assert abs(lon - lon2) < 0.0001
            assert abs(lat - lat2) < 0.0001

