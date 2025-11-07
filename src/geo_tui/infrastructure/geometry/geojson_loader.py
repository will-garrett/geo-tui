"""Simple GeoJSON loader that doesn't require geopandas."""

import json
from pathlib import Path
from typing import Optional, Union

from shapely.geometry import LineString, MultiLineString, Polygon, MultiPolygon, shape
from shapely.ops import unary_union

from geo_tui.domain.interfaces.geometry_loader import GeometryLoader


class GeoJSONLoader(GeometryLoader):
    """Loads geometries from GeoJSON files without requiring geopandas."""
    
    def __init__(self, data_source: Optional[Union[str, Path]] = None):
        """Initialize the loader.
        
        Args:
            data_source: Path to GeoJSON file
        """
        self.data_source = data_source
    
    def load(self):
        """Load geographic geometries from GeoJSON.
        
        Returns:
            List of LineString geometries representing coastlines
        """
        if not self.data_source:
            raise ValueError("GeoJSONLoader requires a data_source path")
        
        path = Path(self.data_source)
        if not path.exists():
            raise FileNotFoundError(f"GeoJSON file not found: {path}")
        
        with open(path, 'r') as f:
            geojson_data = json.load(f)
        
        lines = []
        
        # Process GeoJSON features
        if geojson_data.get('type') == 'FeatureCollection':
            features = geojson_data.get('features', [])
        elif geojson_data.get('type') == 'Feature':
            features = [geojson_data]
        else:
            # Single geometry
            geom = shape(geojson_data)
            if isinstance(geom, (Polygon, MultiPolygon)):
                if isinstance(geom, Polygon):
                    lines.append(LineString(geom.exterior.coords))
                else:
                    for g in geom.geoms:
                        lines.append(LineString(g.exterior.coords))
            elif isinstance(geom, (LineString, MultiLineString)):
                if isinstance(geom, LineString):
                    lines.append(geom)
                else:
                    lines.extend(geom.geoms)
            return lines
        
        # Process each feature
        for feature in features:
            geometry = feature.get('geometry')
            if not geometry:
                continue
            
            geom = shape(geometry)
            
            # Convert polygons to lines (coastlines)
            if isinstance(geom, Polygon):
                lines.append(LineString(geom.exterior.coords))
            elif isinstance(geom, MultiPolygon):
                for g in geom.geoms:
                    lines.append(LineString(g.exterior.coords))
            elif isinstance(geom, LineString):
                lines.append(geom)
            elif isinstance(geom, MultiLineString):
                lines.extend(geom.geoms)
        
        return lines

