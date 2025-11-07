"""Use case for loading map data."""

from geo_tui.application.services.map_service import MapService


class LoadMapUseCase:
    """Use case for loading map geometries."""
    
    def __init__(self, map_service: MapService):
        """Initialize the use case.
        
        Args:
            map_service: Map service instance
        """
        self.map_service = map_service
    
    def execute(self) -> None:
        """Execute the use case to load map data."""
        self.map_service.load_geometries()

