import _ba, os
import time

def client_to_account(client_id):
    rost = _ba.get_game_roster()
    for i in rost:
        if i['client_id'] == client_id:
            return i['account_id']
    return ''

def client_to_display_string(client_id):
    rost = _ba.get_game_roster()
    for i in rost:
        if i['client_id'] == client_id:
            return i['display_string']
    return ''

def client_to_player(client_id):
    rost = _ba.get_game_roster()
    for i in rost:
        if i['client_id'] == client_id:
            if len(i['players']) >= 1:
                return i['players'][0]['name_full']
            return i['display_string']
    return ''

def display_string_to_accounts(account_name):
    session = _ba.get_foreground_host_session()
    accounts = []
    for account_id in session.localPlayersData['stats']:
        if 'account name' in session.localPlayersData['stats'][account_id] and account_name in session.localPlayersData['stats'][account_id]['account name']:
            if account_id not in accounts:
                accounts.append(account_id)
    for account_id in session.playersData['stats']:
        if 'account name' in session.playersData['stats'][account_id] and account_name in session.playersData['stats'][account_id]['account name']:
            if account_id not in accounts:
                accounts.append(account_id)
    return accounts

def account_to_account_names(account_id):
    session = _ba.get_foreground_host_session()
    account_names = []
    if account_id in session.localPlayersData['stats'] and 'account name' in session.localPlayersData['stats'][account_id]:
        for name in session.localPlayersData['stats'][account_id]['account name']:
            if name not in account_names:
                account_names.append(name)
    if account_id in session.playersData['stats'] and 'account name' in session.playersData['stats'][account_id]:
        for name in session.playersData['stats'][account_id]['account name']:
            if name not in account_names:
                account_names.append(name)
    return account_names

def account_to_display_string(account_id):
    rost = _ba.get_game_roster()
    for i in rost:
        if i['account_id'] == account_id:
            return i['display_string']
    account_names = account_to_account_names(account_id)
    if len(account_names) != 0:
        return account_names[-1]
    return ''
