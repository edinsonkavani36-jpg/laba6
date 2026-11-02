from html.parser import HTMLParser
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[1]
pages = ["index.html", "about.html", "projects.html"]

class PageCheck(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = self.body = self.css = False
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "title": self.title = True
        if tag == "body": self.body = True
        if tag == "link" and attrs.get("rel") == "stylesheet" and attrs.get("href") == "style.css": self.css = True

errors = []
for name in pages:
    path = root / name
    if not path.exists():
        errors.append(f"Не найден {name}")
        continue
    check = PageCheck()
    check.feed(path.read_text(encoding="utf-8"))
    if not check.title: errors.append(f"В {name} отсутствует <title>")
    if not check.body: errors.append(f"В {name} отсутствует <body>")
    if not check.css: errors.append(f"В {name} не подключён style.css")
if not (root / "style.css").exists(): errors.append("Не найден style.css")
if errors:
    print("\n".join(errors))
    sys.exit(1)
print("Проверка пройдена: все страницы и таблица стилей на месте.")
