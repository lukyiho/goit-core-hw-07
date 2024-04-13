from datetime import datetime, timedelta
from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Phone number must be 10 digits")
        self.__value = value

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def delete_phone(self, phone):
        self.phones = [p for p in self.phones if str(p) != phone]

    def edit_phone(self, old_phone, new_phone):
        self.delete_phone(old_phone)
        self.add_phone(new_phone)

    def add_birthday(self, birthday):
        if self.birthday is None:
            self.birthday = Birthday(birthday)
        else:
            raise ValueError("Only one birthday allowed per contact")

    def find_phone(self, phone):
        for p in self.phones:
            if str(p) == phone:
                return p
        return None

    def __str__(self):
        phones_str = '; '.join(str(p) for p in self.phones)
        birthday_str = str(self.birthday) if self.birthday else "No birthday"
        return f"Contact name: {self.name}, phones: {phones_str}, birthday: {birthday_str}"

class AddressBook(UserDict):
    def __init__(self):
        self.data = {}

    def add_record(self, record):
        self.data[record.name.value] = record

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def find(self, name):
        return self.data.get(name)

    def upcoming_birthdays(self):
        today = datetime.today()
        next_week = today + timedelta(days=7)
        upcoming_birthdays = []
        for record in self.data.values():
            if record.birthday and today <= record.birthday.value <= next_week:
                upcoming_birthdays.append(record)
        return upcoming_birthdays


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (IndexError, ValueError, KeyError) as e:
            return str(e)
    return inner

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_contact(args, book: AddressBook):
    name, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(record.phones[0], new_phone)  # Assuming there's only one phone number per contact
        return f"Phone number updated for {name}"
    else:
        return f"No contact found with name {name}"

@input_error
def show_phone(args, book: AddressBook):
    name, _ = args
    record = book.find(name)
    if record:
        return f"Phone number for {name}: {record.phones[0]}"  # Assuming there's only one phone number per contact
    else:
        return f"No contact found with name {name}"

@input_error
def show_all(book: AddressBook):
    if book.data:
        return "\n".join(str(record) for record in book.data.values())
    else:
        return "No contacts in the address book"


@input_error
def add_birthday(args, book: AddressBook):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return f"Birthday added for {name}"
    else:
        return f"No contact found with name {name}"

@input_error
def show_birthday(args, book: AddressBook):
    name, _ = args
    record = book.find(name)
    if record and record.birthday:
        return f"Birthday for {name}: {record.birthday}"
    elif record:
        return f"No birthday set for {name}"
    else:
        return f"No contact found with name {name}"

@input_error
def birthdays(args, book: AddressBook):
    upcoming = book.upcoming_birthdays()
    if upcoming:
        return "\n".join(str(record) for record in upcoming)
    else:
        return "No upcoming birthdays"

def parse_input(user_input):
    tokens = user_input.split()
    command = tokens[0]
    args = tokens[1:]
    return command, args

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
