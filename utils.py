from bs4 import BeautifulSoup
from typing import List, Literal, Tuple


mode = Literal["insert", 'append', 'prepend', 'delete',
               'replace', 'wrap', 'unwrap', 'attr']


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

    if content is not None:
        print("content is not None")
        if '<' in content and '>' in content:
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

    print("current elem=", current_elem, end="\n\n")
    print("mode=", mode_fn, end="\n\n")
    print("indexes=", indexes, end="\n\n")

    match mode_fn:
        case "append":
            current_elem.insert(len(list(current_elem.children)), content)
            with open(file_path, "w") as f:
                f.write(str(soup))
            return (True, "Element qo'shildi")
        case "prepend":
            current_elem.insert(0, content)
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
        case "wrap":
            if '<' in content and '>' in content:
                wrapper = BeautifulSoup(content, 'html.parser').contents[0]
                current_elem.wrap(wrapper)
                with open(file_path, "w") as f:
                    f.write(str(soup))
                return (True, "Element o'raldi")
            else:
                return (False, "Wrapper element topilmadi")
        case "unwrap":
            current_elem.unwrap()
            with open(file_path, "w") as f:
                f.write(str(soup))
            return (True, "Element o'chirildi")
        case "replace":
            current_elem.replace_with(content)
            with open(file_path, "w") as f:
                f.write(str(soup))
            return (True, "Element yangilandi")
        case "attr":
            if '<' in content and '>' in content:
                attrs = BeautifulSoup(content, 'html.parser').attrs
                for key, value in attrs.items():
                    current_elem[key] = value
                with open(file_path, "w") as f:
                    f.write(str(soup))
                return (True, "Element atributlari yangilandi")
            else:
                return (False, "Atributlar topilmadi")
        case _:
            return (False, "Mode topilmadi")


# status, message = update_html_element(
#     "append", "templates/components/temple.html", '<div class="container"></div>', [0])
