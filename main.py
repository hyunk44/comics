import concurrent.futures
from functions import *
from maru import *
from toki import *
from toonsarang import *
from cook import *
from jmana import *
from readallcomics import *
from xbato import *
from mangafire import *

def get_scrapper(provider, type):
    if provider == 'maru':
        return Maru(provider, type)
    elif provider == 'toki':
        return Toki(provider, type)
    elif provider == 'toonsarang':
        return Toonsarang(provider, type)
    elif provider == 'cook':
        return Cook(provider, type)
    elif provider == 'jmana':
        return Jmana(provider, type)
    elif provider == 'readallcomics':
        return ReadAllComics(provider, type)
    elif provider == 'xbato':
        return Xbato(provider, type)
    elif provider == 'mangafire':
        return Mangafire(provider, type)

    return

def get_search_list(provider, type, search_keyword):
    domain = get_domain(provider, type)
    scrapper = get_scrapper(provider, type)

    if scrapper:
        return scrapper.get_title_list(domain, search_keyword, provider, type)

    return {}


def main():
    search_keyword = input('검색할 만화 제목을 입력하세요\n> ')
    while not search_keyword:
        search_keyword = input('검색할 만화 제목을 입력하세요\n> ')

    config = read_file('config.json')
    provider_types = filter_provider_types(config['providers'])

    search_list = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(get_search_list, item['provider'], item['type'], search_keyword): item for item in provider_types}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                search_list.append(future.result())
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))

    result_list = []
    for sl in search_list:
        result_list.extend(sl)

    # 이름 정렬
    result_list = sorted(result_list, key=lambda e: (e['title']))

    idx = 1
    idxs = []
    map_by_idx = {}

    for data in result_list:
        provider = data['provider']
        type = data['type']
        title = data['title']
        id = data['id']

        print(f"[ {idx} ] {title} ({provider} {type} {id})")

        str_idx = str(idx)
        idxs.append(str_idx)
        map_by_idx[str_idx] = data
        idx += 1
    
    if map_by_idx:
        idx_select = input('다운로드할 항목의 번호를 입력하세요\n> ')
        while idx_select not in idxs:
            idx_select = input('다운로드할 항목의 번호를 입력하세요\n> ')
        
        data = map_by_idx[idx_select]

        id = data['id']
        type = data['type']
        provider = data['provider']
        scrapper = get_scrapper(provider, type)

        chapter_list = scrapper.get_chapter_list(data)
        
        ch_idxs = []
        for chp_data in chapter_list:
            ch_idxs.append(chp_data['idx'])
            print(f"[ {chp_data['idx']} ] {chp_data['sub_title']}")

        ch_idx_select = input('다운로드할 항목의 번호를 입력하세요(ex. 1,3,4) 0은 전체\n> ')
        if ch_idx_select:
            idxes = []

            if ',' in ch_idx_select:
                idxes = ch_idx_select.split(',')
                # print(f', idxes {idxes}')

            elif '-' in ch_idx_select:
                idxes = ch_idx_select.split('-')
                # print(f'- idxes {idxes}')

                if len(idxes) == 2:
                    temp_idxes = []
                    for i in range(int(idxes[0]), int(idxes[1])+1):
                        temp_idxes.append(str(i))
                    idxes = temp_idxes
            else:
                idxes.append(ch_idx_select)

            if not idxes or idxes[0] == '0':
                idxes = ch_idxs

            download_chapter_list = []

            for chp_data in chapter_list:
                if chp_data['idx'] in idxes:
                    download_chapter_list.append(chp_data)
            
            download_chapter_list = list(reversed(download_chapter_list))

            scrapper.download_by_chapter(download_chapter_list)



if __name__ == "__main__":
   main()


