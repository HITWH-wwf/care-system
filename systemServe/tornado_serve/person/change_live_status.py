from tornado_serve.orm import *
from tornado_serve.common.judge_permission import judgeIfPermiss
'''
{
'sessionId':....,
"userId":用户名,
'stuId':....,
'operation':'set/cancel',
'kind':'sleepOutSchool'/'studyWihtParent'

}
'''
class ChangeLiveStatus():
    def entry(self,receiveRequest):
        self.requestData = eval(receiveRequest.request.body)
        userId = self.requestData['userId']
        stuId = self.requestData['stuId']
        operation = self.requestData['operation']
        kind=self.requestData['kind']
        if judgeIfPermiss(user_id=userId, mode=1, page="person") == False:
            return {"status": 0, "errorInfo": "用户没有操作此页面的权限"}
        elif judgeIfPermiss(user_id=userId, stuid=stuId, mode=0) == False:
            return {"status": 0, "errorInfo": "用户没有操作该学生的权限"}
        else:
            return self.setLiveStatus(stuId, operation,kind)

    def setLiveStatus(self,stuId,operation,kind):
        with db.execution_context():
            thisStu=stu_basic_info.select(stu_basic_info.stuID,stu_basic_info.sleepInOrOut,stu_basic_info.studyWithParent).where(stu_basic_info.stuID==stuId)
            thisStu=thisStu[0]
            if kind=='sleepOutSchool':
                if operation=='set':
                    thisStu.sleepInOrOut='是'
                else:
                    thisStu.sleepInOrOut = '否'
            elif kind=='studyWithParent':
                if operation=='set':
                    thisStu.studyWithParent='是'
                else:
                    thisStu.studyWithParent = '否'
            thisStu.save()

        return {'status':1,'info':'操作成功'}