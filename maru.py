import requests
from bs4 import BeautifulSoup
from scrapper import Scrapper

class Maru(Scrapper):

    def __init__(self, provider, type):
        self.provider = provider
        self.type = type

    def get_title_list(self, domain, keyword, provider, type):

        payload={}
        headers = {}

        url = f"https://{domain}/bbs/search.php?srows=10&gr_id=&sfl=wr_subject&stx={keyword}"
        response = requests.request("GET", url, headers=headers, data=payload)

        # print(response.text)

        # Html_file= open("list.html","w")
        # Html_file.write(response.text)
        # Html_file.close()

        soup = BeautifulSoup(response.text, 'html.parser')

        links = soup.find_all('div', {'class':'media'})

        link_list = []
        for link in links:
            title = link.find('a').text.replace('\n','').strip()
            href = link.find('a').attrs['href']
            id = ""
            for param in href.split('&'):
                if param.startswith("sca="):
                    id = param.replace("sca=", "")
            
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
        links = soup.find_all('td', {'class':'list-subject'})
        comic_name = soup.find('h1').text.replace('\n','').strip()

        link_list = []
        idx = 1
        links = list(reversed(links))

        for link in links:
            href = link.find('a').attrs['href']
            sub_title = link.find('a').text.replace('\n','').strip()
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

    def get_img_data(self, url):

        payload={}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        # print(response.text)

        # Html_file= open("test1.html","w")
        # Html_file.write(response.text)
        # Html_file.close()

        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.find('meta', {'name':'title'}).attrs['content']
        imgs = soup.find_all('img', {'class':'img-tag'})

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
                "name" : f"{title}_{idx:02}.{ext}"
            })
            idx = idx +1
        
        img_data = {
            "title" : title,
            "img_list": img_list
        }

        return img_data
