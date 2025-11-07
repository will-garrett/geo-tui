# Installation Guide

This guide explains how to install geo-tui with `uv`.

## Quick Start

### Basic Installation (without geopandas)

For basic usage with GeoJSON files:

```bash
uv sync
```

This installs the core dependencies (textual, shapely, pyproj) without geopandas.

### Full Installation (with geopandas)

For full functionality including Natural Earth dataset support:

```bash
uv sync --extra geopandas
```

**Note**: This requires system-level GDAL libraries. On Arch Linux:

```bash
sudo pacman -S gdal
```

On Ubuntu/Debian:

```bash
sudo apt-get install gdal-bin libgdal-dev
```

On macOS (with Homebrew):

```bash
brew install gdal
```

## Running the Application

### Using the installed command (recommended):

```bash
# With a GeoJSON file (no geopandas needed)
uv run geo-tui data/globe.geo.json

# Or automatically find data/globe.geo.json
uv run geo-tui
```

### With geopandas (uses Natural Earth dataset):

```bash
uv sync --extra geopandas
uv run geo-tui
```

### Alternative: Direct Python execution

```bash
uv run python main.py data/globe.geo.json
```

## Troubleshooting

### GDAL not found

If you see `gdal-config: No such file or directory`, install GDAL system libraries (see above).

### Python 3.14 compatibility

Some packages may have compatibility issues with Python 3.14. Consider using Python 3.11 or 3.12:

```bash
uv python install 3.12
uv venv --python 3.12
uv sync
```

## Development Setup

For development with tests:

```bash
uv sync --extra dev
```

Or for everything:

```bash
uv sync --extra all
```

