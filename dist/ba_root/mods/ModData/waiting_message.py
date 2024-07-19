import _ba, os, json
import time

data_path = os.path.join(_ba.env()['python_directory_user'],"playersData" + os.sep)   
                                                                    
def load_messages():
    with open(data_path+'waiting_messages.json', 'r') as f:
        messages = json.load(f)
    for account_id in list(messages):
        while len(messages[account_id]['messages']) > 0 and time.mktime(time.strptime(messages[account_id]['dates'][0])) + 30.0 * 24.0 * 60.0 * 60.0 < time.time():
            messages[account_id]['messages'].pop(0)
            messages[account_id]['colors'].pop(0)
            messages[account_id]['dates'].pop(0)
            if len(messages[account_id]['messages']) == 0:
                messages.pop(account_id)
                break
    return messages

def create_message(account_name, msg, color, msg_time):
    message = {
        'account name': [account_name],
        'messages': [msg],
        'colors': [color],
        'dates': [time.ctime(msg_time)]
    }
    return message

def add_message(account_id, account_name, msg, color, msg_time):
    messages = load_messages()
    if account_id in messages:
        messages[account_id]['messages'].append(msg)
        messages[account_id]['colors'].append(color)
        messages[account_id]['dates'].append(time.ctime(msg_time))
    else:
        messages[account_id] = create_message(account_name, msg, color, msg_time)
    save_messages(messages)

def pop_message(account_id):
    messages = load_messages()
    if account_id in messages:
        messages[account_id]['messages'].pop(0)
        messages[account_id]['colors'].pop(0)
        messages[account_id]['dates'].pop(0)
        if len(messages[account_id]['messages']) == 0:
            messages.pop(account_id)
    save_messages(messages)

def save_messages(messages):
    with open(data_path+'waiting_messages.json', 'w') as f:
        json.dump(messages, f, indent=4, ensure_ascii=False)
