from api_define import get_user_role
from common.get_user_role import getUserRole
from tornado_serve.common.deal_data_by_redis import getValue
import json

class GetUserRole(get_user_role):
    def entry(self, response_self):
        body = eval(response_self.request.body)
        sessionId = str(body["sessionId"])
        username=getValue(sessionId)
        if username!=None:
            userRole=getUserRole(username)
            return json.dumps({"status": 1, 'data': userRole,}, ensure_ascii=False)
        else:
            return json.dumps({"status":0,'data':'','errorinfo':'未登录'})
