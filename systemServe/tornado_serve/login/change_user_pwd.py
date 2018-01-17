from api_define import change_user_pwd
from orm import *

import json
from logConfig import logger

'''
请求方式：post
请求url：地址+/login/change-user-pwd
请求数据格式：
{
    'userId':admin,
    'oldpwd':   ,
    'newpwd1':  ,
    'newpwd2':  ,
}

返回数据格式
{
    'status':1, info:    ,       成功
    或
    'status':0, errorInfo:  ,    失败
}
前段只需判断status的值，然后将info/errorInfo的值输出即可
'''


class ChangeUserPwd(change_user_pwd):

    def entry(self, response_self):
        body = eval(response_self.request.body)
        user_name = str(body["userId"])
        user_oldpwd = str(body["oldpwd"])
        user_newpwd1= str(body["newpwd1"])
        user_newpwd2=str(body["newpwd2"])

        # print(user_name, "   ", user_pwd)
        return self.change(user_name,user_oldpwd,user_newpwd1,user_newpwd2)

    def change(self,user_name,user_oldpwd,user_newpwd1,user_newpwd2):
        try:
            nowuser=new_users.select().where(new_users.username==user_name)
            if len(nowuser)>0:
                if nowuser[0].userpass==user_oldpwd:
                    #user_roles=getNowUserRole(user_name)
                    if user_newpwd1==user_newpwd2:
                        nowuser[0].userpass=user_newpwd1
                        nowuser[0].save()
                        logger.info('用户：%s 修改密码成功'%user_name)
                        return json.dumps({"status":1,'info':'修改密码成功'},ensure_ascii=False)
                    else:
                        return json.dumps({"status": 0, "errorInfo": "两次输入的新密码不一致"}, ensure_ascii=False)
                else:
                    logger.info('用户：%s 修改密码失败，原因：原密码输入错误' % user_name)
                    return json.dumps({"status": 0, "errorInfo": "原密码不正确"}, ensure_ascii=False)

            else:
                logger.info('用户：%s 修改密码失败，原因：该用户不存在' % user_name)
                return json.dumps({"status": 0,"errorInfo": "修改失败，该用户不存在"},ensure_ascii=False)
        except:
            raise

