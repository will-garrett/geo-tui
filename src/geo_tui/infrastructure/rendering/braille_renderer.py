"""Braille-based renderer for high-resolution text maps."""

from typing import Any, List, Optional, Tuple

try:
    import geopandas as gpd
    GEOPANDAS_AVAILABLE = True
except ImportError:
    GEOPANDAS_AVAILABLE = False

from shapely.affinity import affine_transform
from shapely.geometry import LineString, MultiLineString

from geo_tui.domain.entities.map_data import MapPoint
from geo_tui.domain.entities.viewport import Viewport
from geo_tui.domain.interfaces.renderer import Renderer

# Braille character mapping
_BRAILLE_BASE = 0x2800
_DOT_BIT = {
    (0, 0): 1, (0, 1): 2, (0, 2): 4, (0, 3): 64,
    (1, 0): 8, (1, 1): 16, (1, 2): 32, (1, 3): 128
}


def _empty_braille_grid(cols: int, rows: int) -> List[List[int]]:
    """Create an empty braille grid.
    
    Args:
        cols: Number of columns (braille cells)
        rows: Number of rows (braille cells)
        
    Returns:
        2D list of bitmasks
    """
    return [[0 for _ in range(cols)] for __ in range(rows)]


def _set_subpixel(grid: List[List[int]], col: int, row: int, sx: int, sy: int) -> None:
    """Set a subpixel in the braille grid.
    
    Args:
        grid: Braille grid
        col: Column (braille cell)
        row: Row (braille cell)
        sx: Subpixel x (0 or 1)
        sy: Subpixel y (0-3)
    """
    if 0 <= row < len(grid) and 0 <= col < len(grid[0]):
        grid[row][col] |= _DOT_BIT[(sx, sy)]


def _rasterize_line_to_braille(
    grid: List[List[int]],
    p0: Tuple[float, float],
    p1: Tuple[float, float],
    width_px: int,
    height_px: int
) -> None:
    """Draw a line using Bresenham's algorithm.
    
    Args:
        grid: Braille grid
        p0: Start point (x, y) in pixel coordinates
        p1: End point (x, y) in pixel coordinates
        width_px: Width in subpixels
        height_px: Height in subpixels
    """
    x0, y0 = int(p0[0]), int(p0[1])
    x1, y1 = int(p1[0]), int(p1[1])
    
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    
    while True:
        if 0 <= x0 < width_px and 0 <= y0 < height_px:
            col = x0 // 2
            row = y0 // 4
            sx_sub = x0 % 2
            sy_sub = y0 % 4
            _set_subpixel(grid, col, row, sx_sub, sy_sub)
        
        if x0 == x1 and y0 == y1:
            break
        
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


def _braille_grid_to_str(grid: List[List[int]]) -> str:
    """Convert braille grid to string.
    
    Args:
        grid: Braille grid
        
    Returns:
        String representation
    """
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    lines = []
    for r in range(rows):
        line = []
        for c in range(cols):
            code = _BRAILLE_BASE + grid[r][c]
            line.append(chr(code) if grid[r][c] else " ")
        lines.append("".join(line))
    return "\n".join(lines)


class BrailleRenderer(Renderer):
    """Renderer using Unicode Braille characters for high resolution."""
    
    def render(
        self,
        viewport: Viewport,
        geometries: Any,
        width: int,
        height: int,
        points: Optional[List[MapPoint]] = None
    ) -> str:
        """Render the map using Braille characters.
        
        Args:
            viewport: Current viewport
            geometries: GeoSeries containing geometries
            width: Display width in characters
            height: Display height in characters
            points: Optional list of points to highlight
            
        Returns:
            String representation of the rendered map
        """
        if width <= 0 or height <= 0:
            return ""
        
        # Build braille grid
        cols, rows = width, height
        grid = _empty_braille_grid(cols, rows)
        
        # Subpixel resolution (2x4 per braille cell)
        px_w = cols * 2
        px_h = rows * 4
        
        # Get viewport bounds
        minx, miny, maxx, maxy = viewport.get_bounds(px_w, px_h)
        
        # Simplify tolerance based on zoom
        tol = max(viewport.meters_per_pixel * 1.5, 500.0)
        
        # Handle both GeoPandas GeoSeries and list of geometries
        if GEOPANDAS_AVAILABLE and isinstance(geometries, gpd.GeoSeries):
            # Filter geometries by viewport using spatial index
            if hasattr(geometries, 'sindex') and geometries.sindex is not None:
                candidate_idx = list(geometries.sindex.intersection((minx, miny, maxx, maxy)))
                if not candidate_idx:
                    return ""
                series = geometries.iloc[candidate_idx]
            else:
                series = geometries
            
            # Clip to viewport (optional optimization)
            try:
                viewport_poly = gpd.GeoSeries.from_bbox((minx, miny, maxx, maxy))
                series = series.clip(viewport_poly.iloc[0])
            except Exception:
                pass
            
            # Simplify geometries
            simplified = series.simplify(tol, preserve_topology=True)
            geometries_to_draw = simplified
        else:
            # Handle list of LineString geometries
            from shapely.geometry import box
            viewport_box = box(minx, miny, maxx, maxy)
            geometries_to_draw = [
                geom for geom in geometries
                if isinstance(geom, LineString) and geom.intersects(viewport_box)
            ]
        
        # Build affine transform from Mercator -> pixel space
        # Pixel x = (X - minx) / meters_per_px
        # Pixel y = (maxy - Y) / meters_per_px (invert y)
        a = 1.0 / viewport.meters_per_pixel
        e = -1.0 / viewport.meters_per_pixel
        b = d = 0.0
        c = -minx * a
        f = maxy * (-e)  # because e is negative
        xform = [a, b, d, e, c, f]
        
        # Draw geometries
        for geom in geometries_to_draw:
            if geom.is_empty:
                continue
            
            g = affine_transform(geom, xform)
            
            def draw_lines(lines):
                for line in lines:
                    coords = list(line.coords)
                    for i in range(len(coords) - 1):
                        x0, y0 = coords[i]
                        x1, y1 = coords[i + 1]
                        _rasterize_line_to_braille(
                            grid, (x0, y0), (x1, y1),
                            width_px=px_w, height_px=px_h
                        )
            
            if isinstance(g, LineString):
                draw_lines([g])
            elif isinstance(g, MultiLineString):
                draw_lines(g.geoms)
        
        # Draw points if provided
        # Note: Points rendering requires projection, which should be passed to renderer
        # For now, points are handled by the map service filtering
        # Full point rendering can be added as an enhancement
        
        return _braille_grid_to_str(grid)

