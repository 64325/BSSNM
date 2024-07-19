import ba, _ba

description = 'открыть лобби'

def extract_args(client_id, account_id, command):
    return True

def run_command(client_id, account_id, type, command_keys):
    unblock_lobby()

def unblock_lobby():
    _ba.get_foreground_host_session().lobby_blocked = False