"""Portlight TUI CSS theme — dark maritime palette."""

APP_CSS = """
Screen {
    background: $surface;
}

#status-sidebar {
    width: 28;
    height: 100%;
    dock: left;
    border-right: thick $primary;
    padding: 1;
    background: $surface-darken-1;
}

#content-area {
    height: 1fr;
    padding: 0 1;
}

#footer-bar {
    dock: bottom;
    height: 1;
    background: $primary-darken-2;
    color: $text;
    padding: 0 1;
}

.tab-label {
    color: $text-muted;
}

.tab-label.active {
    color: $text;
    text-style: bold;
}

#action-bar {
    dock: bottom;
    height: 3;
    padding: 0 1;
    border-top: tall $primary-darken-1;
    background: $surface-darken-1;
}

#input-area {
    dock: bottom;
    height: 3;
    padding: 0 1;
}

.view-panel {
    height: 1fr;
    overflow-y: auto;
}

DataTable {
    height: 1fr;
}

DataTable > .datatable--cursor {
    background: $primary-darken-1;
    color: $text;
}

#combat-you {
    width: 1fr;
    height: auto;
    border: tall $success;
    padding: 1;
}

#combat-enemy {
    width: 1fr;
    height: auto;
    border: tall $error;
    padding: 1;
}

#combat-log {
    height: 1fr;
    overflow-y: auto;
    padding: 0 1;
    border-top: tall $primary-darken-1;
}

.notification {
    dock: bottom;
    height: auto;
    margin: 1 2;
    padding: 1;
    background: $primary-darken-2;
    border: tall $success;
}

#voyage-log {
    height: 1fr;
    overflow-y: auto;
    padding: 0 1;
}

#route-list {
    height: 1fr;
}
"""
