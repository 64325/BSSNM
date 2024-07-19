import os
from importlib import import_module

import _ba

__all__ = []
for filename in os.listdir(__path__[0]):
    if not filename.startswith('_') and filename.endswith('.py'):
        __all__.append(filename[:-3])

#from . import *
for submodule_name in __all__:
    try:
        import_module(__name__ + '.' + submodule_name)
    except SyntaxError as error:
        print(error)
        print('не удалось добавить команду ' + submodule_name + '  (' + __name__ + ')')

def check_permission(client_id, account_id, account_name, command_name):
    if client_id == -1:
        return True
    session = _ba.get_foreground_host_session()
    if account_id in session.playersData['mutelist']:
        return False
    from ModData.me import get_role
    role = get_role(account_id, account_name, client_id)
    if role in session.serverData['server_roles'] and command_name in session.serverData['server_roles'][role]['commands']:
        return True
    else:
        return False
