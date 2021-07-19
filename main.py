# python 구인광고 글 스크랩핑해서 엑셀시트에 저장
# Indeed와 StackOverflow 각각에서. html에서 정보 추출
# [Packages]-[requests : Python HTTP foR Humans]-[Add] 하기.
# 참고문헌 - https://docs.python-requests.org/en/master/

from indeed import get_jobs as get_indeed_jobs
from so import get_jobs as get_so_jobs
from save import save_to_file

indeed_jobs = get_indeed_jobs()
#print(indeed_jobs)
so_jobs = get_so_jobs()
print(so_jobs)
#jobs = indeed_jobs + so_jobs  # 
#save_to_file(jobs) # csv 파일 생성하기 위해 두 배열을 합쳐 만든 jobs 전달