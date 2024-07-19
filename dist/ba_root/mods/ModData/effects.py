import _ba, ba
import os, json
import time

data_path = os.path.join(_ba.env()['python_directory_user'],"playersData" + os.sep)

import random

from typing import Any, Sequence, Optional, Union

from bastd.gameutils import SharedObjects


def load_effects():
    with open(data_path+'effects.json', 'r') as f:
        effects = json.load(f)
    for account_id in list(effects.keys()):
        if len(effects[account_id]) == 0 or len(effects[account_id]) == 1 and 'account name' in effects[account_id]:
            effects.pop(account_id)
    return effects

def save_effects(effects):
    with open(data_path+'effects.json', 'w') as f:
        json.dump(effects, f, indent=4, ensure_ascii=False)

def add_effect(account_id, account_name, name, attrs):
    effects = load_effects()
    if not account_id in effects: effects[account_id] = {'account name': []}

    #placing latest account names in the end
    if account_name in effects[account_id]['account name']:
        effects[account_id]['account name'].remove(account_name)
    effects[account_id]['account name'].append(account_name)
    effects[account_id][name] = attrs
    save_effects(effects)

def remove_effect(account_id, name):
    effects = load_effects()
    if account_id in effects and name in effects[account_id]:
        effects[account_id].pop(name)
        if len(effects[account_id]) == 0 or len(effects[account_id]) == 1 and 'account name' in effects[account_id]:
            effects.pop(account_id)
    save_effects(effects)
