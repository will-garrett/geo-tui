"""Main entry point for geo-tui application."""

import sys
from pathlib import Path

from geo_tui.presentation.app import MapApp


def main():
    """Main entry point."""
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
        default_path = Path(__file__).parent / "data" / "globe.geo.json"
        if default_path.exists():
            data_source = default_path
    
    try:
        app = MapApp(data_source=data_source)
        app.run()
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
