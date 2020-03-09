from jira import JIRA

user = 'gea8861@naver.com'
apikey = 'api'
server = 'jira url'

options = {
 'server': server
}

jir = JIRA(server, basic_auth=(user,apikey))

#프로젝트 명
for project in jir.projects():
    print(project)

#프로젝트 issue key  
jql = 'project = PRC1'
issues=jir.search_issues(jql, maxResults=10000)

for issue in issues :
    issue = jir.issue(issue)
    print(issue)

#이슈 key로 summary 가져오기
iss = jir.issue('prc1-2')
sum = iss.fields.summary
print(sum)
