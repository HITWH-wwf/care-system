from tornado_serve.orm import *
from tornado_serve.common.judge_permission import judgeIfPermiss
'''
{
'sessionId':
'userId':
'stuId':
'operation':'leaveSchool/dropSchool/returnSchool'
}
'''
class ChangeSchoolStatus():
    def entry(self,receiveRequest):
        self.requestData = eval(receiveRequest.request.body)
        userId = self.requestData['userId']
        stuId = self.requestData['stuId']
        operation=self.requestData['operation']
        if judgeIfPermiss(user_id = userId, mode = 1, page = "person") == False:
            return {"status":0, "errorInfo":"用户没有操作此页面的权限"}
        elif judgeIfPermiss(user_id = userId, stuid = stuId, mode = 0) == False:
            return {"status":0, "errorInfo":"用户没有操作该学生的权限"}
        else:
            return self.setSchoolStatus(stuId,operation)

    def setSchoolStatus(self,stuId,operation):
        operationKind={'leaveSchool':'退学','dropSchool':'休学','returnSchool':'复学'}
        with db.execution_context():
            thisStu=stu_basic_info.select(stu_basic_info.stuID,stu_basic_info.schoolStatus).where(stu_basic_info.stuID==stuId)
            thisStu=thisStu[0]
            thisStu.schoolStatus=operationKind[operation]

        return {'status':1,'info':'操作成功'}