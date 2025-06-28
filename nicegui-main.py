import os
import sys
from typing import Callable

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from nicequi.router import Router

from nicegui import ui


@ui.page("/")
@ui.page("/{_:path}")
def main():
    router = Router()

    state = {
        "left_drawer_left_arrow_visible": True,
        "left_drawer_right_arrow_visible": False,
        "active_page": "home",
    }

    def left_drawer_collapse():
        left_drawer.props("mini")
        state["left_drawer_left_arrow_visible"] = False
        state["left_drawer_right_arrow_visible"] = True

    def left_drawer_open():
        left_drawer.props("mini=False")
        state["left_drawer_left_arrow_visible"] = True
        state["left_drawer_right_arrow_visible"] = False

    def menu_item(key: str, icon: str, label: str, action: Callable):
        with (
            ui.item()
            .props("clickable ripple")
            .classes("p-3 pl-7 mb-2 text-gre")
            .on("click", lambda: open_page(key, action))
        ) as item:

            def on_click():
                state["active_page"] = key
                for _key, data in state["menu_items"].items():
                    if data["object"]:
                        data["object"].classes(
                            "bg-gray-300" if _key == key else "",
                            remove="bg-gray-300" if _key != key else "",
                        )

            item.on(
                "click",
                on_click,
            )
            with ui.item_section().props("avatar").style("min-width: 0;"):
                ui.icon(icon)
            ui.item_section(label).bind_visibility_from(left_drawer.props, "mini")
        return item

    def open_page(key, func):
        state["active_page"] = key
        router.open(func)

    @router.add("/")
    def show_one():
        ui.markdown("## 🏠 Home")
        ui.label("Content One").classes("text-2xl")
        ui.label("This is the main content area.").classes("text-lg")

    @router.add("/two")
    def show_two():
        ui.markdown("# 🏠 Home")
        ui.label("Content Two").classes("text-2xl")

    @router.add("/three")
    def show_three():
        ui.label("Content Three").classes("text-2xl")

    state["menu_items"] = {
        "dashboard": {
            "show": show_one,
            "object": None,
            "label": "Dashboard",
            "icon": "dashboard",
        },
        "trading": {
            "show": show_one,
            "object": None,
            "label": "Trading",
            "icon": "candlestick_chart",
        },
        "analytics": {
            "show": show_two,
            "object": None,
            "label": "Analytics",
            "icon": "analytics",
        },
        "journal": {
            "show": show_three,
            "object": None,
            "label": "Journal",
            "icon": "description",
        },
        "accounts": {
            "show": show_three,
            "object": None,
            "label": "Accounts",
            "icon": "business_center",
        },
    }

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
                .on("click", lambda: router.open(show_one))
            ):
                with ui.item_section().props("avatar").style("min-width: 0;"):
                    ui.icon("analytics", size="1.5em")
                ui.item_section("Trading App").bind_visibility_from(left_drawer, "mini")

        with ui.list().classes("text-xl").classes("w-full justify-start items-start"):
            for key, data in state["menu_items"].items():
                state["menu_items"][key]["object"] = menu_item(
                    key, data["icon"], data["label"], data["show"]
                )

    with (
        ui.right_drawer(top_corner=True, bottom_corner=True)
        .style("background-color: #ebf1fa")
        .props("bordered") as right_drawer
    ):
        ui.label("RIGHT DRAWER")

    with ui.header().classes("items-center justify-between bg-transparent"):
        with ui.element("div").classes("flex items-center gap-2"):
            ui.button(
                on_click=left_drawer_collapse, icon="keyboard_double_arrow_left"
            ).props("flat").classes("text-grey-6").bind_visibility_from(
                state, "left_drawer_left_arrow_visible"
            )
            ui.button(
                on_click=left_drawer_open, icon="keyboard_double_arrow_right"
            ).props("flat").classes("text-grey-6").bind_visibility_from(
                state, "left_drawer_right_arrow_visible"
            )

    router.frame().classes("w-full p-5 pt-0 gap-0")


ui.run(port=8123)
