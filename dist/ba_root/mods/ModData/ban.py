import _ba, os, json
import time

data_path = os.path.join(_ba.env()['python_directory_user'],"playersData" + os.sep)

def load_banlist():
    with open(data_path+'banlist.json', 'r') as f:
        banlist = json.load(f)
    for account_id in list(banlist):
        if 'until' in banlist[account_id] and time.mktime(time.strptime(banlist[account_id]['until'])) < time.time():
            banlist.pop(account_id)
    return banlist

def create_ban(account_name, admin_id, reason, ban_time, ban_interval):
    ban = {}
    if account_name != '':
        ban['account name'] = account_name
    ban['banned by'] = admin_id
    if reason != '':
        ban['reason'] = reason
    ban['date'] = time.ctime(ban_time)
    if ban_interval != None:
        ban['until'] = time.ctime(ban_time + ban_interval)
    return ban

def add_ban(account_id, account_name, admin_id, reason, ban_time, ban_interval):
    banlist = load_banlist()
    banlist[account_id] = create_ban(account_name, admin_id, reason, ban_time, ban_interval)
    save_banlist(banlist)

def remove_ban(account_id):
    banlist = load_banlist()
    if account_id in banlist:
        banlist.pop(account_id)
    save_banlist(banlist)

def save_banlist(banlist):
    with open(data_path+'banlist.json', 'w') as f:
        json.dump(banlist, f, indent=4, ensure_ascii=False)
