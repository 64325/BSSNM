import time

import ba, _ba

description = 'выдать игроку статус ADMINISTRATOR'
info = [
    '               выдать привилегию ADMINISTRATOR',
    '             /admin   номер игрока или pb-id   t=время',
    '            без указания времени выдаётся на месяц',
    '                     forever чтобы выдать навсегда'
]

using_players_ids = True
using_pb_ids = True

def extract_args(client_id, account_id, command):
    command['name'] = 'setstatus'
    command['args'] = ['ADMINISTRATOR'] + command['args']
    return True

def run_command(client_id, account_id, type, command_keys, pb_id, acc_name):
    pass