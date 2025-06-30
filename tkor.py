import requests
import re
import base64
from urllib import parse
from bs4 import BeautifulSoup
from scrapper import Scrapper

class Tkor(Scrapper):

    def __init__(self, provider, type):
        self.provider = provider
        self.type = type

    def get_title_list(self, domain, keyword, provider, type):
        payload={}
        headers = {}

        keyword = keyword.replace(" ", "")

        url = f"https://{domain}/bbs/search.php?sfl=wr_subject%7C%7Cwr_content&stx={parse.quote(keyword)}"
        response = requests.request("GET", url, headers=headers, data=payload)

        # print(response.text)

        # Html_file= open("list.html","w")
        # Html_file.write(response.text)
        # Html_file.close()

        soup = BeautifulSoup(response.text, 'html.parser')

        links = soup.find_all('a', {'id':'title'})

        id = 0
        link_list = []
        for link in links:
            title = link.text.replace('\n','').strip()
            href = link.attrs['href']
            
            link_list.append({
                "id": id,
                "link": f'https://{domain}/{href}',
                "title": title,
                'provider' : provider,
                'type' : type,
            })

            id = id +1
        
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
        links = soup.find_all('td', {'class':'content__title'})

        link_list = []
        idx = 1
        links = list(reversed(links))

        for link in links:
            href = link.attrs['data-role']
            sub_title = link.text.replace('\n','').strip()

            item = {
                "idx": str(idx),
                "comic_name": title,
                "sub_title": sub_title,
                "link": f'https://{domain}/{href}'
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

        html = response.text
        match = re.search(r"var\s+toon_img\s*=\s*'([^']+)'", html)
        decoded_html = ''
        if match:
            base64_data = match.group(1)
            decoded_html = base64.b64decode(base64_data).decode("utf-8")
        else:
            print("toon_img base64 문자열을 찾을 수 없습니다.")
            return {}

        soup = BeautifulSoup(decoded_html, 'html.parser')

        imgs = soup.find_all('img')

        img_list = []

        idx = 1
        for img in imgs:
            src = img.attrs['src']
            ext = src.split(".")[-1]
            img_list.append({
                "src" : src,
                "name" : f"{sub_title}_{idx:02}.{ext}"
            })
            idx = idx +1
        
        img_data = {
            "title" : sub_title,
            "img_list": img_list
        }

        return img_data
