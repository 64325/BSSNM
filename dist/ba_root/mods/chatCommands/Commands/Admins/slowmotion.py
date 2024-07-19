import ba, _ba

aliases = ['sm']
description = 'замедленный режим'

def extract_args(client_id, account_id, command):
    return True

def run_command(client_id, account_id, type, command_keys):
    slowmotion()

def slowmotion():
    activity = ba.getactivity()
    activity.globalsnode.slow_motion = not activity.globalsnode.slow_motion