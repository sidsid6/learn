#-*- coding: utf-8 -*-
from jira import JIRA

user = 'gea8861@naver.com'
apikey = 'api'
server = 'jira url'

options = {
 'server': server
}


jira = JIRA(server, basic_auth=(user,apikey))
jr=jira.project('prc1') # project name

issue= jira.issue('prc1-4') # issue key
jira.add_attachment(issue=issue, attachment='\file\path\flower.png')
