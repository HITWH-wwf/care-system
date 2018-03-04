from tornado_serve.orm import *
from tornado_serve.common.judge_permission import judgeIfPermiss
import datetime
'''
{'sessionId':....,
"userId":用户名,
'stuId':....,
'operation':'cancel'/'changeToLongCare'
}
'''
class ChangeEarlyWarningState():
    def entry(self,receiveRequest):
        # self.requestData = receiveRequest
        self.requestData = eval(receiveRequest.request.body)
        userId = self.requestData['userId']
        stuId = self.requestData['stuId']
        operation=self.requestData['operation']
        if judgeIfPermiss(user_id=userId, stuid=stuId, mode=0) == False:
            return {"status": 0, "errorInfo": "用户没有操作该学生的权限"}
        if operation=='cancle':
            with db.execution_context():
                thisStu=stu_some_state.select().where(stu_some_state.stuID==stuId)
                thisStu=thisStu[0]
                thisStu.earlyWarningInfo=str({'costWarning':0,'costColor':'blue','sleepWarning':0,'sleepColor':'blue','scoreWarning':0,'scoreColor':'blue',
                        'aboveOneWarning':'no','aboveOneColor':'blue'})
                thisStu.save()
            return {'status':1,'info':'操作成功'}
        else:
            return self.changeToLongCare(stuId)

    def changeToLongCare(self,stuId):
        with db.execution_context():
            judgeStuIsFocus=MyBaseModel.returnList2(stu_focus.select().where(stu_focus.stuID==stuId))
            if len(judgeStuIsFocus)>0:
                return {"status":0, "errorInfo":"操作失败，该学生已处于关注状态"}
            thisStu = stu_some_state.select().where(stu_some_state.stuID == stuId)
            thisStu = thisStu[0]
            earlyWarningInfo=eval(thisStu.earlyWarningInfo)
            warningKind = {
                'costWarning': '消费预警', 'sleepWarning': '住宿预警', 'scoreWarning': '学情预警', 'have': '综合预警'
            }
            appearWarning=earlyWarningInfo['aboveOneWarning']
            appearWarning=warningKind[appearWarning]
            thisStu.earlyWarningInfo = str(
                {'costWarning': 0, 'costColor': 'blue', 'sleepWarning': 0, 'sleepColor': 'blue', 'scoreWarning': 0,
                 'scoreColor': 'blue',
                 'aboveOneWarning': 'no', 'aboveOneColor': 'blue'})
            thisStu.save()
            reason='由于发生预警状态：'+appearWarning+'，所以转为长期关注'
            stu_focus.create(**{"stuID": stuId, "style": 1, "reason": reason, "level": 3,
                                "createDate": str(datetime.datetime.now())})
            stu = stu_basic_info.select().where(stu_basic_info.stuID == stuId).get()
            stu.state = 3
            stu.save()
        return {'status':1,'info':'操作成功'}




