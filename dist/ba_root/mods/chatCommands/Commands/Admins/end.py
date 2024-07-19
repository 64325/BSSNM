import ba, _ba

description = 'закончить игру'

def extract_args(client_id, account_id, command):
    return True

def run_command(client_id, account_id, type, command_keys):
    end()

def end():
    from chatHandle.chat_functions import showmessage, _light_yellow_
    activity = ba.getactivity()
    from ba._activitytypes import JoinActivity, TransitionActivity
    if isinstance(activity, ba.GameActivity) or not isinstance(activity, JoinActivity) and len(activity.session.sessionplayers) > 0:
        activity.blockend = False
        results = ba.GameResults()
        activity.end(results=results)
        showmessage(-1, 2, 'завершение...', _light_yellow_)