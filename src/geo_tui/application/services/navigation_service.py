"""Service for map navigation operations."""

from geo_tui.domain.entities.viewport import Viewport


class NavigationService:
    """Service for handling map navigation."""
    
    def __init__(self, viewport: Viewport):
        """Initialize the navigation service.
        
        Args:
            viewport: Viewport to control
        """
        self.viewport = viewport
    
    def pan_left(self, step: float = 0.2) -> None:
        """Pan the map left.
        
        Args:
            step: Fraction of screen width to pan (default 0.2 = 20%)
        """
        width_px = 100 * 2  # Estimate, will be updated by actual size
        span_x = width_px * self.viewport.meters_per_pixel
        self.viewport.pan(-step * span_x, 0)
    
    def pan_right(self, step: float = 0.2) -> None:
        """Pan the map right.
        
        Args:
            step: Fraction of screen width to pan
        """
        width_px = 100 * 2
        span_x = width_px * self.viewport.meters_per_pixel
        self.viewport.pan(step * span_x, 0)
    
    def pan_up(self, step: float = 0.2) -> None:
        """Pan the map up.
        
        Args:
            step: Fraction of screen height to pan
        """
        height_px = 100 * 4
        span_y = height_px * self.viewport.meters_per_pixel
        self.viewport.pan(0, step * span_y)
    
    def pan_down(self, step: float = 0.2) -> None:
        """Pan the map down.
        
        Args:
            step: Fraction of screen height to pan
        """
        height_px = 100 * 4
        span_y = height_px * self.viewport.meters_per_pixel
        self.viewport.pan(0, -step * span_y)
    
    def pan(self, delta_x: float, delta_y: float) -> None:
        """Pan the map by the given deltas.
        
        Args:
            delta_x: Change in X (in projected units)
            delta_y: Change in Y (in projected units)
        """
        self.viewport.pan(delta_x, delta_y)
    
    def zoom_in(self, factor: float = 0.8) -> None:
        """Zoom in.
        
        Args:
            factor: Zoom factor (< 1.0 zooms in)
        """
        self.viewport.zoom(factor)
    
    def zoom_out(self, factor: float = 1.25) -> None:
        """Zoom out.
        
        Args:
            factor: Zoom factor (> 1.0 zooms out)
        """
        self.viewport.zoom(factor)
    
    def reset(self) -> None:
        """Reset viewport to default position and zoom."""
        self.viewport.reset()

