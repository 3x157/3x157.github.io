#!/usr/bin/env python
#
# a simple jinja2 template engine to generate html files
#
import datetime
from pprint import pprint

from jinja2 import Environment, FileSystemLoader


def page_info(page_name: str) -> dict[str, str]:
    info = {"title": "", "date": "", "anchor": ""}
    data = open(f"pages/{page_name}").read()
    for item in list(info.keys()):
        try:
            idx = data.index(f'<!-- {item}:"')
            x = data[idx + 5 :].split(':"', 1)[1]
            title = x.split('" -->')[0].strip()
            info[item] = title
        except Exception:
            pass
    return info


def generate():
    generate_date = str(datetime.datetime.now(datetime.UTC))
    pages = {
        # NOTE: order matters, but a TODO in the future would be to sort by dates
        "arc.html": {"content": "", "date": "", "anchor": "", "title": ""},
        # "care.html": {"content": "", "date": "", "anchor": "", "title": ""},
        "hello.html": {},
    }

    environment = Environment(loader=FileSystemLoader("pages/"))
    for page in list(pages.keys()):
        template = environment.get_template(page)
        info = page_info(page)
        print(page)
        pprint(info)
        content = template.render(**info)
        pages[page]["content"] = content
        pages[page]["date"] = info["date"]
        pages[page]["anchor"] = info["anchor"]
        pages[page]["title"] = info["title"]
    template = environment.get_template("index.html")
    final_content = template.render(pages=pages, current_datetime=generate_date)
    with open("index.html", "w") as fd:
        fd.write(final_content)


if __name__ == "__main__":
    generate()
