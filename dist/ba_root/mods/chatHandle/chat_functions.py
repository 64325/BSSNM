from __future__ import annotations

from typing import TYPE_CHECKING

import _ba, ba

_red_ = (1.0, 0.1, 0.0)
_white_ = (0.9, 0.9, 0.9)
_black_ = (0.0, 0.0, 0.0)
_light_yellow_ = (1.0, 0.85, 0.3)
_light_green_ = (0.5, 1.0, 0.5)
_yellow_ = (1.0, 1.0, 0.0)
_clanwar_color_ = (0.9, 0.0, 0.4)

# Функция для преобразования времени из формата строки
def translate_time(time_str):
    t = time_str.split(' ')
    while '' in t:
        t.remove('')
    time_of_day = t[3].split(':')
    months = {
        'Jan': '01',
        'Feb': '02',
        'Mar': '03',
        'Apr': '04',
        'May': '05',
        'Jun': '06',
        'Jul': '07',
        'Aug': '08',
        'Sep': '09',
        'Oct': '10',
        'Nov': '11',
        'Dec': '12'
    }
    return t[2] + '.' + months[t[1]] + '.' + t[4] + ' ' + time_of_day[0] + ':' + time_of_day[1]

# Функция для определения типа строки
def string_type(s):
    if s == None or s == '':
        return None
    if s.startswith('pb-'):
        if '"' not in s and "'" not in s:
            return 'pb_id'
    if s.startswith('') or s.startswith('') or s.startswith(''):
        if '"' not in s and "'" not in s:
            return 'account_name'
    if s[0].isnumeric():
        return 'number'
    if s[0] == '&' and string_type(s[1:]) == 'name':
        return 'package'
    if s[0] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя':
        for c in s:
            if c not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя_0123456789.+':
                return 'notype'
        return 'name'
    return 'notype'

# Функция для отображения сообщений
def showmessage(client_id, type, s, color = (1.0, 1.0, 1.0), sender = None):
    if type == 1:
        if sender != None:
            _ba.chatmessage('  ' + s, sender_override=sender)  # Отправить чат-сообщение с отправителем, если указан
        else:
            _ba.chatmessage('  ' + s, sender_override=ba.charstr(ba.SpecialChar.PARTY_ICON) + ' ')  # Отправить чат-сообщение с иконкой вечеринки
        return
    elif type == 2:
        while len(s) > 0 and s[0] == ' ': s = s[1:]  # Удалить ведущие пробелы в строке s
        if client_id == -1:
            _ba.screenmessage(s, color = color, transient=True)  # Отобразить экранные сообщения без указания клиента
        else:
            _ba.screenmessage(s, color = color, transient=True, clients=[client_id])  # Отобразить экранные сообщения для конкретного клиента
        return
    elif type == 3:
        if sender != None and len(sender) >= 14:
            sender = sender[:11] + '...'  # Обрезать отправителя до 14 символов
        if client_id == -1:
            if sender != None:
                _ba.chatmessage('  ' + s, sender_override=sender)  # Отправить чат-сообщение с отправителем, если указан
            else:
                _ba.chatmessage('  ' + s)  # Отправить обычное чат-сообщение
        else:
            if sender != None:
                _ba.chatmessage('  ' + s, sender_override=sender, clients=[client_id])  # Отправить чат-сообщение с отправителем и указанием клиента
            else:
                _ba.chatmessage('  ' + s, sender_override=ba.charstr(ba.SpecialChar.DICE_BUTTON1) + ba.charstr(ba.SpecialChar.PARTY_ICON) + ' ', clients=[client_id])  # Отправить чат-сообщение с иконками для клиента
        return
