#coding=utf8

import os

from judge_permission import judgeIfPermiss
from get_id_from_users_team import getUsersTeamFromId
from get_id_from_roles_team import getRoleTeamFromId
from api_define import get_one_user
from orm import *

class GetOneUser(get_one_user):
    """
    查看一个用户的基本信息，前端发来的信息为：
    "userId":"admin",
    "userName":"用户一",
    本函数接收该信息，判断userId用户是否拥有查看权限，并按查询结果返回：
    {
    "status":1,//1表示成功，0表示失败
    "errorInfo":"用户没有权限查看",//status为0时，前端展示errorinfo
    "data":{
        "userName":"用户一",
        "description":"巴拉巴拉",
        "userTeam":"用户组一",
        "roleTeam":"角色组一"
        }
    }
    """
    def entry(self, response_self):
        """response为tornado下get函数接收到前端数据后的self"""
        body = eval(response_self.request.body)
        user_id = str(body["userId"])
        user_name_want = str(body["userName"])

        if judgeIfPermiss(user_id = user_id, mode = 1, page = "systemUsers") == False:
            return {"status":0, "errorInfo":"用户没有权限查看", "data":{}}

        return self.returnData(user_id, user_name_want)

    def returnData(self, user_id, user_name_want):
        """
        从数据库中取出信息并返回
        data: {
                name: "用户一",
                description: "巴拉巴拉",
                userTeamName: "一号用户组",
                roleTeamName: "一号角色组",
                passWord: "XXX"
            }
        """
        res = MyBaseModel.returnList(new_users.select(new_users.username, new_users.description, new_users.userteamname, new_users.userrolename, new_users.userpass).where(new_users.username == user_name_want).dicts())
        if len(res) != 1:
            return {"status":0, "errorInfo":"不存在该用户", "data":{}}
        else:
            res = eval(str(res[0]))

        return {"status":1, "errorInfo":"", "data":{"name":res["username"], "description":res["description"], "userTeamName":res["userteamname"], "roleTeamName":res["userrolename"], "passWord":res["userpass"]}}