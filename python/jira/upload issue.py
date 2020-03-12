from jira import JIRA

user = 'gea8861@naver.com'
apikey = 'api'
server = 'jira url'

options = {
 'server': server
}

# 이슈 생성 시,   1.project명  2.summary  3.description  4.issuetype 이 필수로  


# 방법 1 
iss = jira.issue('issue key')
new_issue = jira.create_issue(project='project name', summary='요약내용', description='설명', issuetype={'name': 'Bug'})


# 방법 2. 딕셔너리 사용 , 이슈 여러개 한번에 생성가능
issue_dict = {
    'project': {'name': 'PRC1'},
    'summary': '요약내용',
    'description': '설명',
    'issuetype': {'name': 'Bug'},
}
new_issue = jira.create_issue(fields=issue_dict)

# 여러개 한번에 넣는 방법( 만들 이슈들을 각각 딕셔너리로 만들고 리스트의 원소로 한다. )
issue_list = [
{
    'project': {'key': 'PRC1'},
    'summary': 'First issue of many',
    'description': 'Look into this one',
    'issuetype': {'name': 'Bug'},
},
{
    'project': {'key': 'PRC1'},
    'summary': 'Second issue',
    'description': 'Another one',
    'issuetype': {'name': 'Bug'},
},
{
    'project': {'key': 'PRC1'},
    'summary': 'Last issue',
    'description': 'Final issue of batch.',
    'issuetype': {'name': 'Bug'},
}]
n_issues = jira.create_issues(field_list=issue_list)
