import ba, _ba

description = 'отключить завершение игры'

def extract_args(client_id, account_id, command):
    return True

def run_command(client_id, account_id, type, command_keys):
    blockend()

def blockend():
    from chatHandle.chat_functions import showmessage, _light_yellow_
    activity = ba.getactivity()
    if hasattr(activity, 'end_game'):
        if hasattr(activity, 'blockend') and activity.blockend:
            activity.blockend = False
            activity._has_ended = False
            showmessage(-1, 2, 'игра закончится в обычном режиме', _light_yellow_)
        else:
            activity.blockend = True
            showmessage(-1, 2, 'игра продолжается бесконечно', _light_yellow_)