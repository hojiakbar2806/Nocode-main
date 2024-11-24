from bs4 import BeautifulSoup
from typing import List, Literal, Tuple


mode = Literal["insert", 'append', 'delete', 'replace',
               'wrap', 'unwrap', 'attr', 'clear']


def update_html_element(mode: mode, file_path: str, content: str, indexes: List[int] = None) -> Tuple[bool, str]:

    with open(file_path, "r") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    current_elem = soup.find(id="root")

    if not current_elem:
        temple_dir = f"templates/components/temple.html"
        with open(file_path, "w") as f:
            with open(temple_dir, "r") as t:
                f.write(t.read())
        return (False, "#root element topilmadi")

    if '<' in content and '>' in content:
        content = BeautifulSoup(content, 'html.parser').contents[0]

    if indexes is not None:
        for index in indexes:
            elements = []
            for elem in current_elem.children:
                if elem.name is not None:
                    elements.append(elem)
            if index >= len(elements):
                return (False, "Element topilmadi")
            current_elem = elements[index]

    match mode:
        case "append":
            current_elem.append(content)
            with open(file_path, "w") as f:
                f.write(str(soup))
            return (True, "Element qo'shildi")
        case "delete":
            current_elem.decompose()
            with open(file_path, "w") as f:
                f.write(str(soup))
            return (True, "Element o'chirildi")
        case _:
            return (False, "Mode topilmadi")


# status, message = update_html_element("append", "index.html", "new", [0, 1])
