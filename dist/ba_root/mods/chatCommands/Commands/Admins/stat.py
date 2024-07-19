import math

import ba, _ba

description = 'скрыть/показать рейтинг'
info = [
    '    скрыть статистику:   /stat hide',
    '    показать статистику:   /stat show'
]

using_players_ids = True
using_pb_ids = True

def extract_args(client_id, account_id, command):
    from chatHandle.chat_functions import showmessage, _red_
    if 'hide' in command['args']:
        command['args'].remove('hide')
        command['parsed_keys']['action'] = 'hide'
    elif 'show' in command['args']:
        command['args'].remove('show')
        command['parsed_keys']['action'] = 'show'
    else:
        showmessage(client_id, command['type'], 'напишите hide или show', _red_)
        return False
    return True

def run_command(client_id, account_id, type, command_keys, pb_id, acc_name):
    if command_keys['action'] == 'hide':
        hide_stat(client_id, account_id, type, pb_id, acc_name)
    else:
        show_stat(client_id, account_id, type, pb_id, acc_name)

def hide_stat(client_id, account_id, type, pb_id, acc_name):
    from ModData import effects
    attrs = {
        'hide': True
    }
    effects.add_effect(pb_id, acc_name, 'stat', attrs)
    activity = ba.getactivity()
    activity.session.update_effects()
    from ModData.account_info import client_to_account
    for player in activity.players:
        if client_to_account(player.sessionplayer.inputdevice.client_id) == pb_id:
            if player.actor:
                player.actor.set_ranktag()

def show_stat(client_id, account_id, type, pb_id, acc_name):
    from ModData import effects
    attrs = {
        'hide': True
    }
    effects.remove_effect(pb_id, 'stat')
    activity = ba.getactivity()
    activity.session.update_effects()
    from ModData.account_info import client_to_account
    for player in activity.players:
        if client_to_account(player.sessionplayer.inputdevice.client_id) == pb_id:
            if player.actor:
                player.actor.set_ranktag()
