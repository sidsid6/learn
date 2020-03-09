from jira import JIRA

user = 'gea8861@naver.com'
apikey = 'api'
server = 'jira url'

options = {
 'server': server
}

jir = JIRA(server, basic_auth=(user,apikey))

for project in jir.projects():
    print(project)
    
jql = 'project = PRC1'
issues=jir.search_issues(jql, maxResults=10000)

for issue in issues :
    issue = jir.issue(issue)
    print(issue)
