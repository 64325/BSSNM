import math

import ba, _ba

description = 'изменить цвет топа'
info = [
    '                               изменить цвет топа',
    '                                 /topcolor clr=цвет',
    '                               сбросить цвет топа',
    '                                     /topcolor del'
]

timer_compatible = True

def extract_args(client_id, account_id, command):
    from chatHandle.chat_functions import showmessage, _red_
    if 'del' in command['args']:
        command['args'].remove('del')
        command['parsed_keys']['action'] = 'delete'
        return True
    command['parsed_keys']['action'] = 'set'
    if len(command['keys']) == 0:
        showmessage(client_id, command['type'], 'укажите цвет', _red_)
        return False
    command['parsed_keys']['color'] = []
    from ba._activity import actor_colors, actor_animations
    if 'clr' in command['keys']:
        if len(command['keys']['clr']) == 1:
            color = command['keys']['clr'][0]
            command['keys'].pop('clr')
            if color not in actor_colors and color not in actor_animations:
                showmessage(client_id, command['type'], color + ': цвет не найден', _red_)
                return False
            command['parsed_keys']['color'] = color
        elif len(command['keys']['clr']) == 3:
            try:
                for i in range(3):
                    value = float(command['keys']['clr'][0])
                    command['keys']['clr'].pop(0)
                    command['parsed_keys']['color'].append(value)
                command['keys'].pop('clr')
            except:
                return False
    return True

def run_command(client_id, account_id, type, command_keys):
    if command_keys['action'] == 'delete':
        remove_topcolor()
    else:
        set_topcolor(command_keys['color'])

def remove_topcolor():
    from ModData import server_data as sd
    server_data = sd.load_server_data()
    server_data.pop('topcolor')
    sd.save_server_data(server_data)
    session = _ba.get_foreground_host_session()
    session.load_server_data()
    activity = ba.getactivity()
    if hasattr(activity, 'on_screen_text') and 'toplist' in activity.on_screen_text:
        if activity.on_screen_text['season_name']:
            activity.on_screen_text['season_name'].delete()
        if activity.on_screen_text['update_info']:
            activity.on_screen_text['update_info'].delete()
        if activity.on_screen_text['toplist']:
            activity.on_screen_text['toplist'].delete()
        activity.show_server_top()

def set_topcolor(color):
    from ModData import server_data as sd
    server_data = sd.load_server_data()
    server_data['topcolor'] = color
    sd.save_server_data(server_data)
    session = _ba.get_foreground_host_session()
    session.load_server_data()
    activity = ba.getactivity()
    if hasattr(activity, 'on_screen_text') and 'toplist' in activity.on_screen_text:
        if activity.on_screen_text['toplist']:
            activity.on_screen_text['toplist'].delete()
        activity.show_server_top()
