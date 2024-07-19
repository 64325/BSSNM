import _ba, os, json
import time, math

data_path = os.path.join(_ba.env()['python_directory_user'],"playersData" + os.sep)

def get_parameter_value(account_id, parameter):
    from ModData import stats
    session = _ba.get_foreground_host_session()
    return stats.get_value(session.playersData['stats'], account_id, parameter) + stats.get_value(session.localPlayersData['stats'], account_id, parameter)

def in_rating(account_id):
    if _ba.app.server._playlist_name == 'Soccer':
        goals = get_parameter_value(account_id, 'goals')
        assists = get_parameter_value(account_id, 'assists')
        autogoals = get_parameter_value(account_id, 'autogoals')
        return goals > 0 or assists > 0
    else:
        kills = get_parameter_value(account_id, 'kills')
        return kills >= 5

def get_rank_score(account_id):
    from ModData import stats
    if _ba.app.server._playlist_name == 'Soccer':
        goals = get_parameter_value(account_id, 'goals')
        assists = get_parameter_value(account_id, 'assists')
        autogoals = get_parameter_value(account_id, 'autogoals')
        return 2 * goals + 1 * assists - 3 * autogoals
    else:
        kills = get_parameter_value(account_id, 'kills')
        deaths = get_parameter_value(account_id, 'deaths')
        return math.sqrt(float(kills) * float(kills) * float(kills) / (float(deaths) + 1) / (float(deaths) + 1))

def get_top_list(length = 0):
    session = _ba.get_foreground_host_session()
    values = {}
    for account_id in session.playersData['stats']:
        if in_rating(account_id):
            values[account_id] = -get_rank_score(account_id)
    toplist = sorted(values, key=values.get)
    if length != 0 and length < len(toplist):
        return toplist[:length]
    return toplist

def get_rank(account_id):
    session = _ba.get_foreground_host_session()
    top_list = session.playersData['toplist']
    if not in_rating(account_id) or not account_id in top_list:
        return len(top_list) + 1
    return top_list.index(account_id) + 1
