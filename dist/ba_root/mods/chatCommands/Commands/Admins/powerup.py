import ba, _ba

description = 'включить/выключить поверапы'
timer_compatible = True

def extract_args(client_id, account_id, command):
    return True

def run_command(client_id, account_id, type, command_keys):
    powerups()

def powerups():
    from chatHandle.chat_functions import showmessage, _light_yellow_
    activity = ba.getactivity()
    if not hasattr(activity, '_powerup_drop_timer') or activity._powerup_drop_timer == None:
        showmessage(-1, 2, 'поверапы включены', _light_yellow_)
        activity.setup_standard_powerup_drops(enable_tnt=False)
    else:
        showmessage(-1, 2, 'поверапы выключены', _light_yellow_)
        activity._powerup_drop_timer = None