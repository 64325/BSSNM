import time

import ba, _ba

description = 'заспавнить мяч'

using_players_ids = True
timer_compatible = True

def extract_args(client_id, account_id, command):
    command['name'] = 'spawn'
    command['args'] = ['ball'] + command['args']
    return True

def run_command(client_id, account_id, type, command_keys, pb_id, acc_name):
    pass