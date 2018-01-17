from tornado_serve.common.get_class_or_stu_by_user import getClassOrStuByUser
from tornado_serve.common.deal_data_by_redis import getValue
class GetManageClass():
    def  entry(self,receiveRequest):
        body = eval(receiveRequest.request.body)
        sessionId = str(body["sessionId"])
        userName=getValue(sessionId)
        if userName==None:
            return {'status':0,'errorInfo':'登录状态已过期，请重新登录'}

        manageClass=getClassOrStuByUser(userName,0)
        return {'status':1,'classList':manageClass,'info':'请求成功'}


