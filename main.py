from view import View
from controller import Controller
from db import *


def main():
    database = r"./pythonsqlite.db"
    conn = create_connection(database)
    if conn is not None:
        create_table(conn)
        rows = get_all_rows(conn)
        view = View.View()
        controller = Controller.Controller(view, rows, conn)
        controller.run()


if __name__ == "__main__":
    main()
