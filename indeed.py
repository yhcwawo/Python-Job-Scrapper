# Indeed의 [Jobs]
# Step1. URL 가져오기
# Step2. request 하기(to.서버)
# Step3. Jobs 가져오기
# 참고 - .string과 .text 차이 - https://www.inflearn.com/questions/3945

import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://www.indeed.com/jobs?q=python&limit={LIMIT}" # URL 가져오기


# indeed 페이지 중 가장 마지막 페이지 return
def get_last_page():
  result = requests.get(URL) # 실행시 에러 안 나오면 성공한 것임!
  # print(indeed_result.text) # 실행시 Resonse 뜻 = OK, url에서 html들 가져오기
  soup = BeautifulSoup(result.text, "html.parser") # get을 통해 가져온 html document를 html.parser이용하여 쪼개기
  # print(indeed_result)

  pagination = soup.find("div", {"class": "pagination"}) # 페이지 숫자(결과)에 해당하는 html들 가져와서 pagination에 저장

  #print(pagination)

  links = pagination.find_all('a') # pagination html 속 모든! anchor(링크) 들 리스트! 형태로 저장

  #print(pages)

  # 숫자가 안 들어있는 맨 마지막 내용만 지우고 출력하고 싶을 때
  pages = [] # page 숫자들 저장할 List 
  for link in links[0:-1]: #pages = pages[0:-1] 한 번에 넣어서 마지막 요소 없앰으로서 에러 방지. 즉, 모든 span들을 가져오되, 마지막 것은 제한다. ex) pages[0:5]는 0부터 시작해서 5까지 가져오는 것
    #pages.append(link.find("span").string) #List에 <span>태그 속 문자열들만 append
    pages.append(int(link.string)) # 위처럼 안 해도 됨. <a>의 요소가 <span> 한 개이고, string이 한 개이면 link.string으로 간단히해도 됨
  # print(pages) # List 형식으로 출력됨
  max_page = pages[-1] # 마지막 숫자 = 가장 큰 숫자
  return max_page


# job당 Title, Company, Location, ApplyLink로 정보 쪼개서 정리한 리스트 반환
def extract_job(html):
   title = html.select_one('.jobTitle>span').string #'new' 오류나는 title = html.find("h2", {"class":"jobTitle"}).find("span").string 대신 select_one 함수로!! 
   #print(title)
      #<span> 속 title에 저장되어있는 job들 가져오기
   company = html.find("span", {"class":"companyName"}) # text내용을 가져와줄 .string #.string 안 해주면 html이 저장됨
   company_anchor = company.find("a") 
   #company 이름 중 링크(a)가 걸린 것도 아닌 것도 있음. company 정보가 <span>에 걸려 있는 경우와, <a>에 걸려 있는 찾아지는 경우가 나뉜다는 뜻
   if company_anchor is not None: # 링크(a)에 company 정보가 있는 경우
     company =str(company_anchor.string)  
   else:
     company = str(company.string) # 링크(a)에 없고 span에 company 정보가 있는 경우
    #company = company.strip() # 빈 칸들 없애줌
   #print(title, company) 
   
   location = html.select_one("pre > div").text # 오류나는 html.find("div", {"class":"companyLocation"}).string 대신 select_one과 .text로!!!
   job_id = html.parent['data-jk'] # .parent 중요! 받아온 html의 부모 태그인 <a>에 [data-jk] 속성이 있음(사이트 업뎃 때문인듯)
   #print(job_id)# job_id는 지원링크의 id
   #print(location)
   #print(title)
   #print(result.status_code) # request가 last_page번 잘 되는지 확인해보는용
   return {
     'Title': title, 
     'Company': company, 
     'Location': location,
     'ApplyLnk': f"https://www.indeed.com/viewjob?jk={job_id}&from=web&vjs=3"
     }



# 해당 페이지의 모든 Job 추출
def extract_jobs(last_page):
 jobs = [] 
 for page in range(last_page): #page는 0부터 시작
    print(f"Scrapping Indeed Page: {page}") # 코드실행 진행여부 확인용
    result = requests.get(f"{URL}&start={page*LIMIT}")  
    # 페이지 넘어갈 때마다! URL의 맨 뒤에 &limit={배열*50} 형태를 넣어준 상태에서 다음 페이지 request 해야함 #HTTP 통신상 한 URL씩 request해야 html 내용 가져올 수 있음
    # print(result)
    soup = BeautifulSoup(result.text,"html.parser")
    results = soup.find_all("div", {"class":"slider_container"}) # 직업군 애용있는 html 가져오기
    
    for result in results:
      job = extract_job(result) # result은 html 저장중
      jobs.append(job)
      #print(job)
 return jobs 


# Indeed의 모든 구직광고 내용 모아서 return
def get_jobs():
 last_page = get_last_page()
 #print(f"max_page is {last_page}")
 jobs = extract_jobs(last_page)
 return jobs