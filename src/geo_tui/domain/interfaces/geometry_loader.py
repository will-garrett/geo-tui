"""Interface for loading geographic geometries."""

from abc import ABC, abstractmethod
from typing import Any


class GeometryLoader(ABC):
    """Interface for loading geographic geometry data."""
    
    @abstractmethod
    def load(self) -> Any:
        """Load geographic geometries.
        
        Returns:
            Geometry data (format depends on implementation, e.g., GeoDataFrame)
        """
        pass

