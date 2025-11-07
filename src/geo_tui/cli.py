"""Command-line interface entry point for geo-tui."""

import sys
from pathlib import Path

from geo_tui.presentation.app import MapApp


def main():
    """Main entry point for the geo-tui command."""
    # Check if a data file is provided as command line argument
    data_source = None
    if len(sys.argv) > 1:
        data_path = Path(sys.argv[1])
        if data_path.exists():
            data_source = data_path
        else:
            print(f"Warning: Data file not found: {data_path}", file=sys.stderr)
            print("Trying default data sources...", file=sys.stderr)
    
    # Use the globe.geo.json file if it exists and no source specified
    if data_source is None:
        # Try to find data/globe.geo.json relative to the installed package
        # or in the current working directory
        possible_paths = [
            Path(__file__).parent.parent.parent / "data" / "globe.geo.json",
            Path.cwd() / "data" / "globe.geo.json",
        ]
        for path in possible_paths:
            if path.exists():
                data_source = path
                break
    
    try:
        app = MapApp(data_source=data_source)
        app.run()
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nExiting...", file=sys.stderr)
        sys.exit(0)

