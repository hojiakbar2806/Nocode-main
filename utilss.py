from bs4 import BeautifulSoup


def update_html_element(element_indexes, new_content='', mode='insert', file_path='index.html'):
    """
    HTML elementlarni boshqarish uchun universal funksiya

    Args:
        element_indexes (list): Elementgacha bo'lgan yo'l (bo'sh bo'lsa root bilan ishlaydi)
        new_content (str): Yangi kontent
        mode (str): Quyidagi amallardan biri:
            - 'insert': elementni yangilash yoki root ga qo'shish
            - 'append': elementga yoki root ga qo'shish
            - 'prepend': element yoki root boshiga qo'shish
            - 'delete': elementni o'chirish
            - 'replace': elementni almashtirish
            - 'wrap': elementni o'rash
            - 'unwrap': elementni ochish
            - 'attr': attributni o'zgartirish
            - 'clear': ichidagi kontentni tozalash
        file_path (str): HTML fayl nomi
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file.read(), 'html.parser')

        root = soup.find(id='root')
        if not root:
            print("Xatolik: #root element topilmadi")
            return

        def prepare_new_element(content):
            if '<' in content and '>' in content:
                return BeautifulSoup(content, 'html.parser').contents[0]
            return content

        if not element_indexes:
            if mode in ['insert', 'append']:
                new_element = prepare_new_element(new_content)
                root.insert(len(list(root.children)), new_element)
                print(f"Element root oxiriga qo'shildi ({mode})")

            elif mode == 'prepend':
                new_element = prepare_new_element(new_content)
                root.insert(0, new_element)
                print("Element root boshiga qo'shildi")

            else:
                print(
                    "Xatolik: root uchun faqat insert, append va prepend operatsiyalari mavjud")
                return

            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(str(soup))
            return

        current = root
        for index in element_indexes:
            elements = [
                elem for elem in current.children if elem.name is not None]
            if index >= len(elements):
                print(f"Xatolik: {index}-element topilmadi")
                return
            current = elements[index]

        if mode == 'delete':
            current.decompose()
            print("Element o'chirildi")

        elif mode == 'insert':
            current.clear()
            new_element = prepare_new_element(new_content)
            current.insert(0, new_element)
            print("Element yangilandi")

        elif mode == 'append':
            new_element = prepare_new_element(new_content)
            current.insert(len(list(current.children)), new_element)
            print("Element oxiriga qo'shildi")

        elif mode == 'prepend':
            new_element = prepare_new_element(new_content)
            current.insert(0, new_element)
            print("Element boshiga qo'shildi")

        elif mode == 'replace':
            new_element = prepare_new_element(new_content)
            current.replace_with(new_element)
            print("Element almashtirildi")

        elif mode == 'wrap':
            if '<' in new_content and '>' in new_content:
                wrapper = BeautifulSoup(new_content, 'html.parser').contents[0]
                current.wrap(wrapper)
                print("Element o'raldi")
            else:
                print("Xatolik: wrapper HTML element bo'lishi kerak")

        elif mode == 'unwrap':
            current.unwrap()
            print("Element ochildi")

        elif mode == 'attr':
            try:
                attr_name, attr_value = new_content.split('=')
                current[attr_name.strip()] = attr_value.strip()
                print("Attribut o'zgartirildi")
            except:
                print("Xatolik: format 'attr_name=attr_value' bo'lishi kerak")

        elif mode == 'clear':
            current.clear()
            print("Element tozalandi")

        else:
            print("Xatolik: noto'g'ri mode")
            return

        # O'zgarishlarni saqlash
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(soup))

    except Exception as e:
        print(f"Xatolik yuz berdi: {str(e)}")


# Ishlatish namunalari:
"""
# Root bilan ishlash:
# 1. Root oxiriga element qo'shish
update_html_element([], "<div>Root oxiriga div</div>", mode='insert')
update_html_element([], "<div>Root oxiriga div</div>", mode='append')

# 2. Root boshiga element qo'shish
update_html_element([], "<div>Root boshiga div</div>", mode='prepend')

# Ma'lum element bilan ishlash:
# 3. Element ichini yangilash
update_html_element([0], "<div>Yangi div</div>", mode='insert')

# 4. Element oxiriga qo'shish
update_html_element([0], "<span>Oxirgi span</span>", mode='append')

# 5. Element boshiga qo'shish
update_html_element([0], "<span>Oldingi span</span>", mode='prepend')

# Boshqa operatsiyalar:
# 6. Elementni almashtirish
update_html_element([0], "<p>Yangi paragraf</p>", mode='replace')

# 7. Elementni o'rash
update_html_element([0], "<div class='wrapper'></div>", mode='wrap')

# 8. Elementdan o'ramni olish
update_html_element([0], mode='unwrap')

# 9. Attributni o'zgartirish
update_html_element([0], "class=new-class", mode='attr')

# 10. Elementni tozalash
update_html_element([0], mode='clear')

# 11. Elementni o'chirish
update_html_element([0], mode='delete')
"""
