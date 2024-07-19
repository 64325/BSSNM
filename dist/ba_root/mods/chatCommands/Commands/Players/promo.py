import os

import ba, _ba
import json

data_path = os.path.join(_ba.env()['python_directory_user'], "serverData" + os.sep)  # Путь к данным

description = 'ввести промокод'  # Описание команды
info = [
    'напишите /promo и промокод'
]

invisible_command = True

# Функция для извлечения аргументов команды
def extract_args(client_id, account_id, command):
    if len(command['args']) != 0:
        try:
            value = command['args'][0]
            command['args'].pop(0)  # Удаление первого аргумента из списка
        except:
            return False
        command['parsed_keys']['promocode'] = value  # Сохранение промокода в команду
    return True

# Функция для выполнения команды
def run_command(client_id, account_id, type, command_keys):
    if 'promocode' in command_keys:
        promocode = command_keys['promocode']
        apply_promocode(client_id, type, promocode)  # Вызов функции для применения промокода

# Функция для применения промокода
def apply_promocode(client_id, type, promocode):
    from chatHandle.chat_functions import showmessage, _white_
    session = _ba.get_foreground_host_session()
    filename = data_path + "promocode.json"
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                promocode_data = json.load(f)  # Загрузка данных промокодов
            if promocode in promocode_data['disposable_promocode']:
                msg = promocode_data['disposable_promocode'][promocode].format(client_id=client_id)
                promocode_data['disposable_promocode'].pop(promocode)  # Удаление использованного промокода
                if not 'old' in promocode_data:
                    promocode_data['old'] = []
                if not msg in promocode_data['old']:
                    promocode_data['old'].append(msg)  # Сохранение сообщения в старые промокоды
                with open(filename, 'w') as f:
                    json.dump(promocode_data, f, indent=4, ensure_ascii=False)  # Сохранение обновленных данных
                _ba.chatmessage('$' + msg, sender_override=ba.charstr(ba.SpecialChar.PARTY_ICON) + ' ')  # Отправка сообщения в чат
            elif promocode in promocode_data['promocode']:
                msg = promocode_data['promocode'][promocode].format(client_id=client_id)
                _ba.chatmessage('$' + msg, sender_override=ba.charstr(ba.SpecialChar.PARTY_ICON) + ' ')  # Отправка сообщения в чат для многократного промокода
        except:
            pass
