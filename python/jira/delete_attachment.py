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


query = jira.search_issues(jql_str="attachments is not EMPTY", json_result=True, fields="key, attachment")


#삭제할 첨부파일에 부여된 id를 알아야 함.
for i in query['issues']:
    for a in i['fields']['attachment']:
        print("For issue {0}, attachment_name: '{1}', attachment_id: [{2}].".format(i['key'], a['filename'], a['id']))
        
        #ex) For issue PRC1-4, attachment_name: 'flower.png', attachment_id: [10006]
             For issue PRC1-4, attachment_name: 'flower1.png', attachment_id: [10007]
             For issue PRC1-4, attachment_name: 'flower2.png', attachment_id: [10008] <- 제거원함
             
             
#삭제하고자 하는 첨부파일 id 확인 후, 제거
text1=input("제거할 첨부파일의 id를 입력하세요 : ") #10008 입력
for i in range(0,len(query['issues'][0]['fields']['attachment'])):
    if query['issues'][i]['fields']['attachment'][0]['id']==text1:
        jira.delete_attachment(query['issues'][i]['fields']['attachment'][0]['id'])
        break;
    else:
        pass

#file명으로 제거하기
text1=input("제거할 첨부파일유형 포함 파일명을 입력하세요.(ex: abc.png) : ")
for i in range(0,len(query['issues'][0]['fields']['attachment'])):
    if query['issues'][0]['fields']['attachment'][i]['filename']==text1:
        jira.delete_attachment(query['issues'][i]['fields']['attachment'][0]['id'])
        break;
    else:
        pass
