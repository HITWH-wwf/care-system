#coding=utf8
import os
from get_total_page import getTotalPage
from judge_permission import judgeIfPermiss
from api_define import add_one_role_team
from orm import *

class AddOneRoleTeam(add_one_role_team):
    """
    添加一个用户，前端发送来的信息为：
    "userId": "admin",
    "data": {
        "name": "角色组三",
        "description": "巴拉巴拉",
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

        if judgeIfPermiss(user_id = user_id, mode = 1, page = "systemRoleTeam") == False:
            return {"status":0, "errorInfo":"用户没有权限设置"}
        else:
            return self.insertInMysql(data)

    def judgePara(self, data):
        """对前端发来的data进行校验"""
        try:
            data = eval(data)
        except:
            return False, None
        return set(data) == set({"name", "description"}), data

    def insertInMysql(self, data):
        """将data中用户组信息入库"""
        """
            userrolename = CharField(null=True)
            description = CharField()
            permission  = CharField(null=True)     #角色组权限，varchar
        """
        res, data = self.judgePara(data)
        if res == False:
            return {"status":0, "errorInfo":"返回的data不符合要求"}
        with db.execution_context():
            judge = new_user_role.select().where(new_user_role.userrolename == data["name"]).aggregate(fn.Count(new_user_role.userrolename))
        if judge != 0:
            return {"status":0, "errorInfo":"已经存在相同名称的角色组，请重新命名"}
        try:
            permission = getTotalPage(mode = 1)
            with db.execution_context():
                new_user_role.create(**{"userrolename":data["name"], "description":data["description"], "permission": str(permission)})
        except:
            raise
            # return {"status":0, "errorInfo":"数据库新增信息失败，请稍候重试"}
        return {"status":1, "errorInfo":""}
