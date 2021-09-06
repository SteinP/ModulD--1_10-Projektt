from os import name
import sys
import json
import requests
from requests.api import request

auth_params = {}
path = ".env"
with open(path, encoding="UTF-8") as file_object:
    auth_params_json = json.load(file_object)

# Данные авторизации в API Trello
auth_params = {
    "key": auth_params_json["Schlüssel"],
    "token": auth_params_json["Token"],
}

# Адрес, на котором расположен API Trello, # Именно туда мы будем отправлять HTTP запросы.
base_url = "https://api.trello.com/1/{}"

# id доски
board_id = auth_params_json["board_id"]


def read():
    # Получим данные всех колонок на доске:
    column_data_get = base_url.format('boards') + '/' + board_id + '/lists'
    column_data_requests = requests.get(column_data_get, params=auth_params)
    # https://api.trello.com/1/boards/...(board_id)/lists?key=...&token=...
    column_data = column_data_requests.json()

    # Теперь выведем название каждой колонки и всех заданий, которые к ней относятся:
    for column in column_data:
        # Получим данные всех задач в колонке и перечислим все названия
        task_data = requests.get(base_url.format(
            'lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        # Добавьте рядом с названием колонки цифру, отражающую количество задач в ней
        print(column['name'] + " - ({})".format(len(task_data)))
        if not task_data:
            print('\t' + 'Нет задач!')
            continue
        for task in task_data:
            print('\t' + task['name'] + '\t' + task['id'])


def create(name, column_name):
    # Получим данные всех колонок на доске
    column_data = requests.get(base_url.format(
        'boards') + '/' + board_id + '/lists', params=auth_params).json()

    # Переберём данные обо всех колонках, пока не найдём ту колонку, которая нам нужна
    for column in column_data:
        if column['name'] == column_name:
            # Создадим задачу с именем _name_ в найденной колонке
            requests.post(base_url.format('cards'), data={
                          'name': name, 'idList': column['id'], **auth_params})
            break


def create_cards(column_name: str) -> None:
    # Реализуйте создание колонок
    board_data = requests.get(base_url.format(
        'boards') + '/' + board_id, params=auth_params).json()
    print(board_data["id"])
    requests.post(base_url.format("list"), data={
                  "name": column_name, "idBoard": board_data["id"], **auth_params})


def printColizia(listTask: list) -> None:
    """
    Выводит в консоль список задачь с id номером и имя колонки, в которой эта задача находится
    """
    for task in listTask:
        # Получим колонку, которой принадлежит наша задача
        column = requests.get(base_url.format(
            'lists') + '/' + task['idList'], params=auth_params).json()

        print("Имя колонки: " + column['name'])
        print('\t' + "Имя задачи: " +
              task['name'] + ';\t' + "id задачи: " + task['id'])


def move(name, column_name):
    # Получим данные всех колонок на доске
    column_data = requests.get(base_url.format(
        'boards') + '/' + board_id + '/lists', params=auth_params).json()

    # Среди всех колонок нужно найти задачу по имени и получить её id
    listTask = []
    for column in column_data:
        column_tasks = requests.get(base_url.format(
            'lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        for task in column_tasks:
            if task['name'] == name:
                listTask.append(task)
    if len(listTask) == False:
        raise AssertionError(
            "Команда \"{name}\" не найдена.".format(name=name))

    task_id = listTask[0]
    loopYes = True
    if len(listTask) > 1:
        print("Возникла коллизия. На доске есть несколько задач с именем \"{name}\"".format(
            name=name))
        printColizia(listTask=listTask)
        inputId = input(
            "Введите id номер задачи, которую бы вы хотели переместить: ")

        while loopYes:
            for task in listTask:
                if inputId == task["id"]:
                    task_id = task
                    loopYes = False
                    break
            if loopYes == False:
                break
            print("Id номер \"{inputId}\" задачи \"{name}\", которую бы вы хотели переместить, введен неправильно".format(
                inputId=inputId, name=name))

            inputId = input(
                "Хотите повторить? Введите id номер задачи снова. В противном случае введите  \"N\" или \"n\": ")
            if inputId == "N" or inputId == "n":
                loopYes = False

    # Теперь у нас есть id задачи, которую мы хотим переместить

    if inputId != "N" and inputId != "n":
        for column in column_data:
            if column['name'] == column_name:
                # И выполним запрос к API для перемещения задачи в нужную колонку
                requests.put(base_url.format('cards') + '/' + task_id["id"] +
                             '/idList', data={'value': column['id'], **auth_params})
                break


def name_function(sysArgv: list) -> str:
    """
    Проверка количества введенных аргументов:
    если количество аргументов = 1, вернет "read",
    если количество аргументов = 2 или  > 4, возбуждает исключение AttributeError,
    во всех остальных случаях возращает первый аргумент
    """
    lenArgv = len(sysArgv)
    if lenArgv == 2 or lenArgv > 4:
        raise AttributeError(
            "Количество аргументов не соответствует ожидаемому.")

    if lenArgv == 1:
        return "read"

    return sysArgv[1]


def return_function(nameFunction: str, seq_function: dict):
    """
    Проверяет введенную команду со списком обробатываемых команд. Если совпадение обнаружено, то возвращает ссылку на функцию, в обратном случае возбуждает исключение AttributeError
    """
    for functionName in seq_function:
        if nameFunction == functionName:
            return seq_function[functionName]
    raise AttributeError(
        "Команда \"{func}\" не найдена.".format(func=nameFunction))


def coll_function(referenceFunction, sysArgv: list) -> None:

    lenArgv = len(sysArgv)

    if nameFunction == "read":
        referenceFunction()
        return None
    if lenArgv == 3:
        referenceFunction(sys.argv[2])
        return None
    referenceFunction(sys.argv[2], sys.argv[3])


if __name__ == "__main__":
    seq_function = {"read": read, "createlists": create,
                    "move": move, "createcards": create_cards}
    sysArgv = sys.argv

    try:
        nameFunction = name_function(sysArgv=sysArgv)
        referenceFunction = return_function(
            nameFunction=nameFunction, seq_function=seq_function)
        coll_function(referenceFunction=referenceFunction, sysArgv=sysArgv)
    except AttributeError as err:
        print(err)
    except AssertionError as err:
        print(err)


# python Trello.py
# python Trello.py createcards "Im Gange"
# python Trello.py createlists "Изучить Python" "Im Gange"
# python Trello.py move "Изучить Python" "Im Gange"
