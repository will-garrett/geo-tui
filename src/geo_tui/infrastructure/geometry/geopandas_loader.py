"""GeoPandas-based geometry loader (requires geopandas optional dependency)."""

from pathlib import Path
from typing import Optional, Union

try:
    import geopandas as gpd
    GEOPANDAS_AVAILABLE = True
except ImportError:
    GEOPANDAS_AVAILABLE = False

from shapely.geometry import LineString, MultiLineString, Polygon, MultiPolygon
from shapely.ops import unary_union

from geo_tui.domain.interfaces.geometry_loader import GeometryLoader


class GeoPandasLoader(GeometryLoader):
    """Loads geometries using GeoPandas (requires geopandas package)."""
    
    def __init__(self, data_source: Optional[Union[str, Path]] = None):
        """Initialize the loader.
        
        Args:
            data_source: Path to GeoJSON file, or None to use Natural Earth lowres
            
        Raises:
            ImportError: If geopandas is not installed
        """
        if not GEOPANDAS_AVAILABLE:
            raise ImportError(
                "geopandas is required for GeoPandasLoader. "
                "Install it with: uv sync --extra geopandas"
            )
        self.data_source = data_source
    
    def load(self) -> gpd.GeoSeries:
        """Load geographic geometries.
        
        Returns:
            GeoSeries containing coastline geometries
        """
        if self.data_source:
            # Load from file
            gdf = gpd.read_file(self.data_source)
            # Convert polygons to lines (coastlines)
            lines = []
            for geom in gdf.geometry:
                if isinstance(geom, Polygon):
                    lines.append(LineString(geom.exterior.coords))
                elif isinstance(geom, MultiPolygon):
                    for g in geom.geoms:
                        lines.append(LineString(g.exterior.coords))
            multiline = unary_union(lines)
            return gpd.GeoSeries([multiline], crs="EPSG:4326")
        else:
            # Use Natural Earth lowres dataset
            world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
            lines = []
            for geom in world.geometry:
                if isinstance(geom, Polygon):
                    lines.append(LineString(geom.exterior.coords))
                elif isinstance(geom, MultiPolygon):
                    for g in geom.geoms:
                        lines.append(LineString(g.exterior.coords))
            multiline = unary_union(lines)
            return gpd.GeoSeries([multiline], crs="EPSG:4326")

