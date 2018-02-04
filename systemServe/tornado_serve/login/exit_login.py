from tornado_serve.common.deal_data_by_redis import delData

class ExitLogin():
    def entry(self,receiveRequest):
        body = eval(receiveRequest.request.body)
        sessionId = str(body["sessionId"])
        if delData(sessionId):
            return {'status':1,'info':'退出登录成功'}
        else:
            raise
