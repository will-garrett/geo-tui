"""Service for managing map state and operations."""

from typing import Any, List, Optional

try:
    import geopandas as gpd
    GEOPANDAS_AVAILABLE = True
except ImportError:
    GEOPANDAS_AVAILABLE = False

from shapely.geometry import LineString
from pyproj import Transformer

from geo_tui.domain.entities.map_data import MapPoint, MapDataUpdate
from geo_tui.domain.entities.viewport import Viewport
from geo_tui.domain.interfaces.geometry_loader import GeometryLoader
from geo_tui.domain.interfaces.projection import Projection
from geo_tui.domain.interfaces.renderer import Renderer


class MapService:
    """Service for managing map operations."""
    
    def __init__(
        self,
        geometry_loader: GeometryLoader,
        projection: Projection,
        renderer: Renderer
    ):
        """Initialize the map service.
        
        Args:
            geometry_loader: Loader for geographic geometries
            projection: Coordinate projection system
            renderer: Renderer for map display
        """
        self.geometry_loader = geometry_loader
        self.projection = projection
        self.renderer = renderer
        self._geometries: Any = None
        self._projected_geometries: Any = None
        self._points: List[MapPoint] = []
        self._projector = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
    
    def load_geometries(self) -> None:
        """Load and project geometries."""
        geometries = self.geometry_loader.load()
        self._geometries = geometries
        
        # Project to Web Mercator
        if GEOPANDAS_AVAILABLE and isinstance(geometries, gpd.GeoSeries):
            # Use GeoPandas projection
            self._projected_geometries = geometries.to_crs("EPSG:3857")
        else:
            # Project list of LineStrings manually
            projected_lines = []
            for line in geometries:
                if isinstance(line, LineString):
                    # Transform coordinates
                    coords = list(line.coords)
                    projected_coords = [
                        self._projector.transform(lon, lat) for lon, lat in coords
                    ]
                    projected_lines.append(LineString(projected_coords))
            self._projected_geometries = projected_lines
    
    def get_geometries(self) -> Any:
        """Get the loaded geometries.
        
        Returns:
            Projected geometries (GeoSeries or list), or None if not loaded
        """
        return self._projected_geometries
    
    def get_geometry_bounds(self) -> Optional[tuple]:
        """Get the bounds of the loaded geometries in projected coordinates.
        
        Returns:
            Tuple of (minx, miny, maxx, maxy) in projected coordinates, or None if no geometries
        """
        if self._projected_geometries is None:
            return None
        
        if GEOPANDAS_AVAILABLE and isinstance(self._projected_geometries, gpd.GeoSeries):
            # Use GeoPandas bounds
            bounds = self._projected_geometries.total_bounds
            return (bounds[0], bounds[1], bounds[2], bounds[3])
        else:
            # Calculate bounds from list of LineStrings
            if not self._projected_geometries:
                return None
            
            # Get all coordinates
            all_coords = []
            for geom in self._projected_geometries:
                if isinstance(geom, LineString):
                    all_coords.extend(geom.coords)
            
            if not all_coords:
                return None
            
            # Calculate bounds
            xs = [x for x, y in all_coords]
            ys = [y for x, y in all_coords]
            return (min(xs), min(ys), max(xs), max(ys))
    
    def add_point(self, point: MapPoint) -> None:
        """Add a point to the map.
        
        Args:
            point: Point to add
        """
        self._points.append(point)
    
    def update_map_data(self, update: MapDataUpdate) -> None:
        """Update map data at a specific location.
        
        Args:
            update: Map data update
        """
        point = update.to_point()
        # Check if point already exists and update, or add new
        for i, existing_point in enumerate(self._points):
            if (abs(existing_point.longitude - point.longitude) < 0.0001 and
                abs(existing_point.latitude - point.latitude) < 0.0001):
                self._points[i] = point
                return
        self._points.append(point)
    
    def get_points(self) -> List[MapPoint]:
        """Get all points on the map.
        
        Returns:
            List of points
        """
        return self._points.copy()
    
    def clear_points(self) -> None:
        """Clear all points from the map."""
        self._points.clear()
    
    def render(
        self,
        viewport: Viewport,
        width: int,
        height: int
    ) -> str:
        """Render the map.
        
        Args:
            viewport: Current viewport
            width: Display width
            height: Display height
            
        Returns:
            Rendered map as string
        """
        if self._projected_geometries is None:
            return ""
        
        # Filter points by viewport
        visible_points = self._get_visible_points(viewport, width, height)
        
        return self.renderer.render(
            viewport=viewport,
            geometries=self._projected_geometries,
            width=width,
            height=height,
            points=visible_points
        )
    
    def _get_visible_points(
        self,
        viewport: Viewport,
        width: int,
        height: int
    ) -> List[MapPoint]:
        """Get points visible in the current viewport.
        
        Args:
            viewport: Current viewport
            width: Display width
            height: Display height
            
        Returns:
            List of visible points
        """
        if not self._points:
            return []
        
        minx, miny, maxx, maxy = viewport.get_bounds(width * 2, height * 4)
        visible = []
        
        for point in self._points:
            x, y = self.projection.project(point.longitude, point.latitude)
            if minx <= x <= maxx and miny <= y <= maxy:
                visible.append(point)
        
        return visible

