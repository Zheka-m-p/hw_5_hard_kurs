import json


dict_for_test_1 = {
    "token": "test_token",
    "action": "getbook",
    "data": {
        "id": 2
    }
}
dict_for_test_2 = {
    "token": "best_student!)",
    "action": "getbook",
    "data": {
        "id": 2
    }
}
dict_for_test_3 = {
    "token": "test_token",
    "action": "getbook",
    "data": {
        "id": 3
    }
}
dict_for_test_4 = {
    "token": "wrong_token",
    "action": "getbook",
    "data": {
        "id": 3
    }
}
dict_for_test = [dict_for_test_1, dict_for_test_2, dict_for_test_3, dict_for_test_4]


def user_verification(func):
    # Реализован чисто декоратор: если пользовтеля нет в базе, то заканчивает работу функции
    # Если есть в базе, то передаёт выполнение функции с пользователем, который точно есть в базе
    def inner(*args, **kwargs):
        with open('users.json', 'r') as f:
            users = json.load(f)
        for user_data in users:
            if user_data["token"] == args[0]["token"]:
                print(f'Приветстуем, {user_data["name"]} {user_data["surname"]}!')
                return func(*args, **kwargs)
        print('Извините,но вас нет в нашей базе. Мы не можем выдать вам книгу!')

    return inner


@user_verification
def get_book_from_library(dicionary):
    id_book = dicionary["data"]["id"]  # Ид книги, которую надо выдать, если: 1)она есть в базе, 2)не занята
    with open('library.json') as F:
        library = json.load(F)
    for book_data in library:
        if book_data["id"] == id_book:
            if book_data["availablity"]:
                print(f'Получите книгу "{book_data["title"]}" автора {book_data["author"]}')
                library[book_data["id"] - 1]["availablity"] = False
                with open('library.json', 'w') as change_library:
                    json.dump(library, change_library, indent=4)
                return
            else:
                print(f'К сожалению, книга {book_data["title"]} уже занята. Можем посоветовать что-то наподобие')
                return
    print('К сожалению, у нас в библиотеки нет такой книги. Можем посоветовать что-то наподобие')


for i in range(4):
    print()
    get_book_from_library(dict_for_test[i])
