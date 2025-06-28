from typing import Callable
from nicegui import ui

from ng.pages import dashboard
from .state import get_state

from .routers import router

def open_page(key, func, router: router.Router = None):
        state = get_state()
        state["active_page"] = key
        router.open(func)

def on_click(state, key):
    state["active_page"] = key
    for _key, data in state["menu_items"].items():
        if data["object"]:
            if _key == key:
                data["object"].classes("bg-gray-300 text-black", remove="text-grey-14")
            else:
                data["object"].classes("text-grey-14", remove="bg-gray-300 text-black")


def open_dashboard(state, router):
    on_click(state, "dashboard")
    open_page("dashboard", dashboard, router)

def menu_item(key: str, icon: str, label: str, action: Callable, left_drawer: ui.left_drawer = None, router: router.Router = None):
        state = get_state()
        with (
            ui.item()
            .props("clickable ripple")
            .classes("p-3 pl-7 mb-2 text-grey-14")
            .on("click", lambda: open_page(key, action, router))
        ) as item:
            if key == state["active_page"]:
                item.classes("bg-gray-300 text-black", remove="text-grey-14")

            item.on(
                "click",
                lambda: on_click(state, key),
            )
            with ui.item_section().props("avatar").style("min-width: 0;"):
                ui.icon(icon)
            ui.item_section(label).bind_visibility_from(left_drawer.props, "mini")
        return item


def left_drawer(router: router.Router = None):
    state = get_state()
    with (
            ui.left_drawer(top_corner=True, bottom_corner=True)
            .props("bordered")
            .classes("p-0 gap-3 bg-gray-100") as left_drawer
        ):
            with (
                ui.element("div")
                .classes("p-0 w-full nicegui-header mt-3")
                .style("height: 68px;")
            ):
                with (
                    ui.item()
                    .props("clickable")
                    .classes("p-5 text-3xl w-full h-full")
                    .on("click", lambda: open_dashboard(state, router))
                ):
                    with ui.item_section().props("avatar").style("min-width: 0;"):
                        ui.icon("analytics", size="1.5em")
                    ui.item_section("Trading App").bind_visibility_from(left_drawer, "mini")

            with ui.list().classes("text-xl").classes("w-full justify-start items-start"):
                for key, data in state["menu_items"].items():
                    state["menu_items"][key]["object"] = menu_item(
                        key, data["icon"], data["label"], data["show"], left_drawer, router
                    )
            return left_drawer

def left_drawer_collapse(left_drawer: ui.left_drawer = None):
    state = get_state()
    left_drawer.props("mini")
    state["left_drawer_left_arrow_visible"] = False
    state["left_drawer_right_arrow_visible"] = True

def left_drawer_open(left_drawer: ui.left_drawer = None):
    state = get_state()
    left_drawer.props("mini=False")
    state["left_drawer_left_arrow_visible"] = True
    state["left_drawer_right_arrow_visible"] = False
