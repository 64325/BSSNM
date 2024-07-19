import _ba, os, json
import time

data_path = os.path.join(_ba.env()['python_directory_user'],"playersData" + os.sep)

def load_stats():
    with open(data_path+'stats.json', 'r') as f:
        real_stats = json.load(f)
    return real_stats

def create_profile(account_name):
    profile_stats = {
        'account name': [account_name],
        'last player name': ''
    }
    return profile_stats

def get_value(stats, account_id, parameter):
    if account_id not in stats or parameter not in stats[account_id]:
        return 0
    else:
        return stats[account_id][parameter]

def set_value(stats, account_id, parameter, value=0):
    if account_id not in stats:
        stats[account_id] = create_profile(profile_stats['account name'][0])
    stats[account_id][parameter] = value

def increase_value(stats, account_id, parameter, value=1):
    if account_id not in stats:
        stats[account_id] = create_profile(profile_stats['account name'][0])
    if parameter not in stats[account_id]:
        set_value(stats, account_id, parameter)
    stats[account_id][parameter] += value

def delete_profile(stats, account_id):
    if account_id in stats:
        stats.pop(account_id)
    return stats

def update_profile(stats, account_id, profile_stats):
    if not account_id in stats:
        stats[account_id] = create_profile(profile_stats['account name'][0])

    #placing latest account names in the end
    for account_name in profile_stats['account name']:
        if account_name in stats[account_id]['account name']:
            stats[account_id]['account name'].remove(account_name)
        stats[account_id]['account name'].append(account_name)

    if 'last player name' in profile_stats and profile_stats['last player name'] != '':
        stats[account_id]['last player name'] = profile_stats['last player name']

    for parameter in profile_stats:
        if parameter not in ['account name', 'last player name']:
            if parameter not in stats[account_id]:
                stats[account_id][parameter] = 0
            stats[account_id][parameter] += profile_stats[parameter]

def update_stats(stats):
    real_stats = load_stats()
    for account_id in stats:
        update_profile(real_stats, account_id, stats[account_id])
    with open(data_path+'stats.json', 'w') as f:
        json.dump(real_stats,f,indent=4, ensure_ascii=False)

def backup_stats():
    from shutil import copy2
    copy2(data_path+'stats.json', data_path+'stats_backup.json')

def recover_stats():
    from shutil import copy2
    copy2(data_path+'stats_backup.json', data_path+'stats.json')

def reset_stats():
    with open(data_path+'stats.json', 'w') as f:
        json.dump({},f,indent=4, ensure_ascii=False)
