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

#이슈 우선순위 가져오기
priority= iss.fields.priority
#결과값 5가지 : 1.Highest   2.High   3.Medium   4.Low   5.Lowest
print(priority)

#이슈 해결여부 가져오기
resol=iss.fields.resolution
#결과값 : 1.미해결 : None   2.해결 : 완료됨
print(resol)

#이슈 상세정보(=설명) 가져오기
descript= iss.fields.description
print(descript)

#담당자 및 보고자
assignee = iss.fields.assignee
reporter = iss.fields.reporter
print(assignee)
print(reporter)

#생성일자 및 갱신일자
created = iss.fields.created
updated = iss.fields.updated
print(created)
print(updated)

#이슈 첨부파일(스크린 샷, 로그파일 등) 가져오기
att = iss.fields.attachments
print(att)
