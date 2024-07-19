import _ba, os, json
import time

data_path = os.path.join(_ba.env()['python_directory_user'],"serverData" + os.sep)

def load_server_roles():
    with open(data_path+'server_roles.json', 'r') as f:
        server_roles_list = json.load(f)
    return server_roles_list