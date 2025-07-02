import requests
from urllib import parse
from bs4 import BeautifulSoup
from scrapper import Scrapper

class Toonsarang(Scrapper):

    def __init__(self, provider, type):
        self.provider = provider
        self.type = type

    def get_title_list(self, domain, keyword, provider, type):
        payload={}
        headers = {}

        url = f"https://{domain}/bbs/search_webtoon.php?stx={parse.quote(keyword)}"
        response = requests.request("GET", url, headers=headers, data=payload)

        # print(response.text)

        # Html_file= open("list.html","w")
        # Html_file.write(response.text)
        # Html_file.close()

        soup = BeautifulSoup(response.text, 'html.parser')

        links = soup.find_all('div', {'class':'section-item-title'})

        link_list = []
        for link in links:
            title = link.find('a').text.replace('\n','').strip()
            href = link.find('a').attrs['href']
            id = ""
            
            link_list.append({
                "id": id,
                "link": href,
                "title": title,
                'provider' : provider,
                'type' : type,
            })
        
        return link_list

    def get_chapter_links(self, url, domain, title, id, type):

        payload={}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        # print(response.text)

        # Html_file= open("list.html","w")
        # Html_file.write(response.text)
        # Html_file.close()

        soup = BeautifulSoup(response.text, 'html.parser')

        host = url.split("//")[-1].split("/")[0]
        host = url.split("//")[0] + "//" + host
        links = soup.find('div', {'class':'contents-list'}).find_all('li')
        comic_name = soup.find("meta", {'name':'title'})["content"]

        link_list = []
        idx = 1
        links = list(reversed(links))

        for link in links:
            episode_off = link.find('span', {'class', 's_episode_off'}).text.strip()

            if episode_off == "0":
                continue

            href = link.find('a').attrs['href']
            sub_title = link.find('a').find('div', {'class':'content-title'}).text.replace('\n','').replace('\r','').strip()
            # link_list.append(host + href)
            # print(host + href)

            item = {
                "idx": str(idx),
                "comic_name": comic_name,
                "sub_title": sub_title,
                "link": (host + href)
            }
            link_list.append(item)
            idx += 1
        
        return link_list


    def get_img_data(self, url, sub_title):

        payload={}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        # print(response.text)

        # Html_file= open("test1.html","w")
        # Html_file.write(response.text)
        # Html_file.close()

        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.find('meta', {'name':'title'}).attrs['content']
        imgs = soup.find('div', {'id':'bo_v_con'}).find_all('img')

        img_list = []

        idx = 1
        for img in imgs:
            src = img.attrs['src']
            if not src.startswith("http"):
                host = url.split("//")[-1].split("/")[0]
                host = url.split("//")[0] + "//" + host
                src = host + src
            ext = src.split(".")[-1]
            img_list.append({
                "src" : src,
                "name" : f"{title}_{idx:03}.{ext}"
            })
            idx = idx +1
        
        img_data = {
            "title" : title,
            "img_list": img_list
        }

        return img_data
