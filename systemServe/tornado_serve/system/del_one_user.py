#coding=utf8


from judge_permission import judgeIfPermiss
from api_define import del_one_user
from orm import *
from common.judge_permission import judgeIfPermiss

class DelOneUser(del_one_user):

    def entry(self, response_self):
        body = eval(response_self.request.body)
        user_id = str(body["userId"])
        user_name_want = str(body["userName"])

        if judgeIfPermiss(user_id=user_id, mode=1, page="systemUsers") == False:
            return {"status":0, "errorInfo":"用户没有权限设置"}
        return self.delMysql(user_name_want)

    def delMysql(self, user_name):
        with db.execution_context():
            judge = new_users.select().where(new_users.username == user_name).aggregate(fn.Count(new_users.username))
        if judge == 0:
            return {"status":0, "errorInfo":"不存在所要删除用户"}
        try:
            with db.execution_context():
                new_users.delete().where(new_users.username == user_name).execute()
        except:
            raise
            # return {"status":0, "errorInfo":"删除过程中出错，请稍候重试"}

        return {"status":1, "errorInfo":""}
