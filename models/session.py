@total_ordering
class Session(Entity):
    def __init__(self, login):
        self.login = login
        self._time_in = datetime.now()
        self._time_out = None

    @property
    def login(self):
        return self._login
    @login.setter
    def login(self, v):
        if not (v := str(v).strip()): raise ValueError("Логин не может быть пустым")
        self._login = v

    @property
    def time_in(self): return self._time_in
    @property
    def time_out(self): return self._time_out
    @time_out.setter
    def time_out(self, v): self._time_out = v

    def close(self): self._time_out = datetime.now()
    def as_row(self): return (self._login, self._time_in.strftime(TIME_FORMAT), 
                             self._time_out.strftime(TIME_FORMAT) if self._time_out else "-")
    def describe(self) -> str: return " | ".join(self.as_row())

    def __eq__(self, o): return isinstance(o, Session) and (self._login, self._time_in) == (o._login, o._time_in)
    def __lt__(self, o): return isinstance(o, Session) and self._time_in < o._time_in
    def __hash__(self): return hash((self._login, self._time_in))
    def __repr__(self): return f"Session({self._login!r}, {self._time_in!r}, {self._time_out!r})"
    def __str__(self): return self.describe()
