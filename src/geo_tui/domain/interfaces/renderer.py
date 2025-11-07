"""Interface for rendering map data."""

from abc import ABC, abstractmethod
from typing import Any, List, Optional

from ..entities.map_data import MapPoint
from ..entities.viewport import Viewport


class Renderer(ABC):
    """Interface for rendering map data to display format."""
    
    @abstractmethod
    def render(
        self,
        viewport: Viewport,
        geometries: Any,
        width: int,
        height: int,
        points: Optional[List[MapPoint]] = None
    ) -> str:
        """Render the map to a string representation.
        
        Args:
            viewport: Current viewport
            geometries: Geographic geometries to render
            width: Display width in characters
            height: Display height in characters
            points: Optional list of points to highlight
            
        Returns:
            String representation of the rendered map
        """
        pass

