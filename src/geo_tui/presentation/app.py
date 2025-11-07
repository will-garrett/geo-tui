"""Main Textual application."""

from pathlib import Path
from typing import Optional

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Vertical
from textual.widgets import Header, Footer

from geo_tui.application.services.map_service import MapService
from geo_tui.application.services.navigation_service import NavigationService
from geo_tui.application.use_cases.load_map import LoadMapUseCase
from geo_tui.domain.entities.viewport import Viewport
from geo_tui.infrastructure.geometry.geojson_loader import GeoJSONLoader
from geo_tui.infrastructure.geometry.geopandas_loader import GeoPandasLoader
from geo_tui.infrastructure.projection.mercator_projection import MercatorProjection
from geo_tui.infrastructure.rendering.braille_renderer import BrailleRenderer
from geo_tui.presentation.widgets.map_widget import MapWidget
from geo_tui.presentation.widgets.map_header import MapHeader
from geo_tui.presentation.widgets.map_status_bar import MapStatusBar


class MapApp(App):
    """Main application for the geo-tui map viewer."""
    
    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit", priority=True),
    ]
    
    CSS = """
    Screen {
        background: $surface;
        overflow: hidden;
        layout: vertical;
    }
    
    Vertical {
        width: 100%;
        height: 1fr;
        overflow: hidden;
    }
    
    #header-container {
        height: 1;
        width: 100%;
        background: #1e1e1e;
        border-bottom: solid #444;
        overflow: hidden;
    }
    
    MapHeader {
        width: 100%;
        height: 1;
        content-align: left middle;
        padding: 0 1;
        text-style: bold;
        color: #ffffff;
        background: #1e1e1e;
        overflow: hidden;
        text-opacity: 100%;
    }
    
    MapWidget {
        width: 100%;
        height: 1fr;
        overflow: hidden;
        scrollbar-gutter: stable;
        min-height: 1;
    }
    
    Footer {
        height: 1;
        background: #1e1e1e;
        color: #888888;
        border-top: solid #444;
        overflow: hidden;
        text-opacity: 100%;
    }
    """
    
    def __init__(self, data_source: Optional[Path] = None, **kwargs):
        """Initialize the application.
        
        Args:
            data_source: Optional path to GeoJSON file
            **kwargs: Additional arguments for App
        """
        super().__init__(**kwargs)
        
        # Initialize infrastructure
        # Try to use GeoPandas if available, otherwise use simple GeoJSON loader
        try:
            if data_source:
                geometry_loader = GeoPandasLoader(data_source)
            else:
                # Try GeoPandas for Natural Earth dataset
                geometry_loader = GeoPandasLoader()
        except (ImportError, ValueError) as e:
            # Fall back to simple GeoJSON loader
            if not data_source:
                # Default to globe.geo.json if available
                default_path = Path(__file__).parent.parent.parent.parent / "data" / "globe.geo.json"
                if default_path.exists():
                    data_source = default_path
                else:
                    raise ValueError(
                        "No data source provided and geopandas not available. "
                        "Either install geopandas (uv sync --extra geopandas) "
                        "or provide a GeoJSON file path."
                    ) from e
            geometry_loader = GeoJSONLoader(data_source)
        
        projection = MercatorProjection()
        renderer = BrailleRenderer()
        
        # Initialize domain with default viewport
        # We'll adjust the zoom based on terminal size in on_mount
        viewport = Viewport(0.0, 0.0, 1_000_000.0)
        
        # Initialize services
        self.map_service = MapService(geometry_loader, projection, renderer)
        self.navigation_service = NavigationService(viewport)
        self.projection = projection
        self.viewport = viewport
        
        # Load map data
        load_use_case = LoadMapUseCase(self.map_service)
        load_use_case.execute()
    
    def on_mount(self) -> None:
        """Called when the app is mounted."""
        # Adjust viewport to fit terminal size after screen is ready
        # Use a small delay to ensure geometries are loaded
        self.set_timer(0.1, self._adjust_viewport)
    
    def _adjust_viewport(self) -> None:
        """Adjust viewport to fit terminal size and globe data."""
        try:
            screen = self.screen
            if screen and screen.size.width > 0 and screen.size.height > 0:
                # Get geometry bounds to calculate proper zoom
                bounds = self.map_service.get_geometry_bounds()
                
                if bounds:
                    minx, miny, maxx, maxy = bounds
                    # Calculate the width of the globe data in meters (Web Mercator)
                    globe_width_m = maxx - minx
                    globe_height_m = maxy - miny
                    
                    # Get available screen size (subtract header and footer)
                    # Header: 1 line, Footer: 1 line
                    available_height = screen.size.height - 2
                    available_width = screen.size.width
                    
                    # Terminal dimensions in braille subpixels
                    # Each braille character is 2x4 subpixels
                    terminal_width_px = available_width * 2
                    terminal_height_px = available_height * 4
                    
                    # Add small padding (5%) so globe isn't right at edges
                    padding_factor = 1.05
                    
                    # Calculate meters per pixel to fit the globe width
                    if terminal_width_px > 0:
                        meters_per_pixel_x = (globe_width_m * padding_factor) / terminal_width_px
                    else:
                        meters_per_pixel_x = 1_000_000.0
                    
                    # Also consider height to ensure globe fits vertically
                    if terminal_height_px > 0:
                        meters_per_pixel_y = (globe_height_m * padding_factor) / terminal_height_px
                    else:
                        meters_per_pixel_y = 1_000_000.0
                    
                    # Use the smaller value to ensure the globe fits in both dimensions
                    # (smaller meters_per_pixel = more zoomed in)
                    meters_per_pixel = min(meters_per_pixel_x, meters_per_pixel_y)
                    
                    # Center the viewport on the globe
                    center_x = (minx + maxx) / 2
                    center_y = (miny + maxy) / 2
                    
                    self.viewport.center_x = center_x
                    self.viewport.center_y = center_y
                    self.viewport.meters_per_pixel = meters_per_pixel
                    
                    # Refresh map widget and header after viewport adjustment
                    try:
                        map_widget = self.query_one("MapWidget")
                        map_widget.refresh()
                    except Exception:
                        pass
                    self.call_after_refresh(self._update_header)
                else:
                    # Fallback: use earth circumference if bounds not available
                    earth_circumference = 40075017.0
                    terminal_width_px = screen.size.width * 2
                    if terminal_width_px > 0:
                        meters_per_pixel = earth_circumference / terminal_width_px
                        self.viewport.meters_per_pixel = meters_per_pixel
                        self.call_after_refresh(self._update_header)
        except Exception as e:
            # Silently fail - viewport will use default values
            pass
    
    def _update_header(self) -> None:
        """Update the header widget."""
        try:
            header = self.query_one("MapHeader")
            # Force update by setting viewport (this will trigger _update_content)
            header.viewport = self.viewport
        except Exception:
            pass
    
    def compose(self) -> ComposeResult:
        """Compose the application UI.
        
        Yields:
            Widgets to display
        """
        # Wrap everything in a Vertical container for proper layout
        with Vertical():
            # Custom header for map info (styled like Neovim)
            with Container(id="header-container"):
                header = MapHeader(self.viewport, self.projection)
                yield header
            
            # Map widget takes remaining space
            map_widget = MapWidget(
                self.map_service,
                self.navigation_service,
                self.viewport
            )
            yield map_widget
        
        # Use Textual's Footer widget - it will automatically show bindings from focused widget
        # Footer should be at the Screen level, not inside Vertical
        yield Footer()
    
    def action_quit(self) -> None:
        """Quit the application."""
        self.exit()
    
    def on_ready(self) -> None:
        """Called when the app is ready."""
        # Ensure map widget is focused so Footer shows its bindings
        try:
            map_widget = self.query_one("MapWidget")
            map_widget.focus()
            map_widget.refresh()
        except Exception:
            pass
        # Ensure header is updated after everything is ready
        self.call_after_refresh(self._update_header)

