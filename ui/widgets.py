class TitleLabel(QLabel):
    def __init__(self, t): 
        super().__init__(t)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("font-size: 18px; font-weight: bold; padding: 6px;")


class StatusLabel(QLabel):
    def show_message(self, t, error=False):
        self.setStyleSheet("color: %s;" % ("#c0392b" if error else "#27ae60"))
        self.setText(t)
    def mousePressEvent(self, e):
        self.clear()
        super().mousePressEvent(e)


class NameLineEdit(QLineEdit):
    def focusInEvent(self, e):
        self.setStyleSheet("border: 2px solid #2980b9;")
        super().focusInEvent(e)
    def focusOutEvent(self, e):
        self.setStyleSheet("")
        super().focusOutEvent(e)


class SearchEdit(NameLineEdit):
    def __init__(self):
        super().__init__()
        self.setPlaceholderText("Название или автор…")
        self.setClearButtonEnabled(True)
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape: self.clear()
        super().keyPressEvent(e)


class PrimaryButton(QPushButton):
    def enterEvent(self, e):
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("background-color: #3498db; color: white;")
        super().enterEvent(e)
    def leaveEvent(self, e):
        self.setStyleSheet("")
        super().leaveEvent(e)


class DangerButton(QPushButton):
    def enterEvent(self, e):
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("background-color: #e74c3c; color: white;")
        super().enterEvent(e)
    def leaveEvent(self, e):
        self.setStyleSheet("")
        super().leaveEvent(e)


class YearSpinBox(QSpinBox):
    def __init__(self):
        super().__init__()
        self.setRange(1, datetime.now().year)
        self.setValue(2000)
    def wheelEvent(self, e):
        if self.hasFocus(): super().wheelEvent(e)
        else: e.ignore()


class PagesSpinBox(QSpinBox):
    def __init__(self):
        super().__init__()
        self.setRange(1, 5000)
        self.setValue(200)
        self.setSuffix(" стр.")


class GenreComboBox(QComboBox):
    def __init__(self, items):
        super().__init__()
        self.addItems(list(items))
    def wheelEvent(self, e):
        if self.hasFocus(): super().wheelEvent(e)
        else: e.ignore()


class BookTable(QTableWidget):
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

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Delete: self.delete_requested.emit()
        super().keyPressEvent(e)

    def fill(self, books):
        self.setRowCount(len(books))
        for row, b in enumerate(books):
            for col, val in enumerate((b.title, b.author, b.year, b.pages, b.genre)):
                item = QTableWidgetItem(str(val))
                if col in (2, 3): item.setTextAlignment(Qt.AlignCenter)
                self.setItem(row, col, item)
