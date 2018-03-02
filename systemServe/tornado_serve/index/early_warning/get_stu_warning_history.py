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
Reason={
    'costFixed1':'当天累计消费小于1元，连续1天','costFixed2':'一次性消费超过50元',
    'sleepFixed1':'当天晚上23：30前没有刷卡回宿舍记录','sleepFixed2':'24小时内无任何出入寝室记录',
    'scoreFixed1':'不及格科目超过3科','scoreFixed2':'不及格科目累计12学分','scoreFixed3':'不及格科目累计16学分',
    'scoreFixed4':'不及格科目累计18学分'
}
warningKind={
    'costWarning':'消费预警','sleepWarning':'住宿预警','scoreWarning':'成绩预警'
}
class GetStuWarningHistory():
    def entry(self):
        pass