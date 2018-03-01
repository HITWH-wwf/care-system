from tornado_serve.orm import *
'''
{
'sessionId':....,
"userId":用户名
}

响应：
{
    "status":1,
    "colName": [
            列名的value，如：
             学号，姓名，专业,.....预警类型
        ],
    "propName": [
            列名对应的key值，如：
            "stuId","stuName","major",.....,'earlyWarningKind'

        ],
    "tableData": [{....,,'rank':'red/blue/yellow/orange'},{},....],
    "info":'请求成功'

'''

class GetEarlyWarningStu():
    def entry(self):
        pass
