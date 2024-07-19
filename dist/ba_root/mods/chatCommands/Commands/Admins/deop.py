import time

import ba, _ba

aliases = ['dp']
description = 'лишить игрока привилегии'
info = [
    '                          снять с игрока привилегию',
    '                        /deop   номер игрока или pb-id'
]

using_players_ids = True
using_pb_ids = True

def extract_args(client_id, account_id, command):
    command['name'] = 'setstatus'
    command['args'] = ['PLAYER'] + command['args']
    return True

def run_command(client_id, account_id, type, command_keys, pb_id, acc_name):
    pass