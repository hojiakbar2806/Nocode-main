from bs4 import BeautifulSoup
from typing import List, Literal, Tuple


mode = Literal["insert", 'append', 'delete', 'replace']


def update_html_element(mode_fn: mode, file_path: str, content: str, indexes: List[int] = None) -> Tuple[bool, str]:

    with open(file_path, "r") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    current_elem = soup.find(id="root")

    if not current_elem:
        temple_dir = f"templates/components/temple.html"
        with open(file_path, "w") as f:
            with open(temple_dir, "r") as t:
                f.write(t.read())
        return (False, "#root element topilmadi")

    tag = False
    if content is not None:
        print("content is not None")
        if '<' in content and '>' in content:
            tag = True
            content = BeautifulSoup(content, 'html.parser')
            print("content=", content, end="\n\n")

    if indexes is not None:
        for index in indexes:
            elements = []
            for elem in current_elem.children:
                if elem.name is not None:
                    elements.append(elem)
            if index >= len(elements):
                return (False, "Element topilmadi")
            current_elem = elements[index]

    match mode_fn:
        case "append":
            if tag:
                current_elem.insert(len(list(current_elem.children)), content)
            else:
                current_elem.string = current_elem.string+content
            with open(file_path, "w") as f:
                f.write(str(soup))
            return (True, "Element qo'shildi")
        case "insert":
            if tag:
                current_elem.insert(0, content)
            else:
                current_elem.string = content+current_elem.string
            with open(file_path, "w") as f:
                f.write(str(soup))
            return (True, "Element qo'shildi")
        case "delete":
            if current_elem == soup.find(id="root"):
                return (False, "Root element o'chirib bo'lmaydi")
            current_elem.decompose()
            with open(file_path, "w") as f:
                f.write(str(soup))
            return (True, "Element o'chirildi")

        case "replace":
            if tag:
                current_elem.replace_with(content)
            else:
                current_elem.string = content
            with open(file_path, "w") as f:
                f.write(str(soup))
            return (True, "Element yangilandi")
        case _:
            return (False, "Mode topilmadi")


# status, message = update_html_element(
#     "append", "templates/components/temple.html", '<div class="container"></div>', [0])
