#coding=utf8
from judge_permission import judgeIfPermiss
from api_define import set_one_user
from orm import *

class SetOneUser(set_one_user):
    """
    设定一个用户的信息，前端发来的信息为：
    "userId": "admin",
    "userName": "用户一",
    "data": {
        "userName": "用户一",
        "description": "巴拉巴拉",
        "userTeam": "用户组一",
        "roleTeam": "角色组一",
        "oldPassWord": "1234", //oldPassWord与newPassword成对出现。如果在data中没有该关键字，则表示不需要修改密码。
        "newPassWord": "6789"
    }
    本函数接收该信息，判断userId用户是否拥有设定权限，并按权限查询结果返回：
    {
    "status": 1, //1表示成功，0表示失败
    "errorInfo": "用户没有权限设置", //status为0时，前端展示errorinfo
    }
    """
    def entry(self, response_self):
        """response为tornado下get函数接收到前端数据后的self"""
        body = eval(response_self.request.body)
        user_id = str(body["userId"])
        user_name_want = str(body["name"])
        data = str(body["data"])

        if judgeIfPermiss(user_id = user_id, mode = 1, page = "systemUsers") == False:
            return {"status":0, "errorInfo":"用户没有权限设置", "data":{}}
        else:
            return self.updateDataToMysql(data)

    def updateDataToMysql(self, data):
        """
        前端传递来的数据
        "userId": "admin",
        "name": "用户一",
        "data": {
            "name": "用户一",
            "description": "巴拉巴拉",
            "userTeamName": "用户组一",
            "roleTeamName": "角色组一",
            "passWord": "1234",
        }
        向数据库中更新数据
        """
        data = eval(data)
        with db.execution_context():
            judge = new_users.select().where(new_users.username == data["name"]).aggregate(fn.Count(new_users.username))
        if judge == 0:
            return {"status":0, "errorInfo":"不存在该用户"}
        try:
            with db.execution_context():
                new_users.update(**{"username":data["name"], "description":data["description"], "userteamname":data["userTeamName"], "userrolename":data["roleTeamName"], "userpass":data["passWord"]}).where(new_users.username == data["name"]).execute()
        except:
            raise
            # return {"status":0, "errorInfo":"插入数据库过程中出现错误，请稍候重试"}

        return {"status":1, "errorInfo":""}
