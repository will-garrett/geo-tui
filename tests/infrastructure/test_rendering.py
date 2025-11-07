"""Tests for rendering implementations."""

import pytest
import geopandas as gpd
from shapely.geometry import LineString

from geo_tui.infrastructure.rendering.braille_renderer import BrailleRenderer
from geo_tui.domain.entities.viewport import Viewport


class TestBrailleRenderer:
    """Test suite for BrailleRenderer."""
    
    def test_renderer_initialization(self):
        """Test renderer initialization."""
        renderer = BrailleRenderer()
        assert renderer is not None
    
    def test_render_empty_viewport(self):
        """Test rendering with empty viewport."""
        renderer = BrailleRenderer()
        viewport = Viewport(0.0, 0.0, 1_000_000.0)
        geometries = gpd.GeoSeries([], crs="EPSG:3857")
        
        result = renderer.render(viewport, geometries, 80, 24)
        
        assert isinstance(result, str)
    
    def test_render_with_geometry(self):
        """Test rendering with a simple geometry."""
        renderer = BrailleRenderer()
        viewport = Viewport(0.0, 0.0, 1_000_000.0)
        
        # Create a simple line geometry in Web Mercator
        line = LineString([(-1000000, -1000000), (1000000, 1000000)])
        geometries = gpd.GeoSeries([line], crs="EPSG:3857")
        
        result = renderer.render(viewport, geometries, 80, 24)
        
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_render_zero_size(self):
        """Test rendering with zero size."""
        renderer = BrailleRenderer()
        viewport = Viewport(0.0, 0.0, 1_000_000.0)
        geometries = gpd.GeoSeries([], crs="EPSG:3857")
        
        result = renderer.render(viewport, geometries, 0, 0)
        assert result == ""
        
        result = renderer.render(viewport, geometries, 0, 10)
        assert result == ""
        
        result = renderer.render(viewport, geometries, 10, 0)
        assert result == ""

