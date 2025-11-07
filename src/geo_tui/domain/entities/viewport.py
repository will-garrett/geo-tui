"""Viewport entity representing the current map view."""

from dataclasses import dataclass
from typing import Tuple


@dataclass
class Viewport:
    """Represents the current viewport of the map.
    
    The viewport defines what portion of the map is currently visible.
    Coordinates are in the projected coordinate system (e.g., Web Mercator meters).
    """
    
    center_x: float
    """X coordinate of viewport center in projected units."""
    
    center_y: float
    """Y coordinate of viewport center in projected units."""
    
    meters_per_pixel: float
    """Scale factor: meters per pixel at current zoom level."""
    
    def get_bounds(self, width_px: int, height_px: int) -> Tuple[float, float, float, float]:
        """Calculate viewport bounds in projected coordinates.
        
        Args:
            width_px: Viewport width in pixels
            height_px: Viewport height in pixels
            
        Returns:
            Tuple of (minx, miny, maxx, maxy) in projected coordinates
        """
        half_width_m = (width_px * self.meters_per_pixel) / 2
        half_height_m = (height_px * self.meters_per_pixel) / 2
        
        minx = self.center_x - half_width_m
        maxx = self.center_x + half_width_m
        miny = self.center_y - half_height_m
        maxy = self.center_y + half_height_m
        
        return (minx, miny, maxx, maxy)
    
    def pan(self, delta_x: float, delta_y: float) -> None:
        """Pan the viewport by the given deltas.
        
        Args:
            delta_x: Change in X coordinate (in projected units)
            delta_y: Change in Y coordinate (in projected units)
        """
        self.center_x += delta_x
        self.center_y += delta_y
    
    def zoom(self, factor: float) -> None:
        """Zoom the viewport by the given factor.
        
        Args:
            factor: Zoom factor (>1 zooms in, <1 zooms out)
        """
        self.meters_per_pixel *= factor
    
    def reset(self, center_x: float = 0.0, center_y: float = 0.0, 
              meters_per_pixel: float = 1_000_000.0) -> None:
        """Reset viewport to default position and zoom.
        
        Args:
            center_x: X coordinate of center
            center_y: Y coordinate of center
            meters_per_pixel: Initial scale
        """
        self.center_x = center_x
        self.center_y = center_y
        self.meters_per_pixel = meters_per_pixel

