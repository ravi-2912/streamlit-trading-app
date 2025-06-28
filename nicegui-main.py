import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ng.routers import Router
from ng  import get_state, header, left_drawer, right_drawer

from nicegui import ui


@ui.page("/")
@ui.page("/{_:path}")
def main():
    router = Router()

    state = get_state()

    ld = left_drawer(router)
    rd = right_drawer()
    header(ld, rd)



    for item in state["menu_items"].values():
        router.add(item["path"])(item["show"])


    router.frame().classes("w-full p-5 pt-0 gap-0")


ui.run(port=8123)
