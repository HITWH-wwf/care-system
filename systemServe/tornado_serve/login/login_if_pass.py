#coding=utf8

from api_define import login_if_pass
from orm import *
from get_user_role import getUserRole
#from get_nowuser_role import getNowUserRole
from login.my_session import Session
import json
from logConfig import logger

class LoginIfPass(login_if_pass):

    def entry(self, response_self):
        body = eval(response_self.request.body)
        user_name = str(body["userId"])
        user_pwd = str(body["password"])
        # print(user_name, "   ", user_pwd)
        return self.judge(response_self,user_name,user_pwd)

    def judge(self,response_self,user_name,user_pwd):
        try:
            nowuser=MyBaseModel.returnList(new_users.select().where(new_users.username==user_name))
            if len(nowuser)>0:
                if nowuser[0]['userpass']==user_pwd:
                    user_roles=getUserRole(user_name)
                    #user_roles=getNowUserRole(user_name)
                    my_session=Session(response_self)
                    session_id=my_session.get_session_id()
                    my_session['name']=user_name
                    logger.info('用户：%s 登录'%user_name)
                    return json.dumps({"status":1,'data':user_roles,'session_id':session_id},ensure_ascii=False)
                else:
                    logger.info('用户：%s 登录失败，原因：密码错误' % user_name)
                    return json.dumps({"status": 0, "errorInfo": "密码错误"}, ensure_ascii=False)

            else:
                logger.info('用户：%s 登录失败，原因：该用户不存在' % user_name)
                return json.dumps({"status": 0,"errorInfo": "该用户名不存在"},ensure_ascii=False)
        except:
            raise


