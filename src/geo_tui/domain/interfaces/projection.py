"""Projection interface for coordinate transformations."""

from abc import ABC, abstractmethod
from typing import Tuple


class Projection(ABC):
    """Interface for coordinate projection systems."""
    
    @abstractmethod
    def project(self, longitude: float, latitude: float) -> Tuple[float, float]:
        """Project lon/lat to projected coordinates.
        
        Args:
            longitude: Longitude in degrees (WGS84)
            latitude: Latitude in degrees (WGS84)
            
        Returns:
            Tuple of (x, y) in projected coordinate system
        """
        pass
    
    @abstractmethod
    def unproject(self, x: float, y: float) -> Tuple[float, float]:
        """Unproject coordinates back to lon/lat.
        
        Args:
            x: X coordinate in projected system
            y: Y coordinate in projected system
            
        Returns:
            Tuple of (longitude, latitude) in degrees
        """
        pass

