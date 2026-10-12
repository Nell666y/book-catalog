@total_ordering
class Library(Entity):
    def __init__(self, name, books=None):
        self.name = name
        self._books = list(books) if books else []

    @property
    def name(self): return self._name
    @name.setter
    def name(self, v): self._name = str(v).strip() or "Библиотека"

    @property
    def books(self): return tuple(sorted(self._books))

    def add(self, b):
        if b in self._books: return False
        self._books.append(b); return True
    def remove(self, b):
        if b in self._books: self._books.remove(b); return True
        return False
    def search(self, txt="", genre="Все"):
        txt = txt.strip().lower()
        return [b for b in self.books if (txt in b.title.lower() or txt in b.author.lower()) and 
                (genre == "Все" or b.genre == genre)]
    def stats_by_genre(self):
        s = CustomMap()
        for b in self._books: s.put(b.genre, s.get(b.genre, 0) + 1)
        return s
    def describe(self) -> str: return f"{self._name}: {len(self)} книг"

    def __len__(self): return len(self._books)
    def __eq__(self, o): return isinstance(o, Library) and self._name == o._name and sorted(self._books) == sorted(o._books)
    def __lt__(self, o): return isinstance(o, Library) and len(self) < len(o)
    def __hash__(self): return hash(self._name)
    def __repr__(self): return f"Library({self._name!r}, {len(self)})"
    def __str__(self): return self.describe()

    @staticmethod
    def demo():
        data = [
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
        ]
        return Library("Каталог книг", [Book(*r) for r in data])
