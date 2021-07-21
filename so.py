# StackOverflow의 [Jobs]
# Indeed때와 원리는 같음

import requests
from bs4 import BeautifulSoup


URL = f"https://stackoverflow.com/jobs?q=python"

def get_last_page():
  result = requests.get(URL) 
  soup = BeautifulSoup(result.text, "html.parser") # 모든 html 소스코드 가져오기
  pagination = soup.find("div", {"class" : "s-pagination"}) #class 이름이 pagination에 해당하는 html 소스코드만 가져오기 
  pages = pagination.find_all("a") #anchor들(find()는 한 개만) 가져오기
  last_page = pages[-2].get_text(strip = True)# 가장 큰 숫자를 가져올 때, <next> 버튼 내용을 없애준 상태여야 마지막의 페이지 숫자를 손쉽게 가져올 수 있다 # [-1]이 마지막 내용인 next이니 그 전 숫자인 86을 가져오려면 [-2]
  # strip으로 공백 없애기
  return int(last_page) #last_page가 str이라 integer로 변환해서 return


def extract_job(html):
  title = html.find("h2", {"class" : "mb4"}).find("a")["title"] # 직무명
  company, location = html.find("h3", {"class":"fc-black-700"}).find_all("span",recursive = False) # "span"이 Nest 구조일 때 find_all함수로 부를 때, span 한 개씩만 가져오게 recursive = False #recursive로 리스트 언팩킹
  company = company.get_text(strip = True) #공백 삭제
  location = location.get_text(strip = True)
  job_id = html['data-jobid']
  return {
    'Title' : title,
    'Company': company,
    'Location': location,
    'Apply_link' : f"https://stackoverflow.com/jobs/{job_id}"
    }



def extract_jobs(last_page):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping StackOverflow Page: {page}") # 코드실행 진행여부 확인용
    result = requests.get(f"{URL}&pg={page+1}") #마지막 숫자가 86 그대로 되기 위해서 {page+1}로 해줌
    #print(result.status_code) # 200이 찍힌다는 건 통신이 잘 되었다는 뜻
    soup = BeautifulSoup(result.text, "html.parser") # BeautifulSoup로 끓이면 html들을 보기 좋게(Nested 형태로) 만듦
    results = soup.find_all("div", {"class" : "-job"}) # 모든 div 저장

    for result in results:
     job = extract_job(result)
     #print(job)
     jobs.append(job)
  return jobs


# StackOverflow의 모든 구직광고 내용 모아서 return
def get_jobs():
 last_page = get_last_page()
 jobs = extract_jobs(last_page)
 return jobs