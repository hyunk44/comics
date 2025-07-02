import requests
from urllib import parse
from bs4 import BeautifulSoup
from scrapper import Scrapper

class Jmana(Scrapper):

    def __init__(self, provider, type):
        self.provider = provider
        self.type = type

    def get_title_list(self, domain, keyword, provider, type):
        payload={}
        headers = {}

        url = f"https://{domain}/comic_list_search?keyword={keyword}"
        response = requests.request("GET", url, headers=headers, data=payload)

        # print(response.text)

        # Html_file= open("list.html","w")
        # Html_file.write(response.text)
        # Html_file.close()

        soup = BeautifulSoup(response.text, 'html.parser')

        # https://kr21.jmana.one/comic_list_title?bookname=%EC%97%89%ED%84%B0%EB%A6%AC+%EB%8A%A5%EB%A0%A5+%EC%97%AC%EA%B3%A0%EC%83%9D+%EB%82%98%EB%A3%A8%EB%AA%A8%EA%B0%80%EC%99%80+%EC%96%91
        links = soup.find_all('a', {'class':'tit'})

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
        links = soup.find('div', {'class':['lst-wrap','stl5']}).find_all('a', {'class':'tit'})

        link_list = []
        idx = 1
        links = list(reversed(links))

        for link in links:
            href = link.attrs['href']
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

        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.find('div', {'class':['tit-wrap', 'stl1', 'lg']}).find('h2', {'class':'tit'}).text
        imgs = soup.find_all('img', {'class':'comicdetail'})

        img_list = []

        idx = 1
        for img in imgs:
            # print(img)
            if img.has_attr('data-src') and img.attrs['data-src'].startswith("http"):
                src = img.attrs['data-src']
            elif img.has_attr('src') and img.attrs['src'].startswith("http"):
                src = img.attrs['src']
            else:
                continue
            
            if 'loading' in src or 'notice' in src:
                continue

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
