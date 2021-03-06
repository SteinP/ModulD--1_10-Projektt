
# Задание
1. Добавьте рядом с названием колонки цифру, отражающую количество задач в ней.
1. Реализуйте создание колонок.
1. Обработайте совпадающие имена задач *

Как вы думаете, что случится, если у нас появится две задачи с одинаковым именем? Реализуйте обработку такой ситуации. Пользователь должен иметь возможность управлять всеми задачами вне зависимости от того, как он их называет.

Сейчас при работе с задачей мы перебираем все задачи и работаем с первой найденной по имени. Нужно проверять, имеются ли еще задачи с таким именем и выводить их в консоль. Помимо имени должны быть указаны: колонка, в которой находится эта задача, и другие параметры, по которым можно было бы отличить одну задачу от другой. Пользователю должно быть предложено дополнительно ввести (при помощи функции input) номер для выбора задачи из полученного списка. Наш клиент должен работать с выбранной задачей.

# Подготовка проекта

## Создание виртуального окружения
Для создания виртуального окружения перейдите в директорию проекта и выполните:

```
python -m venv .venv
```
Чтобы начать пользоваться виртуальным окружением, необходимо его активировать:
```
.venv\Scripts\activate.bat - для Windows;
.ven/bin/activate - для Linux и MacOS:
```
Потом можно обновить pip:
```
python -m pip install --upgrade pip
```
При выполнении следующей команды можно устанавливать пакеты, исползованные в проекте:
```
pip install -r requirements.txt
```

~~Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process~~

~~deactivate~~

## Подготовка "environment variables"

Создайте файл с именем ".env".

И вместо многоточия введите ваши значения:

``` json
{"Schlüssel": "...",
"Token": "...",
"board_id": "..."}
```
Как их получить описанно в ["D1.6 Интеграция API через библиотеки"](https://lms.skillfactory.ru/courses/course-v1:Skillfactory+PWS-15-18+21FEB2020/courseware/26595371e1db48c58a2259abb8a3b1c3/5f069b5f9ddb4b7b95b00c4131a28d69/1?activate_block_id=block-v1%3ASkillfactory%2BPWS-15-18%2B21FEB2020%2Btype%40vertical%2Bblock%406307fdfefccc473cb8f58c77fc2097ea)

# Работа с проектом

Откройте консоли и перейдите в директорию проекта.

Вся работа с программой осуществляется через консоль.

В программе реализованы следующие комманды:

1. python Trello.py -- получим данные всех колонок на доске

1. python Trello.py createcards "имя колонки" -- создадим колонку с именем "имя колонки" на текущей доске.

1. python Trello.py createlists "имя задачи" "имя колонки" -- создадим с именем "имя задачи" в колонке с именем "имя колонки"

1. python Trello.py move "имя задачи" "имя колонки" -- перемещение задачи с именем "имя задачи" в нужную колонку с именем "имя колонки"
