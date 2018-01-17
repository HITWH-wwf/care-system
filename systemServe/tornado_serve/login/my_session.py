#coding=utf8
import hashlib
import time
from tornado_serve.common.deal_data_by_redis import saveData

def md5():
    m = hashlib.md5()
    m.update(bytes(str(time.time()), encoding='utf8'))
    return m.hexdigest()

class Session(object):

    def __init__(self, request):
        body = eval(request.request.body)
        try:
            session_value = str(body["sessionId"])     #取出其中的session_id
        except:
            session_value=False                     #没有对对应的session_id
        if not session_value:  # 如果没有说明是第一次请求，需要生成一个随机字符串当作cookie
            self._id = md5()
        else:
            self._id = session_value


    def __setitem__(self,key,value):
        # user = chenchap   pwd = 123.com
        # r = redis.Redis(host='127.0.0.1', port=6379)
        # middle = r.set(self._id,value, ex=1800)
        return saveData(self._id,value)    #登陆状态保持30分中


    def get_session_id(self):
        return self._id
