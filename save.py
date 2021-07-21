# 구글 엑셀 시트로 열 수 있도록, [jobs.csv] 파일 만들거임
# save.py가 실행되고 나면 [jobs.csv] 파일 만들어진다!
import csv # csv 파일로 작성할 수 있음

def save_to_file(jobs):
  file = open("jobs.csv", mode = "w") #jobs.csv 파일 생성
  writer = csv.writer(file) # open한 파일에 csv로 적기
  writer.writerow(["Title", "Company", "Location", "ApplyLink"]) # 엑셀 한 Cell 마다 구분해주려면 (지금처럼)한 데이터씩 ★콤마★로 구분지어서 List에 넣어줘야함
  for job in jobs:
    writer.writerow(list(job.values())) #writer.writerow(job.values()) # jobs에 저장된 {} 형태는 dictionary 라서 값(values)만 불러올 수 있는 dictionary 기능 제공함 #list()로 감싸서 dict_values로 묶인 상태를 없앰

  return
  
  

"""
이후 실행할 순서들

Step 1) [save.py]실행 후 [jobs.csv]파일 생성됨
Step 2) [jobs.csv] 파일 다운로드하기
Step 3) 구글 엑셀 파일 -> 파일(File) -> 가져오기(Import) -> [Upload]에서 파일 열기

"""
