import _ba, os, json
import time

data_path = os.path.join(_ba.env()['python_directory_user'],"playersData" + os.sep)

def get_value(status):
    session = _ba.get_foreground_host_session()
    if status in session.serverData['server_roles']:
        return session.serverData['server_roles'][status]['value']
    else:
        return 0

def get_role(account_id, account_name = '', client_id = None):
    if client_id == -1:
        return 'CREATOR'
    rost = _ba.get_game_roster()
    for i in rost:
        if i['client_id'] == -1 and i['account_id'] == account_id:
            return 'CREATOR'
    session = _ba.get_foreground_host_session()
    if account_name != '' and account_id != '' and account_name in session.playersData['roles']:
        role = session.playersData['roles'][account_name]['role']
    elif account_id in session.playersData['roles']:
        role = session.playersData['roles'][account_id]['role']
    else:
        role = 'PLAYER'
    if account_name == '':
        from ModData.account_info import account_to_account_names
        account_names = account_to_account_names(account_id)
        for name in account_names:
            if name != '' and get_value(get_role(account_id, name)) > get_value(role):
                role = get_role(account_id, name)
    from ModData.free_role import get_free_role
    free_role = get_free_role(role, account_id)
    if free_role != None and get_value(free_role) >= get_value(role):
        return free_role
    return role

def get_me_info(client_id, account_id, account_name):
    from ModData import ranking
    client_str = '   ' if client_id == -1 else str(client_id)
    session = _ba.get_foreground_host_session()
    role = get_role(account_id, account_name)
    from ModData.account_info import account_to_account_names
    account_names = account_to_account_names(account_id)
    if account_name in account_names:
        account_names.remove(account_name)
    account_names = [account_name] + account_names
    me_info = {
        'client_id': ' - ' if client_id == -1 else str(client_id),
        'account_id': account_id,
        'account_name': account_name,
        'account_names': account_names,
        'role': get_role(account_id, account_name)
    }
    me_names = {
        'client_id': 'номер игрока',
        'account_id': 'ID',
        'account_name': 'имя аккаунта',
        'account_names': 'аккаунты',
        'role': 'статус'
    }
    if _ba.app.server._playlist_name == 'Soccer':
        me_info['scored'] = str(ranking.get_parameter_value(account_id, 'goals'))
        me_info['assists'] = str(ranking.get_parameter_value(account_id, 'assists'))
        me_info['autogoals'] = str(ranking.get_parameter_value(account_id, 'autogoals'))
        me_info['rank'] = 'не в рейтинге' if not ranking.in_rating(account_id) else '#' + str(ranking.get_rank(account_id))
        me_names['scored'] = 'голов'
        me_names['assists'] = 'гол.передач'
        me_names['autogoals'] = 'автоголов'
        me_names['rank'] = 'рейтинг'
    else:
        kills = ranking.get_parameter_value(account_id, 'kills')
        me_info['kills'] = str(kills)
        deaths = ranking.get_parameter_value(account_id, 'deaths')
        me_info['deaths'] = str(deaths)
        me_names['kills'] = 'убито'
        me_names['deaths'] = 'смертей'
        if deaths > 0:
            kd = str(round(kills / deaths, 2))
        elif kills == 0:
            kd = '0'
        else:
            kd = '∞'
        me_info['score'] = str(round(ranking.get_rank_score(account_id), 2))
        me_names['score'] = 'очки рейтинга'
        me_info['rank'] = 'не в рейтинге' if not ranking.in_rating(account_id) else '#' + str(ranking.get_rank(account_id))
        me_names['rank'] = 'рейтинг'
    return me_info, me_names
