import _ba, os, json
import time

data_path = os.path.join(_ba.env()['python_directory_user'],"playersData" + os.sep)   
                                                                    
def load_warnlist():
    with open(data_path+'warnlist.json', 'r') as f:
        warnlist = json.load(f)
    for account_id in list(warnlist):
        if 'until' in warnlist[account_id] and time.mktime(time.strptime(warnlist[account_id]['until'])) < time.time():
            warnlist.pop(account_id)
    return warnlist

def create_warn(account_name, reason, warn_time, warn_interval):
    warn = {}
    if account_name != '':
        warn['account name'] = account_name
    warn['count'] = 1
    warn['reasons'] = [reason]
    if warn_interval != None:
        warn['until'] = time.ctime(warn_time + warn_interval)
    return warn

def add_warn(account_id, account_name, reason, warn_time, warn_interval):
    warnlist = load_warnlist()
    if account_id in warnlist:
        warnlist[account_id]['count'] += 1
        warnlist[account_id]['reasons'].append(reason)
    else:
        warnlist[account_id] = create_warn(account_name, reason, warn_time, warn_interval)
    save_warnlist(warnlist)

def remove_warn(account_id):
    warnlist = load_warnlist()
    if account_id in warnlist:
        warnlist.pop(account_id)
    save_warnlist(warnlist)

def save_warnlist(warnlist):
    with open(data_path+'warnlist.json', 'w') as f:
        json.dump(warnlist, f, indent=4, ensure_ascii=False)
