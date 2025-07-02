import requests
from urllib import parse
from scrapper import Scrapper

class Cook(Scrapper):

    def __init__(self, provider, type):
        self.provider = provider
        self.type = type

    def get_title_list(self, domain, keyword, provider, type):
        payload={}
        headers = {"Accept": "application/json, text/plain, */*"}
        url = f"http://{domain}/api/search?key={parse.quote(keyword)}"
        response = requests.request("GET", url, headers=headers, data=payload)

        links = []
        data = response.json()['data']
        if data:
            links = data['list']

        link_list = []
        for link in links:

            id = link['id']
            link_list.append({
                "id": id,
                # http://www.cookmana11.com/api/episode/list/34141?page=1&order=1
                "link": f"http://{domain}/api/episode/list/{id}?order=1",
                "title": link['title'],
                'provider' : provider,
                'type' : type,
            })
        
        return link_list

    def get_json_result(self, url, headers, payload):
        response = requests.request("GET", url, headers=headers, data=payload)
        return response.json()

    def get_chapter_links(self, url, domain, title, id, type):

        page = 1
        payload={}
        headers = {"Accept": "application/json, text/plain, */*"}
        result = self.get_json_result(f'{url}&page={page}', headers, payload)

        if result['code'] != 200 :
            return []

        links = result['data']

        current_page = result['current_page']
        last_page = result['last_page']

        while current_page < last_page:
            next_result = self.get_json_result(f'{url}&page={current_page + 1}', headers, payload)

            if next_result['code'] != 200 :
                break

            links.extend(next_result['data'])
            current_page = next_result['current_page']
            last_page = next_result['last_page']


        # print(f'current_page {current_page}')
        # print(f'links {links}')

        link_list = []
        idx = 1

        for link in links:
            item = {
                "idx": str(idx),
                "comic_name": title,
                "sub_title": link['title'],
                # http://www.cookmana11.com/api/detail/1713531
                "link": f"http://{domain}/api/detail/{link['id']}"
            }
            link_list.append(item)
            idx += 1
        
        return link_list

    def get_img_data(self, url, sub_title):

        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        data = response.json()['data']

        # print(f'data {data}')

        title = data['title']
        if not title:
            title = data['parentTitle']
        imgs = data['urls'].split(',')
        folder = data['folder']
        folder2 = data['folder2']
        # folder3 = data['folder3']
        parentId = data['parentId']
        id = url.split('/')[-1]

        # http://www.pl3040.com//kr/07/34141/1713531/BaQFvVf0SA3I.jpg
        # url_prefix = f'http://www.pl3040.com//kr{folder3}/'

        # print(f'title {title}')
        # print(f'imgs {imgs}')

        img_list = []

        idx = 1
        for img in imgs:
            # src = f'{url_prefix}{img}'
            src = self.make_img_url(folder, img, folder2, parentId, id)

            ext = img.split(".")[-1]
            img_list.append({
                "src" : src,
                "name" : f"{title}_{idx:03}.{ext}"
            })
            idx = idx +1
        
        img_data = {
            "title" : title,
            "img_list": img_list
        }

        # print(img_data)

        return img_data

    
    def make_img_url(self, folder, url, folder2, parentId, id):
        dnsSrc = "http://www.11angle.net/"
        dnsSrc2 = "https://www.pl3040.com/"
        # dnsSrc2 = "http://www.pl4050.com/"

        ret = ''
        if folder:
            ret = f'{dnsSrc}/image_pst-123/{folder}/{parentId}/{url}'
        else:
            ret = f'{dnsSrc}/toon_pst-123/{url}'

        if folder2:
            myUrl = url.split("/")
            url  = myUrl[len(myUrl)-1]

            myFol = folder2.split("/")
            folder2   = myFol[0]
            ret = f'{dnsSrc2}/kr/{folder2}/{parentId}/{id}/{url}'

        # print(ret)

        return ret