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

                item = {
                    "id": id_counter,
                    "link": f"https://{domain}{href}",  # TODO: 909xm
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

        # TODO : 909xm
        # GET https://mangafire.to/ajax/read/909xm/chapter/en HTTP/1.1
        # X-Requested-With: XMLHttpRequest
        # User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36
        # Accept: application/json, text/javascript, */*; q=0.01

        # {"status":200,"result":{"html":"<div class=\"head\"> <form autocomplete=\"off\" onsubmit=\"return false\"> <div class=\"form-group\"> <i class=\"fa-regular fa-magnifying-glass\"><\/i> <input type=\"text\" class=\"form-control\" placeholder=\"Find number...\"> <\/div> <\/form> <button class=\"close-primary btn btn-secondary1\" id=\"number-close\"> <i class=\"fa-solid fa-chevron-right\"><\/i> <\/button> <\/div> <ul> <li><a href=\"\/read\/tower-dungeonn.909xm\/en\/chapter-18\" data-number=\"18\" data-id=\"4159084\" title=\"\">Chap 18: <\/a><\/li> <li><a href=\"\/read\/tower-dungeonn.909xm\/en\/chapter-17\" data-number=\"17\" data-id=\"4106540\" title=\"\">Chap 17: <\/a><\/li> <li><a href=\"\/read\/tower-dungeonn.909xm\/en\/chapter-16\" data-number=\"16\" data-id=\"4051795\" title=\"\">Chap 16: <\/a><\/li> <li><a href=\"\/read\/tower-dungeonn.909xm\/en\/chapter-15\" data-number=\"15\" data-id=\"3954364\" title=\"\">Chap 15: <\/a><\/li> <li><a href=\"\/read\/tower-dungeonn.909xm\/en\/chapter-14\" data-number=\"14\" data-id=\"3893455\" title=\"\">Chap 14: <\/a><\/li> <li><a href=\"\/read\/tower-dungeonn.909xm\/en\/chapter-13\" data-number=\"13\" data-id=\"3847277\" title=\"\">Chap 13: <\/a><\/li> <li><a href=\"\/read\/tower-dungeonn.909xm\/en\/chapter-12\" data-number=\"12\" data-id=\"3803026\" title=\"\">Chap 12: <\/a><\/li> <li><a href=\"\/read\/tower-dungeonn.909xm\/en\/chapter-11\" data-number=\"11\" data-id=\"3754992\" title=\"\">Chap 11: <\/a><\/li> <li><a href=\"\/read\/tower-dungeonn.909xm\/en\/chapter-10\" data-number=\"10\" data-id=\"3676688\" title=\"\">Chap 10: <\/a><\/li> <li><a href=\"\/read\/tower-dungeonn.909xm\/en\/chapter-9\" data-number=\"9\" data-id=\"3630169\" title=\"\">Chap 9: <\/a><\/li> <li><a href=\"\/read\/tower-dungeonn.909xm\/en\/chapter-8\" data-number=\"8\" data-id=\"3557898\" title=\"\">Chap 8: <\/a><\/li> <li><a href=\"\/read\/tower-dungeonn.909xm\/en\/chapter-7\" data-number=\"7\" data-id=\"3468890\" title=\"Yuva, Renowned Thrower of Salt\">Chap 7: Yuva, Renowned Thrower of Salt<\/a><\/li> <li><a href=\"\/read\/tower-dungeonn.909xm\/en\/chapter-6\" data-number=\"6\" data-id=\"3029530\" title=\"The Royal Family&#039;s Secret Treasure\">Chap 6: The Royal Family&#039;s Secret Treasure<\/a><\/li> <li><a href=\"\/read\/tower-dungeonn.909xm\/en\/chapter-5\" data-number=\"5\" data-id=\"2460791\" title=\"Chapter 5: Marquess Karash, Draco-Metamorph\">Chap 5: Chapter 5: Marquess Karash, Draco-Metamorph<\/a><\/li> <li><a href=\"\/read\/tower-dungeonn.909xm\/en\/chapter-4\" data-number=\"4\" data-id=\"2429559\" title=\"An Alluring Scent\">Chap 4: An Alluring Scent<\/a><\/li> <li><a href=\"\/read\/tower-dungeonn.909xm\/en\/chapter-3\" data-number=\"3\" data-id=\"2419347\" title=\"Squad Leader Eliquo&#039;s Woes\">Chap 3: Squad Leader Eliquo&#039;s Woes<\/a><\/li> <li><a href=\"\/read\/tower-dungeonn.909xm\/en\/chapter-2\" data-number=\"2\" data-id=\"2419344\" title=\"The Half-A-Dragon and the Fire Mage\">Chap 2: The Half-A-Dragon and the Fire Mage<\/a><\/li> <li><a href=\"\/read\/tower-dungeonn.909xm\/en\/chapter-1\" data-number=\"1\" data-id=\"2419342\" title=\"Yuva, Renowed Thrower of Feed\">Chap 1: Yuva, Renowed Thrower of Feed<\/a><\/li> <\/ul>","title_format":"Tower Dungeon TYPE_NUM - Read Manga Online"}}


        response = requests.request("GET", url, headers=headers, data=payload)

        # print(response.text)

        # Html_file= open("list.html","w")
        # Html_file.write(response.text)
        # Html_file.close()

        link_list = []

        soup = BeautifulSoup(response.text, 'html.parser')

        list_items = soup.select('ul.scroll-sm li.item')
        if list_items:
            idx = 1
            for link_tag in list_items:
                a_tag = link_tag.find('a')
                if a_tag:
                    href = a_tag.get("href")
                    spans = a_tag.find_all('span')
                    sub_title = spans[0].get_text(strip=True) if len(spans) > 0 else ''
                    sub_title = sub_title.replace(":", "-")

                    item = {
                        "idx": str(idx),
                        "comic_name": title,
                        "sub_title": sub_title,
                        "link": f"https://{domain}{href}",  # href : /read/tower-dungeonn.909xm/en/chapter-18
                    }
                    link_list.append(item)
                    idx += 1

        else:
            print("Required div not found!")

        return link_list

    def get_img_data(self, url):

        payload={}
        headers = {}

        # TODO : 4159084
        # GET https://mangafire.to/ajax/read/chapter/4159084 HTTP/1.1
        # X-Requested-With: XMLHttpRequest
        # User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36
        # Accept: application/json, text/javascript, */*; q=0.01

        # {"status":200,"result":{"images":[["https:\/\/static1.mfcdn1.xyz\/12a3db61fa185b4ef2cf374f85fbf6448c60a95c58bdbbb2494d6fb2a43ed8da6202c01e40602de3fc31c758a44bea\/h\/p.jpg",1,0],["https:\/\/static1.mfcdn1.xyz\/12a3db61fa185b4ef2cf374f85fbf6448c60a95c58bdbbb2494d6fb2a43dd8da6202c01e40602de3fc31c758a44bea\/h\/p.jpg",1,0],["https:\/\/static1.mfcdn1.xyz\/10a3872af20d5d46ad92661bc6bce45bc26fff120ae1fce65c4160acb239cb803452db1d5b6028b7bc34d45ca912b7daa0d88800c06383e9c9ecf56c0720ab867d9444eb525bee\/h\/p.jpg",1,0],["https:\/\/static1.mfcdn1.xyz\/12a3db61fa185b4ef2cf374f85fbf6448c60a95c58bdbbb2494d6fb2a43bd8da6202c01e40602de3fc31c758a44bea\/h\/p.jpg",1,0],["https:\/\/static1.mfcdn1.xyz\/10a3872af20d5d46ad92661bc6bce45bc26fff120ae1fce65c4160acb239cb803452db1d5b6028b7bc34d45ca912b7daa0d88800c06383e9c9ecf56c0720ab867d9442eb525bee\/h\/p.jpg",1,0],["https:\/\/static1.mfcdn1.xyz\/10a3872af20d5d46ad92661bc6bce45bc26fff120ae1fce65c4160acb239cb803452db1d5b6028b7bc34d45ca912b7daa0d88800c06383e9c9ecf56c0720ab867d9441eb525bee\/h\/p.jpg",1,0],["https:\/\/static1.mfcdn1.xyz\/12a3db61fa185b4ef2cf374f85fbf6448c60a95c58bdbbb2494d6fb2a438d8da6202c01e40602de3fc31c758a44bea\/h\/p.jpg",1,0],["https:\/\/static1.mfcdn1.xyz\/12a3db61fa185b4ef2cf374f85fbf6448c60a95c58bdbbb2494d6fb2a437d8da6202c01e40602de3fc31c758a44bea\/h\/p.jpg",1,0],["https:\/\/static1.mfcdn1.xyz\/10a3872af20d5d46ad92661bc6bce45bc26fff120ae1fce65c4160acb239cb803452db1d5b6028b7bc34d45ca912b7daa0d88800c06383e9c9ecf56c0720ab867d944eeb525bee\/h\/p.jpg",1,0],["https:\/\/static1.mfcdn1.xyz\/10a3872af20d5d46ad92661bc6bce45bc26fff120ae1fce65c4160acb239cb803452db1d5b6028b7bc34d45ca912b7daa0d88800c06383e9c9ecf56c0720ab867d9547eb525bee\/h\/p.jpg",1,0],["https:\/\/static1.mfcdn1.xyz\/12a3db61fa185b4ef2cf374f85fbf6448c60a95c58bdbbb2494d6fb2a53ed8da6202c01e40602de3fc31c758a44bea\/h\/p.jpg",1,0],["https:\/\/static1.mfcdn1.xyz\/10a3872af20d5d46ad92661bc6bce45bc26fff120ae1fce65c4160acb239cb803452db1d5b6028b7bc34d45ca912b7daa0d88800c06383e9c9ecf56c0720ab867d9545eb525bee\/h\/p.jpg",1,0],["https:\/\/static1.mfcdn1.xyz\/12a3db61fa185b4ef2cf374f85fbf6448c60a95c58bdbbb2494d6fb2a53cd8da6202c01e40602de3fc31c758a44bea\/h\/p.jpg",1,0],["https:\/\/static1.mfcdn1.xyz\/12a3db61fa185b4ef2cf374f85fbf6448c60a95c58bdbbb2494d6fb2a53bd8da6202c01e40602de3fc31c758a44bea\/h\/p.jpg",1,0],["https:\/\/static1.mfcdn1.xyz\/10a3872af20d5d46ad92661bc6bce45bc26fff120ae1fce65c4160acb239cb803452db1d5b6028b7bc34d45ca912b7daa0d88800c06383e9c9ecf56c0720ab867d9542eb525bee\/h\/p.jpg",1,0],["https:\/\/static1.mfcdn1.xyz\/12a3db61fa185b4ef2cf374f85fbf6448c60a95c58bdbbb2494d6fb2a539d8da6202c01e40602de3fc31c758a44bea\/h\/p.jpg",1,0],["https:\/\/static1.mfcdn1.xyz\/12a3db61fa185b4ef2cf374f85fbf6448c60a95c58bdbbb2494d6fb2a538d8da6202c01e40602de3fc31c758a44bea\/h\/p.jpg",1,0],["https:\/\/static1.mfcdn1.xyz\/10a3872af20d5d46ad92661bc6bce45bc26fff120ae1fce65c4160acb239cb803452db1d5b6028b7bc34d45ca912b7daa0d88800c06383e9c9ecf56c0720ab867d954feb525bee\/h\/p.jpg",1,0],["https:\/\/static1.mfcdn1.xyz\/12a3db61fa185b4ef2cf374f85fbf6448c60a95c58bdbbb2494d6fb2a536d8da6202c01e40602de3fc31c758a44bea\/h\/p.jpg",1,0],["https:\/\/static1.mfcdn1.xyz\/10a3872af20d5d46ad92661bc6bce45bc26fff120ae1fce65c4160acb239cb803452db1d5b6028b7bc34d45ca912b7daa0d88800c06383e9c9ecf56c0720ab867d9647eb525bee\/h\/p.jpg",1,0],["https:\/\/static1.mfcdn1.xyz\/10a3872af20d5d46ad92661bc6bce45bc26fff120ae1fce65c4160acb239cb803452db1d5b6028b7bc34d45ca912b7daa0d88800c06383e9c9ecf56c0720ab867d9646eb525bee\/h\/p.jpg",1,0],["https:\/\/static1.mfcdn1.xyz\/12a3db61fa185b4ef2cf374f85fbf6448c60a95c58bdbbb2494d6fb2a63dd8da6202c01e40602de3fc31c758a44bea\/h\/p.jpg",1,0],["https:\/\/static1.mfcdn1.xyz\/12a3db61fa185b4ef2cf374f85fbf6448c60a95c58bdbbb2494d6fb2a63cd8da6202c01e40602de3fc31c758a44bea\/h\/p.jpg",1,0],["https:\/\/static1.mfcdn1.xyz\/10a3872af20d5d46ad92661bc6bce45bc26fff120ae1fce65c4160acb239cb803452db1d5b6028b7bc34d45ca912b7daa0d88800c06383e9c9ecf56c0720ab867d9643eb525bee\/h\/p.jpg",1,0],["https:\/\/static1.mfcdn1.xyz\/10a3872af20d5d46ad92661bc6bce45bc26fff120ae1fce65c4160acb239cb803452db1d5b6028b7bc34d45ca912b7daa0d88800c06383e9c9ecf56c0720ab867d9642eb525bee\/h\/p.jpg",1,0],["https:\/\/static1.mfcdn1.xyz\/12a3db61fa185b4ef2cf374f85fbf6448c60a95c58bdbbb2494d6fb2a639d8da6202c01e40602de3fc31c758a44bea\/h\/p.jpg",1,0],["https:\/\/static1.mfcdn1.xyz\/10a3872af20d5d46ad92661bc6bce45bc26fff120ae1fce65c4160acb239cb803452db1d5b6028b7bc34d45ca912b7daa0d88800c06383e9c9ecf56c0720ab867d9640eb525bee\/h\/p.jpg",1,0],["https:\/\/static1.mfcdn1.xyz\/12a3db61fa185b4ef2cf374f85fbf6448c60a95c58bdbbb2494d6fb2a637d8da6202c01e40602de3fc31c758a44bea\/h\/p.jpg",1,0],["https:\/\/static1.mfcdn1.xyz\/12a3db61fa185b4ef2cf374f85fbf6448c60a95c58bdbbb2494d6fb2a636d8da6202c01e40602de3fc31c758a44bea\/h\/p.jpg",1,0],["https:\/\/static1.mfcdn1.xyz\/10a3872af20d5d46ad92661bc6bce45bc26fff120ae1fce65c4160acb239cb803452db1d5b6028b7bc34d45ca912b7daa0d88800c06383e9c9ecf56c0720ab867d9747eb525bee\/h\/p.jpg",1,0]]}}

        response = requests.request("GET", url, headers=headers, data=payload)

        # print(response.text)

        # Html_file= open("test1.html","w")
        # Html_file.write(response.text)
        # Html_file.close()

        soup = BeautifulSoup(response.text, 'html.parser')

        a_tag = soup.find('a', class_='link-primary link-hover')
        # 그 안에서 span.opacity-80의 텍스트만 추출
        title = a_tag.find('span', class_='opacity-80').get_text(strip=True)

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
                    "name" : f"{title}_{idx:02}.{ext}"
                })
                idx += 1

        img_data = {
            "title" : title,
            "img_list": img_list
        }

        return img_data

        # download for this
        # GET https://static1.mfcdn1.xyz/10a3872af20d5d46ad92661bc6bce45bc26fff120ae1fce65c4160acb239cb803452db1d5b6028b7bc34d45ca912b7daa0d88800c06383e9c9ecf56c0720ab867d9444eb525bee/h/p.jpg HTTP/1.1
        # User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36
        # Accept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8
        # Referer: https://mangafire.to/
