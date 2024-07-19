import ba, _ba

description = 'перезагрузка сервера'

def extract_args(client_id, account_id, command):
    return True

def run_command(client_id, account_id, type, command_keys):
    restart()

def restart():
    from bacommon.servermanager import ShutdownReason
    _ba.app.server.shutdown(ShutdownReason.RESTARTING, immediate=True)