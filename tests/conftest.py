"""Pytest configuration and fixtures."""

import pytest
from pathlib import Path

from geo_tui.domain.entities.viewport import Viewport
from geo_tui.infrastructure.projection.mercator_projection import MercatorProjection
from geo_tui.infrastructure.geometry.geopandas_loader import GeoPandasLoader
from geo_tui.infrastructure.rendering.braille_renderer import BrailleRenderer
from geo_tui.application.services.map_service import MapService
from geo_tui.application.services.navigation_service import NavigationService


@pytest.fixture
def viewport():
    """Create a test viewport."""
    return Viewport(0.0, 0.0, 1_000_000.0)


@pytest.fixture
def projection():
    """Create a projection instance."""
    return MercatorProjection()


@pytest.fixture
def geometry_loader():
    """Create a geometry loader."""
    return GeoPandasLoader()


@pytest.fixture
def renderer():
    """Create a renderer instance."""
    return BrailleRenderer()


@pytest.fixture
def map_service(geometry_loader, projection, renderer):
    """Create a map service instance."""
    return MapService(geometry_loader, projection, renderer)


@pytest.fixture
def navigation_service(viewport):
    """Create a navigation service instance."""
    return NavigationService(viewport)

