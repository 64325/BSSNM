import os
from importlib import import_module

__all__ = []
for filename in os.listdir(__path__[0]):  # Перебираем все файлы в директории
    if not filename.startswith('_') and filename.endswith('.py'):  # Проверяем, что файл не начинается с '_' и имеет расширение '.py'
        __all__.append(filename[:-3])  # Добавляем имя файла без расширения '.py' в список __all__

#from . import *
for submodule_name in __all__:  # Импортируем каждый модуль из списка __all__
    try:
        import_module(__name__ + '.' + submodule_name)  # Пытаемся импортировать модуль
    except SyntaxError as error:  # Обрабатываем синтаксическую ошибку
        print(error)  # Выводим сообщение об ошибке
        print('не удалось добавить команду ' + submodule_name + '  (' + __name__ + ')')  # Выводим сообщение о неудачном добавлении команды

def check_permission(client_id, account_id, account_name, command_name):  # Определяем функцию для проверки разрешений
    return True  # Возвращаем True
