class Phone:
    def __init__ (self, Id:str, number:str):
        self.__Id = Id
        self.__number = number
    def is_valid(self, number):
        return all(char in "1234567890()." for char in number)
    def get_id(self):
        return self.__Id
    def get_number(self):
        return self.__number
    def __str__(self):
        return f"{self.get_id()}:{self.get_number()}"
    
class Contact:
    def __init__(self, name:str = ""):
        self.__name = name
        self.__phones : list[Phone] = []
        self.__favorited = False
    def add_phone(self, Id:str, number:str):
        phone = Phone(Id, number)
        if not phone.is_valid(number):
            raise Exception("fail: invalid number")
        
        self.__phones.append(phone)

    def rm_phone(self, index:int):

        try:
            self.__phones.remove(self.__phones[index])

        except:
            raise Exception("fail: invalid number")
    def is_favorited(self):
        return self.__favorited
    def toogle_favorited(self):
        self.__favorited = not self.__favorited
    def get_phones(self):
        return list(self.__phones)
    
    def get_name(self):
        return self.__name
    
    def set_name(self, name:str):
        self.__name = name
    def __str__(self):

        phones_list = ", ".join(str(phone) for phone in self.__phones)
        return f"{"@" if self.is_favorited() else "-"} {self.get_name()} [{phones_list}]"



def main():
    while True:
        line = input()
        print("$"+line)
        args:list[str] = line.split(" ")
        cmd = args[0]
        try:
            match cmd:
                case "end":
                    break
                case "init":
                        contact = Contact(args[1])
                case "show":
                    try:
                        print(contact)
                    except:
                        raise Exception("fail: crie um contato antes")
                case "add":
                    contact.add_phone(args[1], args[2])
                case "rm":
                    contact.rm_phone(int(args[1]))
                case "tfav":
                    contact.toogle_favorited()
                case _:
                    print("fail: comando invalido")
        except Exception as e:
            print(e)
           

main()
