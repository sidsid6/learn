from jira import JIRA

user = 'gea8861@naver.com'
apikey = 'api'
server = 'jira url'

options = {
 'server': server
}

jir = JIRA(server, basic_auth=(user,apikey))

jql = 'project = PRC1'
issues=jir.search_issues(jql, maxResults=10000)

for issue in issues :
    issue = jir.issue(issue)
    print(issue) # 결과값 str 반환

#이슈 key로 summary 가져오기 , 결과값 str 반환
iss = jir.issue('prc1-2')
sum = iss.fields.summary
print(sum)

#이슈 현재 진행 상황 가져오기
st = iss.fields.status

#결과값 4가지 : 1. Backlog(이슈 생성만 하고 대기중인 것) 2. Selected For Development(개발하기로 선택된 이슈) 3. 진행중 4. 완료됨
print(st)
