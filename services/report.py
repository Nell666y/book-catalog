class ReportWriter:
    @staticmethod
    def render(sessions):
        h = ("login", "time_in", "time_out")
        rows = [s.as_row() for s in sessions]
        w = [max(len(h[i]), *(len(r[i]) for r in rows)) for i in range(3)]
        line = lambda c: "| " + " | ".join(x.ljust(y) for x, y in zip(c, w)) + " |"
        head = line(h)
        border = "+" + "-" * (len(head) - 2) + "+"
        sep = "|" + "|".join("-" * (x + 2) for x in w) + "|"
        return "\n".join([border, head, sep] + [line(r) for r in rows] + [border]) + "\n"

    @staticmethod
    def save(sessions, path=REPORT_FILE):
        with open(path, "w", encoding="utf-8") as f: f.write(ReportWriter.render(sessions))
