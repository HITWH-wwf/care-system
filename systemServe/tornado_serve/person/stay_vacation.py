from tornado_serve.orm import *
from tornado_serve.common.judge_permission import judgeIfPermiss
'''
{
'sessionId':....,
"userId":用户名,
'stuId':....,
'vacation':'summer'/'winter',
'stayDate':[{'from':'2010-01-01','to':'2010-01-04'},{},{}.....]
}
'''
class StayVacation():
    def entry(self,receiveRequest):
        self.requestData = eval(receiveRequest.request.body)
        userId = self.requestData['userId']
        stuId = self.requestData['stuId']
        vacation = self.requestData['vacation']
        stayDate = self.requestData['stayDate']
        if judgeIfPermiss(user_id=userId, mode=1, page="person") == False:
            return {"status": 0, "errorInfo": "用户没有操作此页面的权限"}
        elif judgeIfPermiss(user_id=userId, stuid=stuId, mode=0) == False:
            return {"status": 0, "errorInfo": "用户没有操作该学生的权限"}
        else:
            return self.stayVacationInfo(stuId,vacation,stayDate)

    def stayVacationInfo(self,stuId,vacation,stayDate):
        with db.execution_context():
            thisStu=stu_some_state.select().where(stu_some_state.stuID==stuId)
            if len(thisStu)==0:
                return {'status':0,'errorInfo':'查询不到该学生'}
            thisStu=thisStu[0]
            thisStu.vacationStayflag=vacation
            thisStu.stayDate=str(stayDate)
            thisStu.save()
        return {'status':1,'info':'操作成功'}