import ba, _ba

description = 'поставить на паузу'

def extract_args(client_id, account_id, command):
    return True

def run_command(client_id, account_id, type, command_keys):
    pause()

def pause():
    from chatHandle.chat_functions import showmessage, _light_yellow_
    activity = ba.getactivity()
    if activity.globalsnode.paused:
        showmessage(-1, 2, 'игра продолжается', _light_yellow_)
        activity.globalsnode.paused = False
    else:
        showmessage(-1, 2, 'пауза', _light_yellow_)
        activity.globalsnode.paused = True