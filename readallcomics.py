import requests
from urllib import parse
from bs4 import BeautifulSoup
from scrapper import Scrapper

class ReadAllComics(Scrapper):

    def __init__(self, provider, type):
        self.provider = provider
        self.type = type

    def get_title_list(self, domain, keyword, provider, type):
        payload={}
        headers = {}
        
        url = f"https://{domain}/?story={parse.quote(keyword)}&s=&type=comic"
        response = requests.request("GET", url, headers=headers, data=payload)

        # print(response.text)

        # Html_file= open("list.html","w")
        # Html_file.write(response.text)
        # Html_file.close()

        soup = BeautifulSoup(response.text, 'html.parser')

        link_list = []

        group_box = soup.find("div", class_="group-box list")
        if group_box:
            list_items = group_box.find_all("li")
            link_list = []

            id_counter = 1
            for li in list_items:
                link_tag = li.find("a")
                if link_tag:
                    href = link_tag.get("href")
                    title = link_tag.get_text(strip=True)
                    title = title.replace(":", "-")

                    item = {
                        "id": id_counter,
                        "link": href,
                        "title": title,
                        "provider": provider,
                        "type": type
                    }
                    link_list.append(item)
                    id_counter += 1

        else:
            print("Required div not found!")

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
        group_box = soup.find("div", class_="group-box list")
        if group_box:
            list_items = group_box.find_all("li")
            
            idx = 1
            # for idx, li in enumerate(list_items, start=1):
            for li in reversed(list_items):
                link_tag = li.find("a")
                if link_tag:
                    href = link_tag.get("href")
                    sub_title = link_tag.get("title")
                    sub_title = sub_title.replace(":", "-")

                    item = {
                        "idx": str(idx),
                        "comic_name": title,
                        "sub_title": sub_title,
                        "link": href
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

        title = ""
        h3_tags = soup.find_all("h3")
        for h3 in h3_tags:
            strong_tag = h3.find("strong")
            if strong_tag:
                title = strong_tag.get_text(strip=True)
                title = title.replace(":", "-")
    
        img_list = []
        img_tags = soup.find_all("img")
        idx = 1
        for img in img_tags:
            src = img.get("src")
            if src and "logo" not in src.lower():

                # https://2.bp.blogspot.com/cd9z4dw8HE9LvuIuZU6jWSp6QEEIslB2zhRdYQHNHoCOZzuTyJAeE_oae8CDkeBHzbg-7nd45Z_RZSVteOeu_bLdAuFYxWfVJUTPvEI4LXpMK70RtfzjnR4c-q0s11Uo6deKPE1EqQ=s0
                # 처럼 확장자 없는 경우가 있다
                # ext = src.split(".")[-1]
                ext = 'jpg'

                img_list.append({
                    "src" : src,
                    "name" : f"{title}_{idx:02}.{ext}"
                })
                idx += 1

        img_data = {
            "title" : title,
            "img_list": img_list
        }

        return img_data
