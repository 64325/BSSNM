import _ba, os, json

def get_free_role(status, account_id):
    session = _ba.get_foreground_host_session()
    from ModData.allow import get_allow_status
    if get_allow_status(session.playersData['allow_data'], status, 0, account_id, 'free_role') == 'disallow':
        return None
    """
    from ModData.ranking import get_rank, in_rating
    if not in_rating(account_id):
        return None
    rank = get_rank(account_id)
    if rank == 1:
        return 'ADMINISTRATOR'
    elif rank <= 10:
        return 'VIP'
    else:
        return None
    """
    return None
