@total_ordering
class Book(Entity):
    def __init__(self, title, author, year, pages, genre):
        self.title = title
        self.author = author
        self.year = year
        self.pages = pages
        self.genre = genre

    @property
    def title(self):
        return self._title
    @title.setter
    def title(self, v):
        if not (v := str(v).strip()): raise ValueError("Название не может быть пустым")
        self._title = v

    @property
    def author(self):
        return self._author
    @author.setter
    def author(self, v):
        if not (v := str(v).strip()): raise ValueError("Автор не может быть пустым")
        self._author = v

    @property
    def year(self):
        return self._year
    @year.setter
    def year(self, v):
        v = int(v)
        if not (0 < v <= datetime.now().year): raise ValueError("Некорректный год")
        self._year = v

    @property
    def pages(self):
        return self._pages
    @pages.setter
    def pages(self, v):
        v = int(v)
        if v <= 0: raise ValueError("Страниц должно быть > 0")
        self._pages = v

    @property
    def genre(self):
        return self._genre
    @genre.setter
    def genre(self, v):
        self._genre = str(v)

    def describe(self) -> str:
        return f"«{self._title}», {self._author}, {self._year} г., {self._pages} стр. [{self._genre}]"

    def __eq__(self, other):
        if not isinstance(other, Book): return NotImplemented
        return (self._title.lower(), self._author.lower(), self._year) == \
               (other._title.lower(), other._author.lower(), other._year)
    def __lt__(self, other):
        if not isinstance(other, Book): return NotImplemented
        return (self._year, self._title.lower()) < (other._year, other._title.lower())
    def __hash__(self): return hash((self._title.lower(), self._author.lower(), self._year))
    def __repr__(self): return f"Book({self._title!r}, {self._author!r}, {self._year}, {self._pages}, {self._genre!r})"
    def __str__(self): return self.describe()
    def __len__(self): return self._pages

