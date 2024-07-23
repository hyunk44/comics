import requests
import json
import pathlib

def send_message_to_slack(text, send_url):
    payload = { "text" : text }
    requests.post(send_url, json=payload)

def store_file(results, filename):
    p = pathlib.Path(__file__).with_name(filename)
    with p.open('w') as json_file:
        json.dump(results, json_file, indent=4)

def read_file(filename):
    try:
        p = pathlib.Path(__file__).with_name(filename)
        with p.open('r') as f:
            return json.load(f)
    except Exception as e:
        print(e)
        return

def filter_provider_types(provider_types):
    filtered_provider_types = []
    for provider_type in provider_types:
        if provider_type['enable']:
            filtered_provider_types.append(provider_type)
    
    return filtered_provider_types

def get_map_by_provider_type(config):
    providers = config['providers']
    map_by_provider_type = {}
    for provider in providers:
        map_by_provider_type[f"{provider['provider']}{provider['type']}"] = provider
    
    return map_by_provider_type

def get_domain(provider, type):
    config = read_file('config.json')
    map_by_provider_type = get_map_by_provider_type(config)
    return map_by_provider_type[f'{provider}{type}']['domain']    

