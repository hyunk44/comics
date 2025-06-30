import requests
import re
from urllib import parse
from bs4 import BeautifulSoup
from scrapper import Scrapper

class Xbato(Scrapper):

    def __init__(self, provider, type):
        self.provider = provider
        self.type = type

    def get_title_list(self, domain, keyword, provider, type):
        payload={}
        headers = {}
        
        url = f"https://{domain}/v3x-search?word={parse.quote(keyword)}"
        response = requests.request("GET", url, headers=headers, data=payload)

        # print(response.text)

        # Html_file= open("list.html","w")
        # Html_file.write(response.text)
        # Html_file.close()

        soup = BeautifulSoup(response.text, 'html.parser')

        link_list = []

        list_items = soup.find_all('a', class_='link-hover link-pri')
        if list_items:
            link_list = []

            id_counter = 1
            for link_tag in list_items:
                href = link_tag.get("href")
                title = link_tag.get_text(" ", strip=True)
                title = title.replace(":", "-")

                item = {
                    "id": id_counter,
                    "link": f"https://{domain}{href}",
                    "title": title,
                    "provider": provider,
                    "type": type
                }
                link_list.append(item)
                id_counter += 1

        # else:
        #     print("Required div not found!")

        return link_list

    def get_chapter_links(self, url, domain, title, id, type):

        payload={}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        # print(response.text)

        # Html_file= open("list.html","w")
        # Html_file.write(response.text)
        # Html_file.close()

        link_list = []

        soup = BeautifulSoup(response.text, 'html.parser')

        list_items = soup.find_all('a', class_=lambda c: c and all(cls in c.split() for cls in ['link-hover', 'link-primary', 'visited:text-accent']))
        if list_items:
            idx = 1
            for link_tag in list_items:
                if link_tag:
                    href = link_tag.get("href")
                    sub_title = link_tag.get_text(" ", strip=True)
                    sub_title = sub_title.replace(":", "-")

                    item = {
                        "idx": str(idx),
                        "comic_name": title,
                        "sub_title": sub_title,
                        "link": f"https://{domain}{href}",
                    }
                    link_list.append(item)
                    idx += 1

        else:
            print("Required div not found!")

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

        a_tag = soup.find('a', class_='link-primary link-hover')
        # 그 안에서 span.opacity-80의 텍스트만 추출
        # title = a_tag.find('span', class_='opacity-80').get_text(strip=True)

        # h3_tags = soup.find_all("h3")
        # for h3 in h3_tags:
        #     strong_tag = h3.find("strong")
        #     if strong_tag:
        #         title = strong_tag.get_text(strip=True)
        #         title = title.replace(":", "-")
    
        img_list = []
        targets = soup.find_all('astro-island', attrs={'component-url': lambda val: val and 'ImageList' in val})
        for tag in targets:
            props = tag.get('props', '')
            decoded_props = props.replace("&quot;", '"').replace("\\/", "/")
            urls = re.findall(r'https://[a-zA-Z0-9./_-]+\.(?:webp|jpg|jpeg|png)', decoded_props)

            idx = 1
            for src in urls:
                ext = 'jpg'

                img_list.append({
                    "src" : src,
                    "name" : f"{sub_title}_{idx:02}.{ext}"
                })
                idx += 1

        img_data = {
            "title" : sub_title,
            "img_list": img_list
        }

        return img_data
