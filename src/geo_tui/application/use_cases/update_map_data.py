"""Use case for updating map data."""

from geo_tui.application.services.map_service import MapService
from geo_tui.domain.entities.map_data import MapDataUpdate


class UpdateMapDataUseCase:
    """Use case for updating map data at a location."""
    
    def __init__(self, map_service: MapService):
        """Initialize the use case.
        
        Args:
            map_service: Map service instance
        """
        self.map_service = map_service
    
    def execute(self, update: MapDataUpdate) -> None:
        """Execute the use case to update map data.
        
        Args:
            update: Map data update
        """
        self.map_service.update_map_data(update)

