import math

import ba, _ba

description = 'изменить освещение'
info = [
    '                              изменить освещение',
    '                                     /tint   r   g   b',
    '                            вернуть исходный цвет',
    '                                            /tint'
]

timer_compatible = True

def extract_args(client_id, account_id, command):
    from chatHandle.chat_functions import showmessage, _red_
    if len(command['args']) == 0:
        command['parsed_keys']['float1'] = 1.0
        command['parsed_keys']['float2'] = 1.0
        command['parsed_keys']['float3'] = 1.0
        return True
    try:
        for i in range(3):
            value = float(command['args'][0])
            command['args'].pop(0)
            command['parsed_keys']['float'+str(i+1)] = value
    except:
        return False
    return True

def run_command(client_id, account_id, type, command_keys):
    set_tint(command_keys['float1'], command_keys['float2'], command_keys['float3'])

def set_tint(*color):
    activity = ba.getactivity()
    if not hasattr(activity, 'default_tint'):
        activity.default_tint = (activity.globalsnode.tint[0], activity.globalsnode.tint[1], activity.globalsnode.tint[2])
    activity.globalsnode.tint = (color[0] * activity.default_tint[0], color[1] * activity.default_tint[1], color[2] * activity.default_tint[2])
    activity.current_tint = activity.globalsnode.tint
