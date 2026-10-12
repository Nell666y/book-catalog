class MainWindow(QMainWindow):
    def __init__(self, session, library):
        super().__init__()
        self._session = session
        self._library = library
        self._visible = []
        self.setWindowTitle(library.name)
        self.resize(900, 640)

        c = QWidget()
        self.setCentralWidget(c)
        r = QVBoxLayout(c)

        r.addWidget(TitleLabel(f"{library.name} · пользователь: {session.login}"))

        f = QHBoxLayout()
        f.addWidget(QLabel("Поиск:"))
        self.search = SearchEdit()
        f.addWidget(self.search, 1)
        f.addWidget(QLabel("Жанр:"))
        self.filter = GenreComboBox(("Все",) + GENRES)
        f.addWidget(self.filter)
        r.addLayout(f)

        self.table = BookTable()
        r.addWidget(self.table, 1)

        box = QGroupBox("Новая книга")
        g = QGridLayout(box)
        self.in_title = NameLineEdit()
        self.in_author = NameLineEdit()
        self.in_year = YearSpinBox()
        self.in_pages = PagesSpinBox()
        self.in_genre = GenreComboBox(GENRES)
        
        for i, (l, w) in enumerate([(("Название:", self.in_title), ("Автор:", self.in_author)),
                                      (("Год:", self.in_year), ("Страниц:", self.in_pages))]):
            for j, (lbl, wgt) in enumerate(l):
                g.addWidget(QLabel(lbl), i, j*2)
                g.addWidget(wgt, i, j*2+1)
        g.addWidget(QLabel("Жанр:"), 2, 0)
        g.addWidget(self.in_genre, 2, 1)
        r.addWidget(box)

        b = QHBoxLayout()
        self.btn_add = PrimaryButton("Добавить")
        self.btn_del = DangerButton("Удалить выбранную")
        self.btn_stats = PrimaryButton("Статистика по жанрам")
        for btn in (self.btn_add, self.btn_del, self.btn_stats):
            b.addWidget(btn, 1)
        r.addLayout(b)

        self.status = StatusLabel("")
        self.status.setAlignment(Qt.AlignCenter)
        r.addWidget(self.status)

        self.search.textChanged.connect(self.refresh)
        self.filter.currentTextChanged.connect(self.refresh)
        self.btn_add.clicked.connect(self.on_add)
        self.btn_del.clicked.connect(self.on_delete)
        self.btn_stats.clicked.connect(self.on_stats)
        self.table.delete_requested.connect(self.on_delete)

        self.refresh()

    def refresh(self):
        self._visible = self._library.search(self.search.text(), self.filter.currentText())
        self.table.fill(self._visible)

    def on_add(self):
        try:
            book = Book(self.in_title.text(), self.in_author.text(), self.in_year.value(),
                        self.in_pages.value(), self.in_genre.currentText())
        except ValueError as e:
            self.status.show_message(str(e), error=True)
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

    def closeEvent(self, e):
        self._session.close()
        ReportWriter.save([self._session])
        e.accept()


def main():
    app = QApplication(sys.argv)
    dialog = LoginDialog()
    if dialog.exec() != QDialog.Accepted: return 0
    session = Session(dialog.login)
    window = MainWindow(session, Library.demo())
    window.show()
    return app.exec()
if __name__ == "__main__":
    sys.exit(main())
