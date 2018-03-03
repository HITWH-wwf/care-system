from tornado_serve.orm import *
from tornado_serve.common.judge_permission import judgeIfPermiss
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
            '发生日期','预警类型','预警原因'
        ],
    "propName": [
            'appearDate','earlyWarningKind','earlyWarningReason'
            

        ],
    "tableData": [{'appearDate':'2010-01-01','earlyWarningKind':'学情预警','earlyWarningReason':''}],
    "info":'请求成功'
}
'''

class GetStuWarningHistory():
    def entry(self,receiveRequest):
        reasons = {
            'costFixed1': '当天累计消费小于1元，连续1天；', 'costFixed2': '一次性消费超过50元；',
            'sleepFixed1': '当天晚上23：30前没有刷卡回宿舍记录；', 'sleepFixed2': '24小时内无任何出入寝室记录；',
            'scoreFixed1': '不及格科目超过3科；', 'scoreFixed2': '不及格科目累计12学分；', 'scoreFixed3': '不及格科目累计16学分；',
            'scoreFixed4': '不及格科目累计18学分；'
        }
        warningKind = {
            'costWarning': '消费预警', 'sleepWarning': '住宿预警', 'scoreWarning': '学情预警', 'aboveOne': '综合预警'
        }
        self.requestData = eval(receiveRequest.request.body)
        userId = self.requestData['userId']
        stuId = self.requestData['stuId']
        if judgeIfPermiss(user_id = userId, stuid = stuId, mode = 0) == False:
            return {"status":0, "errorInfo":"用户没有操作该学生的权限"}
        stuWarningHistory=MyBaseModel.returnList2(stu_some_state.select(stu_some_state.warningHistory).where(stu_some_state.stuID==stuId))
        if len(stuWarningHistory)==0:
            return {'status':0,'errorInfo':'未查询到该学生'}
        stuWarningHistory=stuWarningHistory[0]
        stuWarningHistory=eval(stuWarningHistory.warningHistory)
        tableData=[]
        for oneHistory in stuWarningHistory:
            oneRecord={'appearDate':oneHistory['appearDate'],'earlyWarningKind':warningKind[oneHistory['warningKind']],'earlyWarningReason':''}
            thisRecordReasons=oneHistory['warningReason']
            earlyWarningReason=''
            for i in thisRecordReasons:
                earlyWarningReason=earlyWarningReason+str(i+1)+'、'+reasons[thisRecordReasons[i]]
            oneRecord['earlyWarningReason']=earlyWarningReason
            tableData.append(oneRecord)
        resultData={
                "status":1,
                "colName": ['发生日期','预警类型','预警原因'],
                "propName": ['appearDate','earlyWarningKind','earlyWarningReason'],
                "tableData":tableData,
                "info":'请求成功'
                }
        return resultData