from nicegui import ui

from .state import get_state

def right_drawer():
    state ={
        "width": 300
    }
    def on_width_change(value):
        state["width"] = value
        right_drawer.props(f"width={state['width']}" )

    with ui.right_drawer( bottom_corner=True, elevated=True, bordered=True, value=False).classes("bg-gray-100").props("overlay") as right_drawer:
        ui.button("increase", on_click=lambda: on_width_change(500)).classes("m-2")
        ui.label(f"Width: {state['width']}").classes("m-2").bind_text_from(state, "width", backward=lambda x: f"{x}px")
        return right_drawer
