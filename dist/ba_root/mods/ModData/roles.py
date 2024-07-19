import _ba, os, json
import time

data_path = os.path.join(_ba.env()['python_directory_user'],"playersData" + os.sep)

def load_roles():
    with open(data_path+'roles.json', 'r') as f:
        roles = json.load(f)
    for account_id in list(roles):
        if 'until' in roles[account_id] and time.mktime(time.strptime(roles[account_id]['until'])) < time.time():
            roles.pop(account_id)
    return roles

def create_role(account_name, role, role_time, role_interval):
    role = {
        'account name': [account_name],
        'role': role
    }
    role['date'] = time.ctime(role_time)
    if role_interval != None:
        role['until'] = time.ctime(role_time + role_interval)
    return role

def add_role(account_id, account_name, role, role_time, role_interval):
    roles = load_roles()
    roles[account_id] = create_role(account_name, role, role_time, role_interval)
    save_roles(roles)

def remove_role(account_id):
    roles = load_roles()
    if account_id in roles:
        roles.pop(account_id)
    save_roles(roles)

def save_roles(roles):
    with open(data_path+'roles.json', 'w') as f:
        json.dump(roles, f, indent=4, ensure_ascii=False)
