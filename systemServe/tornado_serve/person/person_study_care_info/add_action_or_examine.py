from tornado_serve.orm import stu_all_aspect_info,db
from tornado_serve.common.deal_data_by_redis import getValue
from tornado_serve.common.judge_permission import judgeIfPermiss
from datetime import datetime
from tornado_serve.common.deal_dateortime_func import dateTimeChangeToIntWithTime

class AddActionOrExamine(object):
    def entry(self,receiveRequest):
        self.requestData = eval(receiveRequest.request.body)
        userName = getValue(self.requestData['sessionId'])
        # self.requestData=receiveRequest
        stuId=self.requestData['stuId']
        # userName='wangjianting'
        role=self.requestData['role']
        if userName == None:
            return {'status': 0, 'errorInfo': '登陆状态已过期，请重新登录'}
        elif judgeIfPermiss(user_id = userName, stuid = stuId, mode = 0) == False:
            return {"status":0, "errorInfo":"用户没有操作该学生的权限"}

        if role=='fudaoyuan':
            if judgeIfPermiss(user_id=userName, mode=1, page="fudaoyuanEdit") == False:
                return {"status": 0, "errorInfo": "当前用户没有进行此项操作的权限"}
            with db.execution_context():
                thisStu=stu_all_aspect_info.select(stu_all_aspect_info.stuID,stu_all_aspect_info.fudaoyuan,stu_all_aspect_info.latelyEditTime).where(stu_all_aspect_info.stuID==stuId)
                thisStu=thisStu[0]
                fudaoyuanActions=eval(thisStu.fudaoyuan)
                nowTime=datetime.now()
                oneAction={'time':str(nowTime.strftime('%Y-%m-%d %H:%M')),'editUser':userName,
                           'content':self.requestData['content']}
                fudaoyuanActions.insert(0,oneAction)
                thisStu.fudaoyuan=str(fudaoyuanActions)
                thisStu.latelyEditTime=dateTimeChangeToIntWithTime(nowTime)
                thisStu.save()
        elif role=='fushuji':
            if judgeIfPermiss(user_id=userName, mode=1, page="toExamineEdit") == False:
                return {"status": 0, "errorInfo": "当前用户没有进行此项操作的权限"}
            with db.execution_context():
                thisStu=stu_all_aspect_info.select(stu_all_aspect_info.stuID,stu_all_aspect_info.fushuji,stu_all_aspect_info.latelyEditTime).where(stu_all_aspect_info.stuID==stuId)
                thisStu=thisStu[0]
                fushujiActions=eval(thisStu.fushuji)
                nowTime=datetime.now()
                oneAction={'time':str(nowTime.strftime('%Y-%m-%d %H:%M')),'editUser':userName,
                           'content':self.requestData['content']}
                fushujiActions.insert(0,oneAction)
                thisStu.fushuji=str(fushujiActions)
                thisStu.latelyEditTime=dateTimeChangeToIntWithTime(nowTime)
                thisStu.save()
        else:
            return {"status": 0, "errorInfo": "无效用户身份"}

        return {
                "status":1,
                "info":'请求成功',
                "data":oneAction
                     #将此处返回的data中的信息绑定到对应的地方（如辅导员措施处，或审核意见处）
                }


