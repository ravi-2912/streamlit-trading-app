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

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from nicequi.router import Router

from nicegui import ui


@ui.page('/')  # normal index page (e.g. the entry point of the app)
@ui.page('/{_:path}')  # all other pages will be handled by the router but must be registered to also show the SPA index page
def main():
    router = Router()

    @router.add('/')
    def show_one():
        ui.label('Content One').classes('text-2xl')

    @router.add('/two')
    def show_two():
        ui.label('Content Two').classes('text-2xl')

    @router.add('/three')
    def show_three():
        ui.label('Content Three').classes('text-2xl')

    # adding some navigation buttons to switch between the different pages
    with ui.row():
        ui.button('One', on_click=lambda: router.open(show_one)).classes('w-32')
        ui.button('Two', on_click=lambda: router.open(show_two)).classes('w-32')
        ui.button('Three', on_click=lambda: router.open(show_three)).classes('w-32')

    # this places the content which should be displayed
    router.frame().classes('w-full p-4 bg-gray-100')


ui.run(port=8123)
