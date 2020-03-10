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

