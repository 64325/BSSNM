from ba._generated.enums import TimeType
import _ba
import os, json

data_path = os.path.join(_ba.env()['python_directory_user'],"serverData" + os.sep)

def load_server_data():
    with open(data_path+'server_data.json', 'r') as f:
        server_data = json.load(f)
    with open(data_path+'packages.json', 'r') as f:
        server_data['packages'] = json.load(f)
    return server_data

def save_server_data(server_data):
    server_data = server_data.copy()
    if 'packages' in server_data:
        with open(data_path+'packages.json', 'w') as f:
            json.dump(server_data['packages'], f, indent=4, ensure_ascii=False)
        server_data.pop('packages')
    with open(data_path+'server_data.json', 'w') as f:
        json.dump(server_data, f, indent=4, ensure_ascii=False)

def save_packages(packages):
    with open(data_path+'packages.json', 'w') as f:
        json.dump(packages, f, indent=4, ensure_ascii=False)