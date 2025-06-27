# from nicegui import ui

# @ui.page('/page_layout')
# def page_layout():
#     ui.label('CONTENT')
#     [ui.label(f'Line {i}') for i in range(100)]
#     with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center justify-between'):
#         ui.label('HEADER')
#         ui.button(on_click=lambda: left_drawer.toggle(), icon='menu').props('flat color=red')
#         ui.button(on_click=lambda: right_drawer.toggle(), icon='menu').props('flat color=white')
#     with ui.left_drawer(top_corner=True, bottom_corner=True, fixed=True).style('background-color: #d7e3f4') as left_drawer:
#         ui.label('LEFT DRAWER')
#     with ui.right_drawer(fixed=False).style('background-color: #ebf1fa').props('bordered') as right_drawer:
#         ui.label('RIGHT DRAWER')
#     with ui.footer().style('background-color: #3874c8'):
#         ui.label('FOOTER')

# ui.link('show page with fancy layout', page_layout)

# ui.run(port=8123)

import os
import sys
from typing import Callable

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from nicequi.router import Router

from nicegui import ui


@ui.page('/')
@ui.page('/{_:path}')
def main():
    router = Router()

    left_drawer_minified = False

    def menu_item(icon: str, label: str, action: Callable):
        with ui.item().props("clickable ripple").classes("p-5 pl-7 bg-gray-200").on('click', lambda: router.open(action)):
            with ui.item_section().props("avatar").style("min-width: 0;"):
                ui.icon(icon)
            ui.item_section(label).bind_visibility_from(left_drawer, 'mini', value=True)

    @router.add('/')
    def show_one():
        ui.markdown('## 🏠 Home')
        ui.label('Content One').classes('text-2xl')
        ui.label('This is the main content area.').classes('text-lg')


    @router.add('/two')
    def show_two():
        ui.markdown("# 🏠 Home")
        ui.label('Content Two').classes('text-2xl')

    @router.add('/three')
    def show_three():
        ui.label('Content Three').classes('text-2xl')

    with ui.left_drawer(top_corner=True, bottom_corner=True).classes("p-0 bg-gray-100") as left_drawer:

        with ui.element('div').classes('p-0 w-full nicegui-header').style('height: 68px;'):

            with ui.item().props("clickable").classes("p-5 text-3xl w-full h-full"):
                with ui.item_section().props("avatar").style("min-width: 0;"):
                    ui.icon('analytics',size='1.5em')
                ui.item_section("Trading App").bind_visibility_from(left_drawer, 'mini', value=True)

        with ui.list().classes("text-xl").classes("w-full justify-start items-start"):
            # menu_item('home', 'Home', show_one)
            # menu_item('send', 'Send', show_two)
            # menu_item('analytics', 'Analytics', show_three)
            with ui.item().props("clickable ripple").classes("p-5 pl-7 bg-gray-200").on('click', lambda: router.open(show_one)):
                with ui.item_section().props("avatar").style("min-width: 0;"):
                    ui.icon('home')
                ui.item_section("Inbox").bind_visibility_from(left_drawer, 'mini', value=True)
            with ui.item().props("clickable ripple").classes("p-5 pl-7 bg-gray-200").on('click', lambda: router.open(show_two)):
                with ui.item_section().props("avatar").style("min-width: 0;"):
                    ui.icon('send')
                ui.item_section("Send").bind_visibility_from(left_drawer, 'mini', value=True)
            with ui.item().props("clickable ripple").classes("p-5 pl-7 bg-gray-200").on('click', lambda: router.open(show_three)):
                with ui.item_section().props("avatar").style("min-width: 0;"):
                    ui.icon('send')
                ui.item_section("Send").bind_visibility_from(left_drawer, 'mini', value=True)

    with ui.right_drawer(top_corner=True, bottom_corner=True).style('background-color: #ebf1fa').props('bordered') as right_drawer:
        ui.label('RIGHT DRAWER')

    with ui.header().classes('items-center justify-between bg-transparent'):
        with ui.element('div').classes('flex items-center gap-2'):
            ui.button(on_click=lambda: left_drawer.props('mini'), icon='keyboard_double_arrow_left').props('flat').classes("text-black").bind_visibility_from(left_drawer, 'mini', value=False)
            ui.button(on_click=lambda: left_drawer.props('mini=False'), icon='keyboard_double_arrow_right').props('flat').classes("text-black").bind_visibility_from(left_drawer, 'mini', value=True)

            ui.label('HEADER')
            ui.label(f"{left_drawer.VALUE_PROP}").classes('text-sm text-gray-500')



    router.frame().classes('w-full p-5 pt-0')


ui.run(port=8123)
