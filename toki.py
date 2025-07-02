import io
import cloudscraper
import time
# import js2py
from py_mini_racer import py_mini_racer
import http.client
from urllib import parse
from bs4 import BeautifulSoup
from scrapper import Scrapper

class Toki(Scrapper):

    def __init__(self, provider, type):
        self.provider = provider
        self.type = type
    
    def get_title_list(self, domain, keyword, provider, type):
        result  = self.do_connect_toki('', domain, f"/{type}?stx=" + parse.quote(keyword))
    
        soup = BeautifulSoup(result, 'html.parser')

        links = soup.find_all('div', {'class':'img-item'})

        link_list = []
        for link in links:
            id = link.find('div').attrs['rel']
            href = link.find('a').attrs['href']
            title = link.find('span').text
            link_list.append({
                "id": id,
                "link": href,
                "title": title,
                'provider' : provider,
                'type' : type,
            })
        
        return link_list

    def get_chapter_links(self, url, domain, title, id, type):
        result  = self.do_connect_toki('', domain, f'/{type}/{id}')

        # print(domain)
        # print(f'/{type}/{id}')
        # print(result)

        soup = BeautifulSoup(result, 'html.parser')

        list_body = soup.find('ul', {'class': 'list-body'})
        links = list_body.find_all('div', {'class': 'wr-subject'})
        comic_name = soup.find('span', {'class': 'page-desc'}).text.replace('\n','').strip()

        link_list = []
        idx = 1
        links = list(reversed(links))


        # start = False
        for link in links:
            href = link.find('a').attrs['href']
            
            [tag.extract() for tag in link.find('a').find_all('span')]
            title = link.find('a').text.replace('\n','').strip()

            # 임시처리
            # if "136화" in title:
            #     start = True
            # if not start:
            #     continue

            date = link.find('div', {'class':'item-details'}).find('span').text.replace('\n','').strip()
            # TODO : 날짜 기준처리 (하지만 등록일이 제멋대로임)
            # release_date = dt.strptime(date, "%Y.%m.%d")
            # condition_date = dt.strptime("2018.12.01", "%Y.%m.%d")
            # if release_date < condition_date:
            #     continue

            item = {
                "idx": str(idx),
                "comic_name": comic_name,
                "sub_title": title,
                "link": href,
                "date": date
            }
            link_list.append(item)
            idx += 1
            # link_list.append(href)
        
        return link_list

    def get_img_data(self, url, sub_title):

        # https://manatoki141.net/comic/5822817?spage=1
        result  = self.do_connect_toki(url, '', '')

        soup = BeautifulSoup(result, 'html.parser')

        title = soup.find('meta', {'name':'subject'}).attrs['content']
        divs = soup.find_all('div', {'class':'view-padding'})

        script_val = ""
        for div in divs:
            script_node = div.find('script', {'language':'Javascript'})
            if script_node:
                script_val = script_node.string
                break
        
        html_data = ""
        s = io.StringIO(script_val)
        for line in s:
            if line.startswith("var html_data='';") or line.startswith("html_data+='") or line.startswith("html_encoder(html_data)"):
                html_data += line

        html_data += "function html_encoder(s){var i=0,out='';l=s.length;for(;i<l;i+=3){out+=String.fromCharCode(parseInt(s.substr(i,2),16));}return out;}"

        # print(html_data)

        # res = js2py.eval_js(html_data)
        ctx = py_mini_racer.MiniRacer()
        res = ctx.eval(html_data)

        # print()
        # print(res)

        # second parsing
        soup2 = BeautifulSoup(res, 'html.parser')
        imgs = soup2.find_all('img')

        img_list = []

        idx = 1
        for img in imgs:
            attrs = img.attrs

            if "/img/loading-image.gif" != img.attrs['src']:
                continue

            for (k, v) in attrs.items():
                # print(k, v)
                if k.startswith("data-"):
                    img_url = v
                    ext = "jpg"

                    filename = img_url.split("/")[-1]
                    if "." in filename:
                        ext = img_url.split(".")[-1]
                        if "?" in ext:
                            ext = ext.split("?")[0]

                    if ext.startswith('php'):
                        ext = "jpg"

                    img_list.append({
                        "src" : img_url,
                        "name" : f"{title}_{idx:03}.{ext}"
                    })
                    idx = idx +1

        img_data = {
            "title" : title,
            "img_list": img_list
        }

        return img_data

    def do_connect_toki(self, url, domain, query):
        headers = {
            "accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            # "Accept-Encoding": 'gzip, deflate, br',
            # "accept-language": 'ko-KR,ko;q=0.9',
            "cache-control": 'max-age=0',
            # "if-modified-since": "Sat, 21 May 2022 07:08:50 GMT",
            # "Cookie": 'PHPSESSID=5bgg7hf84nkl9o5267u7ogovhkkjod1hhvo84vt6ui4m6jd262atmlpb19tc2jaq; e1192aefb64683cc97abb83c71057733=Y29taWM%3D',
            "sec-ch-ua": 'Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
            "sec-ch-ua-mobile": '?0',
            "sec-ch-ua-platform": 'macOS',
            "sec-fetch-dest": 'document',
            "sec-fetch-mode": 'navigate',
            "sec-fetch-site": 'none',
            "sec-fetch-user": '?1',
            "upgrade-insecure-requests": '1',
            "user-agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'
        }

        if url:
            withoutSch = url.split('//')[1]
            urlResult = withoutSch.split('/', 1)
            domain = urlResult[0]
            query = "/" + urlResult[1]

            # https://manatoki283.net/comic/14576816?stx=%EB%B4%87%EC%B9%98&spage=1
            # https://newtoki283.com/webtoon/27571572/%EC%95%84%ED%8F%AC%ED%81%AC%EB%A6%AC%ED%8C%8C-22%ED%99%94?toon=%EC%9D%BC%EB%B0%98%EC%9B%B9%ED%88%B0&spage=1

            if 'new' in domain:
                array = query.split('/', 3)
                new_query = f'/{array[1]}/{array[2]}'
                query = new_query


        #conn = http.client.HTTPSConnection(domain, 443)
        payload = ''

        #print(f'query {query}')
        #print(f'domain {domain}')


        #conn.request("GET", query, payload, headers)
        #res = conn.getresponse()

        #print(f'res {res}')
        #data = res.read()

        send_url = f'https://{domain}{query}'
        scraper = cloudscraper.create_scraper()

        print(send_url)

        response = scraper.get(send_url)
        time.sleep(5)
        print(response)

        data = response.text

        print(f'data {data}')

        result = data.decode("utf-8")

        return result
