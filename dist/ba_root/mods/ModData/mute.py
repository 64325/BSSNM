import _ba, os, json
import time

data_path = os.path.join(_ba.env()['python_directory_user'],"playersData" + os.sep)

def load_mutelist():
    with open(data_path+'mutelist.json', 'r') as f:
        mutelist = json.load(f)
    for account_id in list(mutelist):
        if 'until' in mutelist[account_id] and time.mktime(time.strptime(mutelist[account_id]['until'])) < time.time():
            mutelist.pop(account_id)
    return mutelist

def create_mute(account_name, admin_id, reason, mute_time, mute_interval):
    mute = {}
    if account_name != '':
        mute['account name'] = account_name
    mute['muted by'] = admin_id
    if reason != '':
        mute['reason'] = reason
    mute['date'] = time.ctime(mute_time)
    if mute_interval != None:
        mute['until'] = time.ctime(mute_time + mute_interval)
    return mute

def add_mute(account_id, account_name, admin_id, reason, mute_time, mute_interval):
    mutelist = load_mutelist()
    mutelist[account_id] = create_mute(account_name, admin_id, reason, mute_time, mute_interval)
    save_mutelist(mutelist)

def remove_mute(account_id):
    mutelist = load_mutelist()
    if account_id in mutelist:
        mutelist.pop(account_id)
    save_mutelist(mutelist)

def save_mutelist(mutelist):
    with open(data_path+'mutelist.json', 'w') as f:
        json.dump(mutelist, f, indent=4, ensure_ascii=False)
