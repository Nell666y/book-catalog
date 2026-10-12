"""Зачётный проект: «Каталог книг» (PySide6). Точка входа."""
import sys

from PySide6.QtWidgets import QApplication, QDialog

from models.library import Library
from models.session import Session
from ui.login_dialog import LoginDialog
from ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    dialog = LoginDialog()
    if dialog.exec() != QDialog.Accepted:
        return 0
    session = Session(dialog.login)
    window = MainWindow(session, Library.demo())
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
