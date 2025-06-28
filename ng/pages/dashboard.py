from nicegui import ui

def dashboard():
    ui.markdown("## 💻 Dashboard")
    ui.label("Content One").classes("text-2xl")
    ui.label("This is the main content area.").classes("text-lg")
