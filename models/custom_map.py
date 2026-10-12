@total_ordering
class CustomMap(Entity):
    def __init__(self):
        self._keys, self._values = [], []

    @property
    def keys(self): return tuple(self._keys)
    @property
    def values(self): return tuple(self._values)

    def put(self, k, v):
        if k in self._keys: self._values[self._keys.index(k)] = v
        else: self._keys.append(k); self._values.append(v)
    def get(self, k, d=None): return self._values[self._keys.index(k)] if k in self._keys else d
    def items(self): return list(zip(self._keys, self._values))
    def describe(self) -> str: return "\n".join(f"{k}: {v}" for k, v in self.items())

    def __getitem__(self, k): return self.get(k) if k in self._keys else (_ for _ in ()).throw(KeyError(k))
    def __setitem__(self, k, v): self.put(k, v)
    def __contains__(self, k): return k in self._keys
    def __len__(self): return len(self._keys)
    def __iter__(self): return iter(self._keys)
    def __eq__(self, o): return isinstance(o, CustomMap) and self.items() == o.items()
    def __lt__(self, o): return isinstance(o, CustomMap) and len(self) < len(o)
    __hash__ = None
    def __repr__(self): return f"CustomMap({self.items()!r})"
    def __str__(self): return self.describe()
