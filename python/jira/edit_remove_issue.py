from jira import JIRA

user = 'gea8861@naver.com'
apikey = 'api'
server = 'jira url'

options = {
 'server': server
}

jir = JIRA(server, basic_auth=(user,apikey))

issue=jira.issue('prc1-3')

#수정
issue.update(fields={'summary' : 'change summary', 'description' : 'change description'})

#제거
issue.remove()
