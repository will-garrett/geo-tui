"""Use case for navigating the map."""

from geo_tui.application.services.navigation_service import NavigationService


class NavigateMapUseCase:
    """Use case for map navigation."""
    
    def __init__(self, navigation_service: NavigationService):
        """Initialize the use case.
        
        Args:
            navigation_service: Navigation service instance
        """
        self.navigation_service = navigation_service
    
    def pan_left(self, step: float = 0.2) -> None:
        """Pan left."""
        self.navigation_service.pan_left(step)
    
    def pan_right(self, step: float = 0.2) -> None:
        """Pan right."""
        self.navigation_service.pan_right(step)
    
    def pan_up(self, step: float = 0.2) -> None:
        """Pan up."""
        self.navigation_service.pan_up(step)
    
    def pan_down(self, step: float = 0.2) -> None:
        """Pan down."""
        self.navigation_service.pan_down(step)
    
    def zoom_in(self, factor: float = 0.8) -> None:
        """Zoom in."""
        self.navigation_service.zoom_in(factor)
    
    def zoom_out(self, factor: float = 1.25) -> None:
        """Zoom out."""
        self.navigation_service.zoom_out(factor)
    
    def reset(self) -> None:
        """Reset viewport."""
        self.navigation_service.reset()

