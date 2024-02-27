import requests
from bs4 import BeautifulSoup
import re
import json
import os
from datetime import datetime, timedelta
from tqdm import tqdm

# 과 이름에 대한 코드 매핑
hidak_all = {
    # '소화기내과': 'PMG00',
    '호흡기내과': 'PMP00',
    '감염내과': 'PMI00',
    '알레르기내과': 'PMA00',
    '내분비내과': 'PME00',
    '순환기내과': 'PMC00',
    '신장내과': 'PMN00',
    '류마티스내과': 'PMR00',
    '혈액종양내과': 'PMO00',
    '성형외과': 'PA000',
    '정형외과': 'PO000',
    '신경외과': 'PB000',
    '대장항문': 'PGI00',
    '흉부외과': 'PC000',
    '외과': 'PG000',
    '피부과': 'PS000',
    '안과': 'PH000',
    '치과': 'PV000',
    '비뇨의학과': 'PU000',
    '산부인과': 'PY000',
    '한방과': 'PL000',
    '신경과': 'PN000',
    '재활의학과': 'PR000',
    '정신건강의학과': 'PP000',
    '응급의학과': 'PJ000',
    '마취통증의학과': 'PT000',
    '방사선종양학과': 'PX000',
    '영상의학과': 'PK000',
    '진담검사의학과': 'PQL00',
    '작업환경의학과': 'PQ000',
}

def crawl_links_by_department(department_code):
    head = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"}
    link_list = []

    for page in range(1, 10): 
        url = f"https://mobile.hidoc.co.kr/healthqna/part/list?code={department_code}&page={page}"
        r = requests.get(url, headers=head)
        bs = BeautifulSoup(r.text, 'html.parser')

        data = bs.find("section", class_='contents').find_all("a") 

        pattern = r'href="(view[^"]+)"'
        for tag in data:
            tag_str = str(tag)  
            match = re.search(pattern, tag_str)
            if match:
                link = match.group(1)
                link_list.append(link)
    return link_list


today = datetime.today().strftime('%Y-%m-%d')

for department, code in tqdm(hidak_all.items()):
    file_name = f"{code}_{department}.json"

    if os.path.exists(file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            file_qna = json.load(f)
    else:
        print(f"{department}  데이터가 없습니다.")
        file_qna = {}

    link_list = crawl_links_by_department(code)

    # json 중복되지 않는 질문 link만 오늘날짜로 json 파일 생성
    new_links = list(set(link_list) - set(file_qna.get(department, [])))
    
    today_qna = {department: new_links}

    new_file_name = f"{code}_{department}_{today}.json"

    with open(new_file_name, 'w', encoding='utf-8') as f:
        json.dump(today_qna, f, ensure_ascii=False, indent=4)

    if not new_links:
        print(f"{department} 새로운 데이터가 없습니다.")
