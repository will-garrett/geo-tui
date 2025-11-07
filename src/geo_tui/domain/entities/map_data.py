"""Map data entity representing geographic features."""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class MapPoint:
    """Represents a point on the map with associated data."""
    
    longitude: float
    """Longitude in degrees (WGS84)."""
    
    latitude: float
    """Latitude in degrees (WGS84)."""
    
    data: Optional[Dict[str, Any]] = None
    """Optional data associated with this point."""
    
    def __post_init__(self):
        """Validate coordinates."""
        if not -180 <= self.longitude <= 180:
            raise ValueError(f"Longitude must be between -180 and 180, got {self.longitude}")
        if not -90 <= self.latitude <= 90:
            raise ValueError(f"Latitude must be between -90 and 90, got {self.latitude}")


@dataclass
class MapDataUpdate:
    """Represents an update to map data at a specific location."""
    
    longitude: float
    """Longitude in degrees (WGS84)."""
    
    latitude: float
    """Latitude in degrees (WGS84)."""
    
    data: Dict[str, Any]
    """Data to associate with this location."""
    
    def to_point(self) -> MapPoint:
        """Convert to a MapPoint."""
        return MapPoint(
            longitude=self.longitude,
            latitude=self.latitude,
            data=self.data
        )

