from nicegui import ui

def accounts():
    with ui.column().classes("w-full h-full border text-lg"):
        ui.markdown("## 💼 Accounts")
        ui.label("Manage your trading accounts")
        ui.space()
        grid = ui.aggrid({
            'defaultColDef': {'flex': 1},
            'columnDefs': [
                {'headerName': 'Name', 'field': 'name'},
                {'headerName': 'Age', 'field': 'age'},
                {'headerName': 'Parent', 'field': 'parent', 'hide': True},
            ],
            'rowData': [
                {'name': 'Alice', 'age': 18, 'parent': 'David'},
                {'name': 'Bob', 'age': 21, 'parent': 'Eve'},
                {'name': 'Carol', 'age': 42, 'parent': 'Frank'},
            ],
            'rowSelection': 'multiple',
        }).classes('max-h-40')

        def update():
            grid.options['rowData'][0]['age'] += 1
            grid.update()

        ui.button('Update', on_click=update)
        ui.button('Select all', on_click=lambda: grid.run_grid_method('selectAll'))
        ui.button('Show parent', on_click=lambda: grid.run_grid_method('setColumnsVisible', ['parent'], True))

    # with right_drawer:
    #     ui.label("Accounts").classes("text-2xl")

    #     ui.button("Close", on_click=lambda: right_drawer.toggle())



