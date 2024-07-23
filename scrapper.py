import os
import time
import requests
import concurrent.futures
import shutil
import urllib3
from zipfile import ZipFile, ZIP_DEFLATED
from functions import get_domain

class Scrapper:
    THIS_FOLDER = os.path.abspath(os.path.dirname(__file__))
    provider = ''
    type = ''

    def get_title_list(self, domain, search_keyword, provider, type):
        print('get_title_list')

    def get_chapter_links(self, url, domain, title):

        print('get_chapter_links')

    def get_img_data(self, url):

        print('get_img_data')

    def download(self, url, filename, dest_folder):
        try:
            dest_folder = os.path.join(self.THIS_FOLDER, dest_folder)
            file_path = os.path.join(dest_folder, filename)
            headers = {}

            if self.provider == 'jmana' or self.provider == 'toki':
                domain = get_domain(self.provider, self.type)
                headers = {"Referer" : f"https://{domain}/"}


            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

            r = requests.get(url, headers=headers, stream=True, verify=False)
            if r.ok:
                print("saving to", os.path.abspath(file_path))
                with open(file_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024 * 8):
                        if chunk:
                            f.write(chunk)
                            f.flush()
                            os.fsync(f.fileno())
            else:  # HTTP status code 4XX/5XX
                print("Download failed: status code {}\n{}".format(r.status_code, r.text))
        except Exception as e:
            print('url', url)
            print('예외가 발생했습니다.', e)

    def get_chapter_list(self, data):
        domain = get_domain(self.provider, data['type'])

        if domain:
            return self.get_chapter_links(data['link'], domain, data['title'], data['id'], data['type'])

        return

    def download_by_chapter(self, chapter_links):
        # print(chapter_links)

        start = time.time()
        comic_name = chapter_links[0]['comic_name']

        title_directory = os.path.join(self.THIS_FOLDER, comic_name)

        if not os.path.exists(title_directory):
            os.makedirs(title_directory)

        idx = 1
        for link in chapter_links:
            img_data = self.get_img_data(link['link'])

            chapter_name = img_data["title"]

            # 폴더명 index 처리 (순서 섞이는 것 방지)
            chapter_name = f"{int(link['idx']):03} {chapter_name}"

            dest_folder = os.path.join(comic_name, chapter_name)

            img_list = img_data["img_list"]

            # print(img_list)

            dest_folder_path = os.path.join(self.THIS_FOLDER, dest_folder)
            if not os.path.exists(dest_folder_path):
                os.makedirs(dest_folder_path)

            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                future_to_url = {executor.submit(self.download, img["src"], img["name"], dest_folder): img for img in img_list}
                for future in concurrent.futures.as_completed(future_to_url):
                    url = future_to_url[future]
                    try:
                        data = future.result()
                    except Exception as exc:
                        print('%r generated an exception: %s' % (url, exc))
            
            self.zipfolder(dest_folder)
            shutil.rmtree(dest_folder_path)

            idx += 1

        
        end = time.time() - start
        min = end // 60
        sec = end - (min * 60)

        print(f"소요시간 {min}분 {sec}초")


    def zipfolder(self, foldername):
        zip_name = foldername + '.zip'

        with ZipFile(zip_name, 'w', ZIP_DEFLATED) as zip_ref:
            for folder_name, subfolders, filenames in os.walk(foldername):
                for filename in filenames:
                    file_path = os.path.join(folder_name, filename)
                    zip_ref.write(file_path, arcname=os.path.relpath(file_path, foldername))

        zip_ref.close()