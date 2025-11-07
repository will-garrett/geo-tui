"""Map widget for displaying the map."""

from textual.binding import Binding
from textual.widget import Widget
from textual import events

from geo_tui.application.services.map_service import MapService
from geo_tui.application.services.navigation_service import NavigationService
from geo_tui.domain.entities.viewport import Viewport


class MapWidget(Widget):
    """Widget for displaying the interactive map."""
    
    BINDINGS = [
        Binding("a", "pan_left", "Pan Left", show=True),
        Binding("d", "pan_right", "Pan Right", show=True),
        Binding("w", "pan_up", "Pan Up", show=True),
        Binding("s", "pan_down", "Pan Down", show=True),
        Binding("ctrl+q", "quit", "Quit", priority=True, show=True),
        Binding("]", "zoom_in", "Zoom In", show=True),
        Binding("[", "zoom_out", "Zoom Out", show=True),
        Binding("r", "reset", "Reset View", show=True),
    ]
    
    can_focus = True
    
    def __init__(
        self,
        map_service: MapService,
        navigation_service: NavigationService,
        viewport: Viewport
    ):
        """Initialize the map widget.
        
        Args:
            map_service: Service for map operations
            navigation_service: Service for navigation
            viewport: Viewport entity
        """
        super().__init__()
        self.map_service = map_service
        self.navigation_service = navigation_service
        self.viewport = viewport
    
    def on_mount(self) -> None:
        """Called when widget is mounted."""
        # Focus the widget so it can receive key events
        self.focus()
        # Viewport is already initialized by the app
        # Just update the header
        self.call_after_refresh(self._update_header)
    
    def action_pan_left(self) -> None:
        """Pan the map left."""
        step = 0.2
        width = self.size.width
        px_w = width * 2
        span_x = px_w * self.viewport.meters_per_pixel
        self.viewport.pan(-step * span_x, 0)
        self.refresh()
        self._update_header()
    
    def action_pan_right(self) -> None:
        """Pan the map right."""
        step = 0.2
        width = self.size.width
        px_w = width * 2
        span_x = px_w * self.viewport.meters_per_pixel
        self.viewport.pan(step * span_x, 0)
        self.refresh()
        self._update_header()
    
    def action_pan_up(self) -> None:
        """Pan the map up."""
        step = 0.2
        height = self.size.height
        px_h = height * 4
        span_y = px_h * self.viewport.meters_per_pixel
        self.viewport.pan(0, step * span_y)
        self.refresh()
        self._update_header()
    
    def action_pan_down(self) -> None:
        """Pan the map down."""
        step = 0.2
        height = self.size.height
        px_h = height * 4
        span_y = px_h * self.viewport.meters_per_pixel
        self.viewport.pan(0, -step * span_y)
        self.refresh()
        self._update_header()
    
    def action_quit(self) -> None:
        """Quit the application."""
        self.app.exit()
    
    def action_zoom_in(self) -> None:
        """Zoom in."""
        zoom_factor = 0.8
        self.viewport.zoom(zoom_factor)
        self.refresh()
        self._update_header()
    
    def action_zoom_out(self) -> None:
        """Zoom out."""
        zoom_factor = 0.8
        self.viewport.zoom(1.0 / zoom_factor)
        self.refresh()
        self._update_header()
    
    def action_reset(self) -> None:
        """Reset the viewport."""
        self.viewport.reset()
        self.refresh()
        self._update_header()
    
    def on_key(self, event: events.Key) -> None:
        """Handle key events.
        
        Args:
            event: Key event
        """
        # Handle r for reset
        if event.key == "r":
            self.viewport.reset()
            self.refresh()
            self._update_header()
            event.stop()
    
    def _update_header(self) -> None:
        """Update the header widget if it exists."""
        # Find the header widget in the app
        try:
            header = self.app.query_one("MapHeader")
            # Update the viewport reference to trigger header update
            header.viewport = self.viewport
        except Exception:
            # Header not found or not ready yet, ignore
            pass
    
    def render(self) -> str:
        """Render the map.
        
        Returns:
            Rendered map as string
        """
        # Get the actual available size, ensuring we don't exceed container bounds
        width, height = self.size.width, self.size.height
        
        # Ensure we have valid dimensions
        if width <= 0 or height <= 0:
            return ""
        
        # Clamp to reasonable maximums to prevent overflow
        width = min(width, 1000)
        height = min(height, 1000)
        
        # Render the map with constrained dimensions
        rendered = self.map_service.render(self.viewport, width, height)
        
        # Ensure the output doesn't exceed the expected size
        # Split into lines and truncate if necessary
        lines = rendered.split('\n')
        if len(lines) > height:
            lines = lines[:height]
        rendered = '\n'.join(lines)
        
        # Ensure each line doesn't exceed width
        final_lines = []
        for line in lines:
            if len(line) > width:
                line = line[:width]
            final_lines.append(line)
        
        return '\n'.join(final_lines)

