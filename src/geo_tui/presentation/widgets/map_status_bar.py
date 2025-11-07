"""Status bar widget for displaying key bindings."""

from textual.widgets import Static


class MapStatusBar(Static):
    """Status bar widget displaying key bindings and shortcuts."""
    
    def __init__(self, **kwargs):
        """Initialize the status bar widget."""
        super().__init__("", **kwargs)
    
    def _update_content(self) -> None:
        """Update the status bar content with key bindings."""
        bindings = [
            "W/A/S/D: Pan",
            "[/]: Zoom",
            "R: Reset",
            "Ctrl+Q: Quit",
        ]
        status_text = "  ".join(bindings)
        
        # Ensure status bar fits in available width
        available_width = self.size.width if self.size.width > 0 else 80
        if len(status_text) > available_width:
            # Truncate if too long
            status_text = status_text[:available_width - 3] + "..."
        elif len(status_text) < available_width:
            # Pad if too short
            status_text = status_text + " " * (available_width - len(status_text))
        
        # Use Rich Text for better rendering
        from rich.text import Text
        text = Text(status_text, style="#888888 on #1e1e1e")
        self.update(text)
    
    def on_mount(self) -> None:
        """Called when widget is mounted."""
        self.call_after_refresh(self._update_content)
    
    def on_resize(self) -> None:
        """Called when widget is resized."""
        self.call_after_refresh(self._update_content)

