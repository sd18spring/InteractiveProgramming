import requests
from bs4 import BeautifulSoup, NavigableString, Tag


urls = [
    "https://en.wikipedia.org/wiki/Modern_Greek",
    "https://en.wikipedia.org/wiki/Diglossia"
]

with requests.Session() as session:
    for url in urls:
        response = session.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        stack = []
        for child in soup.select_one("#mw-content-text > p").children:
            if isinstance(child, NavigableString):
                if "(" in child:
                    stack.append("(")
                if ")" in child:
                    stack.pop()

            if isinstance(child, Tag) and child.name == "a" and not stack:
                print(child.get_text())
                break
