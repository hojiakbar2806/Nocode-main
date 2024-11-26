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












        #
        # for index in element_indexes:
        #     elements = [
        #         elem for elem in current.children if elem.name is not None]
        #     if index >= len(elements):
        #         print(f"Xatolik: {index}-element topilmadi")
        #         return
        #     current = elements[index]
        #
        # if mode == 'delete':
        #     current.decompose()
        #     print("Element o'chirildi")
        #
        # elif mode == 'insert':
        #     current.clear()
        #     new_element = prepare_new_element(new_content)
        #     current.insert(0, new_element)
        #     print("Element yangilandi")
        #
        # elif mode == 'append':
        #     new_element = prepare_new_element(new_content)
        #     current.insert(len(list(current.children)), new_element)
        #     print("Element oxiriga qo'shildi")
        #
        # elif mode == 'prepend':
        #     new_element = prepare_new_element(new_content)
        #     current.insert(0, new_element)
        #     print("Element boshiga qo'shildi")
        #
        # elif mode == 'replace':
        #     new_element = prepare_new_element(new_content)
        #     current.replace_with(new_element)
        #     print("Element almashtirildi")
        #
        # elif mode == 'wrap':
        #     if '<' in new_content and '>' in new_content:
        #         wrapper = BeautifulSoup(new_content, 'html.parser').contents[0]
        #         current.wrap(wrapper)
        #         print("Element o'raldi")
        #     else:
        #         print("Xatolik: wrapper HTML element bo'lishi kerak")
        #
        # elif mode == 'unwrap':
        #     current.unwrap()
        #     print("Element ochildi")
        #
        # elif mode == 'attr':
        #     try:
        #         attr_name, attr_value = new_content.split('=')
        #         current[attr_name.strip()] = attr_value.strip()
        #         print("Attribut o'zgartirildi")
        #     except:
        #         print("Xatolik: format 'attr_name=attr_value' bo'lishi kerak")
        #
        # elif mode == 'clear':
        #     current.clear()
        #     print("Element tozalandi")
        #
        # else:
        #     print("Xatolik: noto'g'ri mode")
        #     return