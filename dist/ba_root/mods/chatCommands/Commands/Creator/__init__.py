import os
from importlib import import_module

__all__ = []
# Перебор файлов в директории, добавление их в список __all__
for filename in os.listdir(__path__[0]):
    if not filename.startswith('_') and filename.endswith('.py'):
        __all__.append(filename[:-3])

# Импортирование всех подмодулей
for submodule_name in __all__:
    try:
        import_module(__name__ + '.' + submodule_name)  # Импортирование подмодуля
    except SyntaxError as error:
        print(error)  # Вывод ошибки синтаксиса, если она произошла
        print('не удалось добавить команду ' + submodule_name + '  (' + __name__ + ')')  # Сообщение о неудачном добавлении команды

# Функция для проверки прав доступа
def check_permission(client_id, account_id, account_name, command_name):
    if client_id == -1:
        return True  # Если client_id равен -1, права доступа подтверждаются
    from ModData.me import get_role
    role = get_role(account_id, account_name, client_id)  # Получение роли пользователя
    if role == 'CREATOR':
        return True  # Если роль пользователя "CREATOR", права доступа подтверждаются
    else:
        return False  # В остальных случаях права доступа не подтверждаются
