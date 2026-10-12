class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Вход")
        self.setFixedSize(320, 150)
        self._login = ""
        
        l = QVBoxLayout(self)
        l.addWidget(TitleLabel("Введите логин"))
        self.edit = NameLineEdit()
        self.edit.setPlaceholderText("UserName")
        self.edit.returnPressed.connect(self.accept)
        l.addWidget(self.edit)
        self.error = StatusLabel("")
        self.error.setAlignment(Qt.AlignCenter)
        l.addWidget(self.error)
        b = PrimaryButton("Войти")
        b.clicked.connect(self.accept)
        l.addWidget(b)

    @property
    def login(self): return self._login

    def accept(self):
        t = self.edit.text().strip()
        if not t:
            self.error.show_message("Логин не может быть пустым", error=True)
            return
        self._login = t
        super().accept()
