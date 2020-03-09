from jira import JIRA

#과거엔 id와 pw를 사용했는데 더 이상 id를 사용하지 않고 email과 api를 pw로 사용한다.

user = 'gea8861@naver.com'
apikey = 'api'
server = 'jira url'

options = {
 'server': server
}

jir = JIRA(server, basic_auth=(user,apikey))
