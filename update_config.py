import requests
from bs4 import BeautifulSoup
import http.client
from urllib import parse
from functions import *
from toki import *


# def get_domain_list():

#     payload={}
#     headers = {}

#     response = requests.request("GET", "https://jusoshow.me/", headers=headers, data=payload)

#     # print(response.text)

#     # Html_file= open("list.html","w")
#     # Html_file.write(response.text)
#     # Html_file.close()

#     soup = BeautifulSoup(response.text, 'html.parser')

#     links = soup.find('ul', {'class':'list'}).find_all('li')

#     link_list = []
#     for link in links:
#         title = link.find('a').attrs['title']
#         href = link.find('a').attrs['href'].split('//')[1]
        
#         link_list.append({
#             "domain": href,
#             "title": title
#         })
    
#     return link_list

def check_domain(schema, domain, provider):
    try:
        
        if provider == 'toki':
            scrapper = Toki(provider)
            response = scrapper.do_connect_toki('', domain, '')
            print(response)
        
        else:
            payload={}
            headers = {}

            print(domain)
            response = requests.request("GET", f"{schema}{domain}", headers=headers, data=payload)
            print(response.status_code)

            return response.status_code

    except requests.exceptions.ConnectionError as ce:
        print(f'ConnectionError {ce}')
        return 54

    except ConnectionResetError as cre:
        print(f'ConnectionResetError {cre}')
        return 54

    except Exception as e:
        print(f'그 외 {e}')
        return 500

def get_refused_domains(providers):
    refusedDomains = []

    for provider in providers:
        if not provider['enable']:
            continue

        schema = provider['schema']
        domainFormat = provider['domainFormat']
        domainCount = provider['domainCount']
        domain = domainFormat.replace('$$$', str(domainCount))

        status_code = check_domain(schema, domain, provider)

        if status_code == 54:
            refusedDomains.append(provider)

    return refusedDomains

def get_new_domain(refused_domain, check_new_domain_try_count):
    name = refused_domain['name']
    provider = refused_domain['provider']
    schema = refused_domain['schema']
    domainFormat = refused_domain['domainFormat']
    domainCount = refused_domain['domainCount']

    for idx in range(check_new_domain_try_count):
        this_domain_count = domainCount + (idx + 1)
        domain = domainFormat.replace('$$$', str(this_domain_count))

        status_code = check_domain(schema, domain, provider)

        if status_code == 200:
            return {
                    "name": name,
                    "domain": domain,
                    "domainCount": this_domain_count
                }

        elif status_code == 54:
            continue

        elif status_code == 500:
            break
    
    return
    

def update_domain(providers, domain_list):
    map_by_name = {}
    for data in domain_list:
        map_by_name[data['name']] = data

    new_providers = []
    for provider in providers:
        new_domain = map_by_name.get(provider['name'])

        if new_domain:
            provider['domain'] = new_domain['domain']
            provider['domainCount'] = new_domain['domainCount']

        new_providers.append(provider)

    new_providers_data = {
        "providers" : new_providers
    }
    store_file(new_providers_data, "config.json")


config = read_file('config.json')
providers = config['providers']
check_new_domain_try_count = 10

refused_domains = get_refused_domains(providers)

if refused_domains:
    update_providers = []
    for refused_domain in refused_domains:
        new_domain = get_new_domain(refused_domain, check_new_domain_try_count)
        if new_domain:
            update_providers.append(new_domain)
    
    if update_providers:
        update_domain(providers, update_providers)


# check_domain('https://', 'manatoki283.net', 'toki')