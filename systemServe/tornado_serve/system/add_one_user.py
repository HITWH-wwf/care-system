#coding=utf8
from judge_permission import judgeIfPermiss
from get_id_from_users_team import getIdFromUsersTeam
from get_id_from_roles_team import getIdFromRoleTeam
from api_define import add_one_user
from orm import *

class AddOneUser(add_one_user):
    """
    添加一个用户，前端发送来的信息为：
    "userId": "admin",
    "data": {
        "name": "用户三",
        "description": "巴拉巴拉",
        "userTeamName": "用户组一",
        "roleTeamName": "角色组一",
        "passWord": "1234",
    }
    本函数接收该信息，判断userId用户是否拥有该权限并根据结果将其添加入库，返回：
    {
    "status": 1, #1表示成功，0表示失败
    "errorInfo": "用户没有权限设置", #status为0时，前端展示errorinfo
    }
    """
    def entry(self, response_self):
        """response为tornado下get函数接收到前端数据后的self"""
        body = eval(response_self.request.body)
        user_id = str(body["userId"])
        data = str(body["data"])
        if not (judgeIfPermiss(user_id = user_id, mode = 1, page = "systemUsers") == True or judgeIfPermiss(user_id = user_id, mode = 1, page = "systemRoleTeam") == True or judgeIfPermiss(user_id = user_id, mode = 1, page = "systemUserTeam") == True):
            return {"status":0, "errorInfo":"用户没有权限查看", "data":{}}

        return self.insertInMysql(data)

    def judgePara(self, data):
        """对前端发来的data进行校验"""
        try:
            data = eval(data)
        except:
            return False, None

        return set(data) == set({"name", "description", "userTeamName", "roleTeamName", "passWord"}), data

    def insertInMysql(self, data):
        """将data中用户信息入库"""
        """
            username = CharField(null=True)     #用户名，varchar
            userpass = CharField(null=True)     #用户密码，varchar
            description = CharField()
            userteamname = CharField(null=True)   #该用户对应用户组名
            userrolename = CharField(null=True)   #该用户对应角色组名
        """
        res, data = self.judgePara(data)
        if res == False:
            return {"status":0, "errorInfo":"返回的data不符合要求"}
        with db.execution_context():
            judge = new_users.select().where(new_users.username == data["name"]).aggregate(fn.Count(new_users.username))
        if judge != 0:
            return {"status":0, "errorInfo":"已经存在相同用户名的用户，请重新命名"}
        try:
            with db.execution_context():
                new_users.create(**{"username":data["name"], "userpass":data["passWord"], "description":data["description"], "userteamname":data["userTeamName"], "userrolename":data["roleTeamName"]})
        except:
            raise
            # return {"status":0, "errorInfo":"数据库新增信息失败，请稍候重试"}
        return {"status":1, "errorInfo":""}
