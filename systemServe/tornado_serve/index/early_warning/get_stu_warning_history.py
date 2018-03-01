from tornado_serve.orm import *

'''
{
'sessionId':....,
"userId":用户名,
'stuId':...
}

响应：
{
    "status":1,
    "colName": [
            列名的value
        ],
    "propName": [
            列名对应的key值，如：
            

        ],
    "tableData": [{},{},....],
    "info":'请求成功'
}
'''

class GetStuWarningHistory():
    def entry(self):
        pass