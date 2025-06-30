import requests
import re
from urllib import parse
from bs4 import BeautifulSoup
from scrapper import Scrapper

class Mangafire(Scrapper):

    def __init__(self, provider, type):
        self.provider = provider
        self.type = type

    def get_title_list(self, domain, keyword, provider, type):
        payload={}
        headers = {}
        
        url = f"https://{domain}/filter?keyword={parse.quote(keyword)}"
        response = requests.request("GET", url, headers=headers, data=payload)

        # print(response.text)

        # Html_file= open("list.html","w")
        # Html_file.write(response.text)
        # Html_file.close()

        soup = BeautifulSoup(response.text, 'html.parser')

        link_list = []

        list_items = soup.find_all('div', class_='inner')
        if list_items:
            link_list = []

            id_counter = 1
            for link_tag in list_items:
                a_tag = link_tag.find('a', class_='poster')
                if not a_tag:
                    continue

                href = a_tag.get("href")
                img = a_tag.find('img')
                title = img.get('alt') if img else ''
                title = title.replace(":", "-")

                match = re.search(r'\.([a-zA-Z0-9]+)$', href)
                if match:
                    manga_id = match.group(1)

                    item = {
                        "id": id_counter,
                        "link": f"https://{domain}/ajax/read/{manga_id}/chapter/en",
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
        headers = {
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            "Accept": "application/json, text/javascript, */*; q=0.01"
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        # print(response.text)

        # Html_file= open("list.html","w")
        # Html_file.write(response.text)
        # Html_file.close()

        link_list = []

        html = response.json()['result']['html']
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            list_items = soup.select('li')
            # <li>
            #     <a href="/read/tower-dungeonn.909xm/en/chapter-18" data-number="18" data-id="4159084" title="">Chap 18: </a>
            # </li>

            list_items = list(reversed(list_items))

            idx = 1
            for link_tag in list_items:
                a_tag = link_tag.find('a')
                if a_tag:
                    href = a_tag.get("href")
                    sub_title = a_tag.get_text(strip=True)
                    sub_title = sub_title.replace(":", "-")

                    link_list.append({
                        "idx": str(idx),
                        "comic_name": title,
                        "sub_title": sub_title,
                        "link": a_tag.get("data-id")
                    })
                    idx += 1

        # print(link_list)

        return link_list

    def get_img_data(self, data_id, sub_title):

        payload={}
        headers = {
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            "Accept": "application/json, text/javascript, */*; q=0.01"
        }

        url = f"https://mangafire.to/ajax/read/chapter/{data_id}"

        # print(url)

        response = requests.request("GET", url, headers=headers, data=payload)

        # print(response.text)

        # Html_file= open("test1.html","w")
        # Html_file.write(response.text)
        # Html_file.close()

        img_list = []
        images = response.json()['result']['images']
        if images:
            # [
            #     [
            #         "https://static1.mfcdn1.xyz/12a3db61fa185b4ef2cf374f85fbf6448c60a95c58bdbbb2494d6fb2a43ed8da6202c01e40602de3fc31c758a44bea/h/p.jpg",
            #         1,
            #         0
            #     ],

            idx = 1
            for image in images:
                ext = 'jpg'

                img_list.append({
                    "src" : image[0],
                    "name" : f"{sub_title}_{idx:02}.{ext}"
                })
                idx += 1

        img_data = {
            "title" : sub_title,
            "img_list": img_list
        }

        # print(img_data)

        return img_data

        # download for this
        # GET https://static1.mfcdn1.xyz/10a3872af20d5d46ad92661bc6bce45bc26fff120ae1fce65c4160acb239cb803452db1d5b6028b7bc34d45ca912b7daa0d88800c06383e9c9ecf56c0720ab867d9444eb525bee/h/p.jpg HTTP/1.1
        # User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36
        # Accept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8
        # Referer: https://mangafire.to/
