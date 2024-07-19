import _ba, ba
import os, json
import time

data_path = os.path.join(_ba.env()['python_directory_user'],"playersData" + os.sep)


from typing import Any, Sequence, Optional, Union

                                                            
def load_allow_data():
    with open(data_path+'allow_data.json', 'r') as f:
        allow_data = json.load(f)
    new_allow_data = []
    for allow in allow_data:
        if 'until' in allow and time.mktime(time.strptime(allow['until'])) < time.time():
            #allow_data.remove(allow)
            pass
        else:
            new_allow_data.append(allow)
    return new_allow_data

def execute_allow(subject, action, type, subtype, admin_id, allow_time, allow_interval, count, self_only):
    new_allow = {
        'subject': subject,
        'action': action,
        'type': type
    }
    if subtype != None:
        new_allow['subtype'] = subtype
    new_allow['admin'] = admin_id
    new_allow['date'] = time.ctime(allow_time)
    if allow_interval != None:
        new_allow['until'] = time.ctime(allow_time + allow_interval)
    if count != None:
        new_allow['count'] = count
    if self_only:
        new_allow['action'] = 'self_only'
    allow_data = load_allow_data()
    new_allow_data = []
    for allow in allow_data:
        if allow['subject'] != new_allow['subject']:
            new_allow_data.append(allow)
        elif allow['type'] != new_allow['type']:
            new_allow_data.append(allow)
        elif 'subtype' in new_allow and ('subtype' not in allow or allow['subtype'] != new_allow['subtype']):
            new_allow_data.append(allow)
        else:
            pass
    if new_allow['action'] != 'default':
        new_allow_data.append(new_allow)
    save_allow_data(new_allow_data)

def use_allow(account_id, type, subtype=None):
    allow_data = load_allow_data()
    for allow in allow_data:
        if allow['subject'] == account_id and allow['action'] != 'disallow' and allow['type'] == type and 'subtype' in allow and allow['subtype'] == subtype:
            if 'count' in allow:
                allow['count'] -= 1
                if allow['count'] == 0:
                    allow_data.remove(allow)
                save_allow_data(allow_data)
            return
    for allow in allow_data:
        if allow['subject'] == account_id and allow['action'] != 'disallow' and allow['type'] == type and 'subtype' not in allow:
            if 'count' in allow:
                allow['count'] -= 1
                if allow['count'] == 0:
                    allow_data.remove(allow)
                save_allow_data(allow_data)
            return

def save_allow_data(allow_data):
    with open(data_path+'allow_data.json', 'w') as f:
        json.dump(allow_data, f, indent=4, ensure_ascii=False)


def get_allow_status(allow_data, role, rank, account_id, type, subtype = None, default = 'default'):
    if role == 'CREATOR':
        return 'allow'
    result = default
    if subtype != None:
        for subject in ['ALL', role, 'TOP', account_id]:
            for allow in allow_data:
                if allow['subject'] == subject and allow['type'] == type and 'subtype' not in allow:
                    if subject == 'TOP' and rank != None and rank <= allow['top'] and (result == 'default' or result == 'disallow') or subject != 'TOP':
                        result = allow['action']
        for subject in ['ALL', role, 'TOP', account_id]:
            for allow in allow_data:
                if allow['subject'] == subject and allow['type'] == type and 'subtype' in allow and allow['subtype'] == subtype:
                    if subject == 'TOP' and rank != None and rank <= allow['top'] and (result == 'default' or result == 'disallow') or subject != 'TOP':
                        result = allow['action']
    else:
        for subject in ['ALL', role, 'TOP', account_id]:
            for allow in allow_data:
                if allow['subject'] == subject and allow['type'] == type and 'subtype' not in allow:
                    if subject == 'TOP' and rank != None and rank <= allow['top'] and (result == 'default' or result == 'disallow') or subject != 'TOP':
                        result = allow['action']
            for allow in allow_data:
                if allow['subject'] == subject and allow['type'] == type and 'subtype' in allow:
                    if subject == 'TOP' and rank != None and rank <= allow['top'] and (result == 'default' or result == 'disallow') or subject != 'TOP':
                        if allow['action'] != 'disallow':
                            result = 'allow'
    return result
