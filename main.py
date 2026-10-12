"""Зачётный проект: «Каталог книг» (PySide6).

Соответствие требованиям:
  * все сущности - классы, наследуют абстрактный класс Entity;
  * переопределено 12 компонентов окна (TitleLabel, NameLineEdit, SearchEdit,
    PrimaryButton, DangerButton, YearSpinBox, PagesSpinBox, GenreComboBox,
    BookTable, StatusLabel, LoginDialog, MainWindow);
  * специальные методы: __eq__, __repr__, __str__, __lt__, __hash__, __len__ ...;
  * классы сравнимы (total_ordering), атрибуты через property (геттеры/сеттеры);
  * dict не используется - вместо него класс CustomMap;
  * 12 пользовательских объектов Book в списке;
  * при закрытии приложения сохраняется report.txt.
"""
import sys
from abc import ABC, abstractmethod
from datetime import datetime
from functools import total_ordering

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QApplication, QComboBox, QDialog, QGridLayout, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QMainWindow, QMessageBox, QPushButton,
    QSpinBox, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget,
    QAbstractItemView,
)

TIME_FORMAT = "%d.%m.%Y %H:%M:%S"
REPORT_FILE = "report.txt"
GENRES = ("Роман", "Фантастика", "Детектив", "Наука", "Поэзия")


# ======================================================================
#  Абстрактный класс и доменные сущности
# ======================================================================
class Entity(ABC):
    """Абстрактный родитель всех сущностей приложения."""

    @abstractmethod
    def describe(self) -> str:
        """Человекочитаемое описание сущности."""

    @abstractmethod
    def __eq__(self, other) -> bool:
        ...

    @abstractmethod
    def __lt__(self, other) -> bool:
        ...


@total_ordering
class Book(Entity):
    def __init__(self, title, author, year, pages, genre):
        self.title = title
        self.author = author
        self.year = year
        self.pages = pages
        self.genre = genre

    # --- геттеры / сеттеры ---
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        value = str(value).strip()
        if not value:
            raise ValueError("Название не может быть пустым")
        self._title = value

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        value = str(value).strip()
        if not value:
            raise ValueError("Автор не может быть пустым")
        self._author = value

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value):
        if not 0 < int(value) <= datetime.now().year:
            raise ValueError("Некорректный год издания")
        self._year = int(value)

    @property
    def pages(self):
        return self._pages

    @pages.setter
    def pages(self, value):
        if int(value) <= 0:
            raise ValueError("Число страниц должно быть положительным")
        self._pages = int(value)

    @property
    def genre(self):
        return self._genre

    @genre.setter
    def genre(self, value):
        self._genre = str(value)

    # --- методы объекта ---
    def describe(self) -> str:
        return f"«{self.title}», {self.author}, {self.year} г., {self.pages} стр. [{self.genre}]"

    # --- специальные методы ---
    def __eq__(self, other):
        if not isinstance(other, Book):
            return NotImplemented
        return (self._title.lower(), self._author.lower(), self._year) == \
               (other._title.lower(), other._author.lower(), other._year)

    def __lt__(self, other):
        if not isinstance(other, Book):
            return NotImplemented
        return (self._year, self._title.lower()) < (other._year, other._title.lower())

    def __hash__(self):
        return hash((self._title.lower(), self._author.lower(), self._year))

    def __repr__(self):
        return (f"Book(title={self._title!r}, author={self._author!r}, "
                f"year={self._year}, pages={self._pages}, genre={self._genre!r})")

    def __str__(self):
        return self.describe()

    def __len__(self):
        return self._pages


@total_ordering
class CustomMap(Entity):
    """Собственная реализация отображения (ключ -> значение) без dict."""

    def __init__(self):
        self._keys = []
        self._values = []

    # --- геттеры ---
    @property
    def keys(self):
        return tuple(self._keys)

    @property
    def values(self):
        return tuple(self._values)

    # --- работа с отображением ---
    def put(self, key, value):
        if key in self._keys:
            self._values[self._keys.index(key)] = value
        else:
            self._keys.append(key)
            self._values.append(value)

    def get(self, key, default=None):
        if key in self._keys:
            return self._values[self._keys.index(key)]
        return default

    def items(self):
        return list(zip(self._keys, self._values))

    def describe(self) -> str:
        return "\n".join(f"{k}: {v}" for k, v in self.items())

    # --- специальные методы ---
    def __getitem__(self, key):
        if key not in self._keys:
            raise KeyError(key)
        return self.get(key)

    def __setitem__(self, key, value):
        self.put(key, value)

    def __contains__(self, key):
        return key in self._keys

    def __len__(self):
        return len(self._keys)

    def __iter__(self):
        return iter(self._keys)

    def __eq__(self, other):
        if not isinstance(other, CustomMap):
            return NotImplemented
        return self.items() == other.items()

    def __lt__(self, other):
        if not isinstance(other, CustomMap):
            return NotImplemented
        return len(self) < len(other)

    __hash__ = None  # изменяемый объект

    def __repr__(self):
        return f"CustomMap({self.items()!r})"

    def __str__(self):
        return self.describe()


@total_ordering
class Session(Entity):
    """Сеанс работы пользователя (для отчёта)."""

    def __init__(self, login):
        self.login = login
        self._time_in = datetime.now()
        self._time_out = None

    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, value):
        value = str(value).strip()
        if not value:
            raise ValueError("Логин не может быть пустым")
        self._login = value

    @property
    def time_in(self):
        return self._time_in

    @property
    def time_out(self):
        return self._time_out

    @time_out.setter
    def time_out(self, value):
        self._time_out = value

    def close(self):
        self._time_out = datetime.now()

    def as_row(self):
        out = self._time_out.strftime(TIME_FORMAT) if self._time_out else "-"
        return (self._login, self._time_in.strftime(TIME_FORMAT), out)

    def describe(self) -> str:
        return " | ".join(self.as_row())

    def __eq__(self, other):
        if not isinstance(other, Session):
            return NotImplemented
        return (self._login, self._time_in) == (other._login, other._time_in)

    def __lt__(self, other):
        if not isinstance(other, Session):
            return NotImplemented
        return self._time_in < other._time_in

    def __hash__(self):
        return hash((self._login, self._time_in))

    def __repr__(self):
        return f"Session(login={self._login!r}, time_in={self._time_in!r}, time_out={self._time_out!r})"

    def __str__(self):
        return self.describe()


@total_ordering
class Library(Entity):
    """Коллекция книг и операции над ней."""

    def __init__(self, name, books=None):
        self.name = name
        self._books = list(books) if books else []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = str(value).strip() or "Библиотека"

    @property
    def books(self):
        return tuple(sorted(self._books))

    def add(self, book):
        if book in self._books:
            return False
        self._books.append(book)
        return True

    def remove(self, book):
        if book in self._books:
            self._books.remove(book)
            return True
        return False

    @staticmethod
    def matches(book, text, genre):
        text = text.strip().lower()
        in_text = text in book.title.lower() or text in book.author.lower()
        in_genre = genre == "Все" or book.genre == genre
        return in_text and in_genre

    def search(self, text="", genre="Все"):
        return [b for b in self.books if Library.matches(b, text, genre)]

    def stats_by_genre(self):
        stats = CustomMap()
        for book in self._books:
            stats.put(book.genre, stats.get(book.genre, 0) + 1)
        return stats

    def describe(self) -> str:
        return f"{self._name}: {len(self)} книг"

    def __len__(self):
        return len(self._books)

    def __eq__(self, other):
        if not isinstance(other, Library):
            return NotImplemented
        return self._name == other._name and sorted(self._books) == sorted(other._books)

    def __lt__(self, other):
        if not isinstance(other, Library):
            return NotImplemented
        return len(self) < len(other)

    def __hash__(self):
        return hash(self._name)

    def __repr__(self):
        return f"Library(name={self._name!r}, books={len(self)})"

    def __str__(self):
        return self.describe()

    @staticmethod
    def demo():
        data = (
            ("Война и мир", "Лев Толстой", 1869, 1225, "Роман"),
            ("Преступление и наказание", "Фёдор Достоевский", 1866, 672, "Роман"),
            ("Мастер и Маргарита", "Михаил Булгаков", 1967, 480, "Роман"),
            ("Солярис", "Станислав Лем", 1961, 320, "Фантастика"),
            ("Дюна", "Фрэнк Герберт", 1965, 704, "Фантастика"),
            ("Основание", "Айзек Азимов", 1951, 255, "Фантастика"),
            ("Убийство в «Восточном экспрессе»", "Агата Кристи", 1934, 256, "Детектив"),
            ("Собака Баскервилей", "Артур Конан Дойл", 1902, 256, "Детектив"),
            ("Краткая история времени", "Стивен Хокинг", 1988, 256, "Наука"),
            ("Cosmos", "Карл Саган", 1980, 396, "Наука"),
            ("Евгений Онегин", "Александр Пушкин", 1833, 224, "Поэзия"),
            ("Стихотворения", "Анна Ахматова", 1940, 300, "Поэзия"),
        )
        return Library("Каталог книг", [Book(*row) for row in data])


class ReportWriter:
    """Формирует и сохраняет отчёт о работе приложения."""

    @staticmethod
    def render(sessions):
        headers = ("login", "time_in", "time_out")
        rows = [s.as_row() for s in sessions]
        widths = [max(len(headers[i]), *(len(r[i]) for r in rows)) for i in range(3)]

        def line(cells):
            return "| " + " | ".join(c.ljust(w) for c, w in zip(cells, widths)) + " |"

        head = line(headers)
        border = "+" + "-" * (len(head) - 2) + "+"
        sep = "|" + "|".join("-" * (w + 2) for w in widths) + "|"
        return "\n".join([border, head, sep] + [line(r) for r in rows] + [border]) + "\n"

    @staticmethod
    def save(sessions, path=REPORT_FILE):
        with open(path, "w", encoding="utf-8") as f:
            f.write(ReportWriter.render(sessions))


# ======================================================================
#  Переопределённые компоненты окна
# ======================================================================
class TitleLabel(QLabel):  # 1
    def __init__(self, text):
        super().__init__(text)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("font-size: 18px; font-weight: bold; padding: 6px;")


class StatusLabel(QLabel):  # 2
    def show_message(self, text, error=False):
        self.setStyleSheet("color: %s;" % ("#c0392b" if error else "#27ae60"))
        self.setText(text)

    def mousePressEvent(self, event):  # клик по статусу очищает его
        self.clear()
        super().mousePressEvent(event)


class NameLineEdit(QLineEdit):  # 3
    def focusInEvent(self, event):
        self.setStyleSheet("border: 2px solid #2980b9;")
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        self.setStyleSheet("")
        super().focusOutEvent(event)


class SearchEdit(NameLineEdit):  # 4
    def __init__(self):
        super().__init__()
        self.setPlaceholderText("Название или автор…")
        self.setClearButtonEnabled(True)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.clear()
        super().keyPressEvent(event)


class PrimaryButton(QPushButton):  # 5
    def enterEvent(self, event):
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("background-color: #3498db; color: white;")
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet("")
        super().leaveEvent(event)


class DangerButton(QPushButton):  # 6
    def enterEvent(self, event):
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("background-color: #e74c3c; color: white;")
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet("")
        super().leaveEvent(event)


class YearSpinBox(QSpinBox):  # 7
    def __init__(self):
        super().__init__()
        self.setRange(1, datetime.now().year)
        self.setValue(2000)

    def wheelEvent(self, event):
        if self.hasFocus():
            super().wheelEvent(event)
        else:
            event.ignore()


class PagesSpinBox(QSpinBox):  # 8
    def __init__(self):
        super().__init__()
        self.setRange(1, 5000)
        self.setValue(200)
        self.setSuffix(" стр.")

    def textFromValue(self, value):
        return str(value)


class GenreComboBox(QComboBox):  # 9
    def __init__(self, items):
        super().__init__()
        self.addItems(list(items))

    def wheelEvent(self, event):
        if self.hasFocus():
            super().wheelEvent(event)
        else:
            event.ignore()


class BookTable(QTableWidget):  # 10
    delete_requested = Signal()
    HEADERS = ("Название", "Автор", "Год", "Страниц", "Жанр")

    def __init__(self):
        super().__init__(0, len(self.HEADERS))
        self.setHorizontalHeaderLabels(list(self.HEADERS))
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setAlternatingRowColors(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setVisible(False)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.delete_requested.emit()
        super().keyPressEvent(event)

    def fill(self, books):
        self.setRowCount(len(books))
        for row, b in enumerate(books):
            values = (b.title, b.author, b.year, b.pages, b.genre)
            for col, val in enumerate(values):
                item = QTableWidgetItem(str(val))
                if col in (2, 3):
                    item.setTextAlignment(Qt.AlignCenter)
                self.setItem(row, col, item)


class LoginDialog(QDialog):  # 11
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Вход")
        self.setFixedSize(320, 150)
        self._login = ""

        layout = QVBoxLayout(self)
        layout.addWidget(TitleLabel("Введите логин"))
        self.edit = NameLineEdit()
        self.edit.setPlaceholderText("UserName")
        self.edit.returnPressed.connect(self.accept)
        layout.addWidget(self.edit)
        self.error = StatusLabel("")
        self.error.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.error)
        btn = PrimaryButton("Войти")
        btn.clicked.connect(self.accept)
        layout.addWidget(btn)

    @property
    def login(self):
        return self._login

    def accept(self):  # переопределён
        text = self.edit.text().strip()
        if not text:
            self.error.show_message("Логин не может быть пустым", error=True)
            return
        self._login = text
        super().accept()


class MainWindow(QMainWindow):  # 12
    def __init__(self, session, library):
        super().__init__()
        self._session = session
        self._library = library
        self._visible = []
        self.setWindowTitle(library.name)
        self.resize(900, 640)

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)

        root.addWidget(TitleLabel(f"{library.name} · пользователь: {session.login}"))

        # --- поиск и фильтр ---
        filters = QHBoxLayout()
        filters.addWidget(QLabel("Поиск:"))
        self.search = SearchEdit()
        filters.addWidget(self.search, 1)
        filters.addWidget(QLabel("Жанр:"))
        self.filter = GenreComboBox(("Все",) + GENRES)
        filters.addWidget(self.filter)
        root.addLayout(filters)

        # --- таблица ---
        self.table = BookTable()
        root.addWidget(self.table, 1)

        # --- форма добавления ---
        box = QGroupBox("Новая книга")
        grid = QGridLayout(box)
        self.in_title = NameLineEdit()
        self.in_author = NameLineEdit()
        self.in_year = YearSpinBox()
        self.in_pages = PagesSpinBox()
        self.in_genre = GenreComboBox(GENRES)
        grid.addWidget(QLabel("Название:"), 0, 0)
        grid.addWidget(self.in_title, 0, 1)
        grid.addWidget(QLabel("Автор:"), 0, 2)
        grid.addWidget(self.in_author, 0, 3)
        grid.addWidget(QLabel("Год:"), 1, 0)
        grid.addWidget(self.in_year, 1, 1)
        grid.addWidget(QLabel("Страниц:"), 1, 2)
        grid.addWidget(self.in_pages, 1, 3)
        grid.addWidget(QLabel("Жанр:"), 2, 0)
        grid.addWidget(self.in_genre, 2, 1)
        for col in range(4):
            grid.setColumnStretch(col, 1 if col % 2 else 0)
        root.addWidget(box)

        # --- кнопки ---
        buttons = QHBoxLayout()
        self.btn_add = PrimaryButton("Добавить")
        self.btn_del = DangerButton("Удалить выбранную")
        self.btn_stats = PrimaryButton("Статистика по жанрам")
        for b in (self.btn_add, self.btn_del, self.btn_stats):
            buttons.addWidget(b, 1)
        root.addLayout(buttons)

        self.status = StatusLabel("")
        self.status.setAlignment(Qt.AlignCenter)
        root.addWidget(self.status)

        # --- сигналы ---
        self.search.textChanged.connect(self.refresh)
        self.filter.currentTextChanged.connect(self.refresh)
        self.btn_add.clicked.connect(self.on_add)
        self.btn_del.clicked.connect(self.on_delete)
        self.btn_stats.clicked.connect(self.on_stats)
        self.table.delete_requested.connect(self.on_delete)

        self.refresh()

    # --- методы объекта ---
    def refresh(self):
        self._visible = self._library.search(self.search.text(), self.filter.currentText())
        self.table.fill(self._visible)

    def on_add(self):
        try:
            book = Book(self.in_title.text(), self.in_author.text(), self.in_year.value(),
                        self.in_pages.value(), self.in_genre.currentText())
        except ValueError as err:
            self.status.show_message(str(err), error=True)
            return
        if self._library.add(book):
            self.status.show_message(f"Добавлено: {book.title}")
            self.in_title.clear()
            self.in_author.clear()
            self.refresh()
        else:
            self.status.show_message("Такая книга уже есть в каталоге", error=True)

    def on_delete(self):
        row = self.table.currentRow()
        if row < 0 or row >= len(self._visible):
            self.status.show_message("Выберите книгу в таблице", error=True)
            return
        book = self._visible[row]
        self._library.remove(book)
        self.status.show_message(f"Удалено: {book.title}")
        self.refresh()

    def on_stats(self):
        stats = self._library.stats_by_genre()
        QMessageBox.information(self, "Статистика", stats.describe() or "Каталог пуст")

    def closeEvent(self, event):  # переопределено: сохраняем отчёт
        self._session.close()
        ReportWriter.save([self._session])
        event.accept()


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
