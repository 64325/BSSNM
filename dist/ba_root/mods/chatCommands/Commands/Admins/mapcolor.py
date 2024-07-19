import math

import ba, _ba

description = 'изменить цвет карты'
info = [
    '                              изменить цвет карты',
    '                                 /mapcolor   r   g   b',
    '                            вернуть исходный цвет',
    '                                         /mapcolor'
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
    set_mapcolor(command_keys['float1'], command_keys['float2'], command_keys['float3'])

def set_mapcolor(*color):
    activity = ba.getactivity()
    if hasattr(activity, 'map') and hasattr(activity.map, 'node') and activity.map.node:
        activity.map.node.color = color
    if hasattr(activity, 'map') and hasattr(activity.map, 'bottom') and activity.map.bottom:
        activity.map.bottom.color = color
