"""Web Mercator projection implementation."""

from typing import Tuple

from pyproj import Transformer

from geo_tui.domain.interfaces.projection import Projection


class MercatorProjection(Projection):
    """Web Mercator (EPSG:3857) projection implementation."""
    
    def __init__(self):
        """Initialize the projection transformers."""
        self._to_mercator = Transformer.from_crs(
            "EPSG:4326", "EPSG:3857", always_xy=True
        )
        self._from_mercator = Transformer.from_crs(
            "EPSG:3857", "EPSG:4326", always_xy=True
        )
    
    def project(self, longitude: float, latitude: float) -> Tuple[float, float]:
        """Project lon/lat to Web Mercator meters.
        
        Args:
            longitude: Longitude in degrees (WGS84)
            latitude: Latitude in degrees (WGS84)
            
        Returns:
            Tuple of (x, y) in Web Mercator meters
        """
        x, y = self._to_mercator.transform(longitude, latitude)
        return (x, y)
    
    def unproject(self, x: float, y: float) -> Tuple[float, float]:
        """Unproject Web Mercator meters back to lon/lat.
        
        Args:
            x: X coordinate in Web Mercator meters
            y: Y coordinate in Web Mercator meters
            
        Returns:
            Tuple of (longitude, latitude) in degrees
        """
        lon, lat = self._from_mercator.transform(x, y)
        return (lon, lat)

