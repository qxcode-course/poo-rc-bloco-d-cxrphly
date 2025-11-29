class Phone:
    def __init__(self, Id: str, number: str):
        self.__Id = Id
        self.__number = number

    def is_valid(self, number):
        return all(char in "0123456789()." for char in number)

    def get_id(self):
        return self.__Id

    def get_number(self):
        return self.__number

    def __str__(self):
        return f"{self.get_id()}:{self.get_number()}"


class Contact:
    def __init__(self, name: str):
        self.__name = name
        self.__phones: list[Phone] = []
        self.__favorited = False

    def add_phone(self, Id: str, number: str):
        phone = Phone(Id, number)
        if not phone.is_valid(number):
            raise Exception("fail: invalid number")
        self.__phones.append(phone)

    def rm_phone(self, index: int):
        if 0 <= index < len(self.__phones):
            self.__phones.pop(index)
        else:
            raise Exception("fail: invalid index")

    def is_favorited(self):
        return self.__favorited

    def toggle_favorited(self):
        self.__favorited = not self.__favorited

    def get_phones(self):
        return list(self.__phones)

    def get_name(self):
        return self.__name

    def __str__(self):
        phones_list = ", ".join(str(phone) for phone in self.__phones)
        return f"{'@' if self.is_favorited() else '-'} {self.get_name()} [{phones_list}]"


class Contacts:
    def __init__(self):
        self.__contacts: list[Contact] = []

    def __find_pos_by_name(self, name: str) -> int:
        for i, c in enumerate(self.__contacts):
            if c.get_name() == name:
                return i
        return -1

    def add_contact(self, name: str, phones: list[Phone]):
        pos = self.__find_pos_by_name(name)
        if pos != -1:  # já existe
            for ph in phones:
                self.__contacts[pos].add_phone(ph.get_id(), ph.get_number())
        else:
            c = Contact(name)
            for ph in phones:
                c.add_phone(ph.get_id(), ph.get_number())
            self.__contacts.append(c)
            self.__contacts.sort(key=lambda x: x.get_name().lower())

    def get_contact(self, name: str) -> Contact:
        pos = self.__find_pos_by_name(name)
        if pos == -1:
            raise Exception("fail: nao encontrado")
        return self.__contacts[pos]

    def rm_contact(self, name: str):
        pos = self.__find_pos_by_name(name)
        if pos == -1:
            raise Exception("fail: nao encontrado")
        self.__contacts.pop(pos)

    def search(self, pattern: str):
        low = pattern.lower()
        res = []
        for contact in self.__contacts:
            if low in contact.get_name().lower():
                res.append(contact)
                continue
            for phone in contact.get_phones():
                if low in phone.get_id().lower() or low in phone.get_number():
                    res.append(contact)
                    break
        return res

    def get_favorited(self):
        return [c for c in self.__contacts if c.is_favorited()]

    def __str__(self):
        return "\n".join(str(c) for c in self.__contacts) if self.__contacts else "fail: sem contatos"


def main():
    contacts = Contacts()

    while True:
        try:
            line = input()
            print("$" + line)
            args = line.split()
            cmd = args[0]

            if cmd == "end":
                break
            elif cmd == "add":
                name = args[1]
                phones = [Phone(*p.split(":")) for p in args[2:]]
                contacts.add_contact(name, phones)
            elif cmd == "show":
                print(contacts)
            elif cmd == "rmFone":
                name = args[1]
                index = int(args[2])
                contacts.get_contact(name).rm_phone(index)
            elif cmd == "rm":
                contacts.rm_contact(args[1])
            elif cmd == "search":
                res = contacts.search(args[1])
                print("\n".join(str(c) for c in res))
            elif cmd == "tfav":
                c = contacts.get_contact(args[1])
                c.toggle_favorited()
            elif cmd == "favs":
                print("\n".join(str(c) for c in contacts.get_favorited()))
            else:
                print("fail: comando invalido")

        except Exception as e:
            print(e)


main()
