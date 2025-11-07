"""Header widget for displaying map information."""

from textual.widgets import Static

from geo_tui.domain.entities.viewport import Viewport
from geo_tui.domain.interfaces.projection import Projection


class MapHeader(Static):
    """Header widget displaying map viewport information."""
    
    def __init__(self, viewport: Viewport, projection: Projection, **kwargs):
        """Initialize the header widget.
        
        Args:
            viewport: Viewport to display information for
            projection: Projection for coordinate conversion
            **kwargs: Additional widget arguments
        """
        super().__init__("Loading map...", **kwargs)
        self._viewport = viewport
        self._projection = projection
    
    @property
    def viewport(self) -> Viewport:
        """Get the viewport."""
        return self._viewport
    
    @viewport.setter
    def viewport(self, value: Viewport) -> None:
        """Set the viewport and trigger refresh."""
        # Always update, even if same object (viewport properties may have changed)
        self._viewport = value
        # Use call_after_refresh to ensure app/widget is ready
        if hasattr(self, 'app') and self.app is not None:
            self.call_after_refresh(self._update_content)
        else:
            # If app not ready, try direct update
            try:
                self._update_content()
            except Exception:
                pass
    
    def _update_content(self) -> None:
        """Update the header content."""
        if self._viewport is None or self._projection is None:
            self.update("Loading...")
            return
        
        # Ensure we have access to app
        if not hasattr(self, 'app') or self.app is None:
            return
        
        # Get the map widget to use its actual dimensions
        try:
            map_widget = self.app.query_one("MapWidget")
            if map_widget.size.width > 0 and map_widget.size.height > 0:
                map_width = map_widget.size.width
                map_height = map_widget.size.height
            else:
                raise ValueError("Map widget size not ready")
        except Exception:
            # Fallback to screen dimensions minus header and status bar
            try:
                screen = self.app.screen
                if screen and screen.size.width > 0:
                    map_width = screen.size.width
                    map_height = screen.size.height - 2  # Subtract header and status bar
                else:
                    raise ValueError("Screen size not ready")
            except Exception:
                map_width = 80
                map_height = 22
        
        # Calculate pixel dimensions (braille cells are 2x4 subpixels)
        px_w = map_width * 2
        px_h = map_height * 4
        
        # Get viewport bounds in projected coordinates
        minx, miny, maxx, maxy = self._viewport.get_bounds(px_w, px_h)
        
        # Convert to lat/lon
        top_left_lon, top_left_lat = self._projection.unproject(minx, maxy)
        bottom_right_lon, bottom_right_lat = self._projection.unproject(maxx, miny)
        center_lon, center_lat = self._projection.unproject(
            self._viewport.center_x, self._viewport.center_y
        )
        
        # Calculate zoom level (approximate)
        # Web Mercator: meters_per_pixel at equator
        # Zoom level formula: zoom = log2(earth_circumference / (meters_per_pixel * tile_size))
        earth_circumference = 40075017.0  # meters at equator
        zoom_level = 0.0
        if self._viewport.meters_per_pixel > 0:
            import math
            zoom_level = math.log2(earth_circumference / (self._viewport.meters_per_pixel * 256))
        
        # Format coordinates
        def format_coord(lon: float, lat: float) -> str:
            """Format coordinates nicely."""
            lon_str = f"{lon:.4f}°E" if lon >= 0 else f"{abs(lon):.4f}°W"
            lat_str = f"{lat:.4f}°N" if lat >= 0 else f"{abs(lat):.4f}°S"
            return f"{lat_str}, {lon_str}"
        
        # Build header string
        header_parts = [
            f"Zoom: {zoom_level:.2f}",
            f"Center: {format_coord(center_lon, center_lat)}",
            f"Top-Left: {format_coord(top_left_lon, top_left_lat)}",
            f"Bottom-Right: {format_coord(bottom_right_lon, bottom_right_lat)}",
        ]
        
        header = " | ".join(header_parts)
        
        # Ensure header fits in available width
        available_width = self.size.width if self.size.width > 0 else 80
        if len(header) > available_width:
            # Truncate if too long
            header = header[:available_width - 3] + "..."
        elif len(header) < available_width:
            # Pad if too short
            header = header + " " * (available_width - len(header))
        
        # Update the widget directly - use plain string, CSS will handle styling
        # Ensure we're updating with visible text
        if header.strip():
            self.update(header)
        else:
            self.update("Map Loading...")
    
    def on_mount(self) -> None:
        """Called when widget is mounted."""
        # Update after a brief delay to ensure app is ready
        self.call_after_refresh(self._update_content)
    
    def on_resize(self) -> None:
        """Called when widget is resized."""
        self.call_after_refresh(self._update_content)

