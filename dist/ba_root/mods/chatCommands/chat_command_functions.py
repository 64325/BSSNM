from __future__ import annotations  # Используем новые аннотации типов

import os
import time

from typing import TYPE_CHECKING

import _ba, ba

def parse_time(str):
    timemarks = {'y': 365.0 * 24.0 * 60.0 * 60.0, 'w': 7.0 * 24.0 * 60.0 * 60.0, 'd': 24.0 * 60.0 * 60.0, 'h': 60.0 * 60.0, 'm': 60.0, 's': 1.0}
    time_interval = 0.0
    contains_marks = False
    for mark in timemarks:
        if mark in str:
            contains_marks = True
            break
    if not contains_marks: str += 's'  # Добавляем 's', если метки времени отсутствуют
    for mark in timemarks:
        i = str.find(mark)
        if i != -1:
            try:
                a = int(str[:i])
                if a < 0: return None
                time_interval += a * timemarks[mark]
                str = str[i + 1:]
            except:
                if mark == 's' and time_interval == 0:
                    try:
                        a = float(str[:i])
                        if a < 0: return None
                        time_interval += a * timemarks[mark]
                        str = str[i + 1:]
                    except:
                        return None
                else:
                    return None
    if str != '': return None
    return time_interval  # Возвращаем вычисленный временной интервал

def add_cooldown(account_id, command_name, time_interval):
    session = _ba.get_foreground_host_session()
    if account_id not in session.playersData['cooldown']:
        session.playersData['cooldown'][account_id] = {}
    session.playersData['cooldown'][account_id][command_name] = time.time() + time_interval  # Устанавливаем время окончания отката команды

def log_command(account_id, command_name, acc_id, comment=''):
    from chatHandle.chat_functions import translate_time  # Импортируем функцию перевода времени
    logstr = translate_time(time.ctime(time.time())) + ' >'  # Формируем строку лога с текущим временем
    logstr += ' ' + str(account_id)
    logstr += ' [' + command_name + ']'
    if acc_id != None:
        logstr += ' ' + acc_id
    if comment != '':
        logstr += ' | ' + comment
    import os
    data_path = os.path.join(_ba.env()['python_directory_user'],"chatHandle", "commandsLog" + os.sep)
    filename = data_path + 'commands' + ".log"
    if os.path.exists(filename):
        with open(filename, "a") as file:
            file.write('\n' + logstr)  # Записываем лог в файл
    else:
        with open(filename, "w") as file:
            file.write(logstr)  # Создаем новый файл и записываем лог

def show_pages(client_id, text_lines, type, page, long = False, inverse = False):
    from chatHandle.chat_functions import showmessage, _white_  # Импортируем функции отображения сообщений и цвета
    if type == 2:
        type = 3  # Изменяем тип на вывод только в чат

    if len(text_lines) == 0: return

    lines_on_page = lop = 12
    if long: lines_on_page = lop = 24

    pages = int((len(text_lines) - 1) / lop) + 1
    if page == 0:
        page = 1
    elif page > pages:
        page = pages

    _start = (page - 1) * lop
    _end = min(len(text_lines), page * lop)
    page_lines = text_lines[_start:_end]
    if inverse:
        page_lines.reverse()  # Реверсируем строки, если требуется вывод в обратном порядке
    for line in page_lines:
        showmessage(client_id, type, line, _white_)  # Выводим строки на экран
    showmessage(client_id, type, '============ страница ' + str(page) + ' из ' + str(pages) + ' ============', _white_)  # Выводим информацию о текущей странице и общем количестве страниц
