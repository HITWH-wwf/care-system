from tornado_serve.orm import *
from tornado_serve.common.judge_permission import judgeIfPermiss
'''
{
'sessionId':....,
"userId":用户名,
'stuId':....,
'showColor':'red'/'yellow'/'orange'
}
'''
class SetFocusColor():
    def entry(self,receiveRequest):
        # self.requestData = receiveRequest
        self.requestData = eval(receiveRequest.request.body)
        userId=self.requestData['userId']
        stuId=self.requestData['stuId']
        showColor=self.requestData['showColor']
        if judgeIfPermiss(user_id = userId, mode = 1, page = "person") == False:
            return {"status":0, "errorInfo":"用户没有操作此页面的权限"}
        elif judgeIfPermiss(user_id = userId, stuid = stuId, mode = 0) == False:
            return {"status":0, "errorInfo":"用户没有操作该学生的权限"}
        else:
            return self.setColor(stuId,showColor)

    def setColor(self,stuId,showColor):
        with db.execution_context():
            thisstu=stu_basic_info.select(stu_basic_info.stuID,stu_basic_info.state,stu_basic_info.focusColor).where(stu_basic_info.stuID==stuId)
            if len(thisstu)==0:
                return {"status":0, "errorInfo":"查询不到该学生"}
            thisstu=thisstu[0]
            if thisstu.state==0:
                return {"status": 0, "errorInfo": "该学生尚未被关注，无法修改颜色等级"}
            else:
                thisstu.focusColor=showColor
                thisstu.save()
        return {'status':1,'info':'操作成功'}
