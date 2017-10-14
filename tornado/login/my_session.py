#coding=utf8
import hashlib
import time
import redis

def md5():
    m = hashlib.md5()
    m.update(bytes(str(time.time()), encoding='utf8'))
    return m.hexdigest()

class Session(object):

    def __init__(self, request):
        body = eval(request.request.body)
        try:
            session_value = str(body["session_id"])     #取出其中的session_id
        except:
            session_value=False                     #没有对对应的session_id
        if not session_value:  # 如果没有说明是第一次请求，需要生成一个随机字符串当作cookie
            self._id = md5()
        else:
            self._id = session_value

    def __getitem__(self, key):

        r = redis.Redis(host='127.0.0.1', port=6379)
        r.expire(self._id,1800)       #只要有操作，登陆状态就继续保持30分钟
        return r.get(self._id)

    def __setitem__(self,key,value):
        # user = chenchap   pwd = 123.com
        r = redis.Redis(host='127.0.0.1', port=6379)
        middle = r.set(self._id, value, ex=1800)
        return middle    #登陆状态保持30分中

    def __delitem__(self, key):
        r = redis.Redis(host='127.0.0.1', port=6379)
        return r.delete(self._id)

    def get_session_id(self):
        return self._id
