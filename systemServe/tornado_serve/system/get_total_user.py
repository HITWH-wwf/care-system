#coding=utf8

from api_define import get_total_user
from orm import *
from judge_permission import judgeIfPermiss
import traceback
class GetTotalUser(get_total_user):

    def entry(self, response_self):
        
        user_id = str(eval(response_self.request.body)["userId"])
        if judgeIfPermiss(user_id = user_id, mode = 1, page = "systemUsers") == False:
            return {"status":0, "errorInfo":"用户没有权限查看", "data":{}}
        
        return self.returnData(user_id)

    def returnData(self, user_id):
        """
        前端数据返回样例
        colName: ["用户名", "描述", "所在角色组", "所在用户组", "密码"],
        propName: ["name", "description", "roleTeamName", "userTeamName", "passWord"],
        data: [
            {
                name: "王导员",
                description: "巴拉巴拉",
                roleTeamName: "一号角色组",
                userTeamName: "一号用户组",
                passWord: "XXX"
            }
        ]
        """
        #username = CharField(null=True)     #用户名，varchar
        #userpass = CharField(null=True)     #用户密码，varchar
        #description = CharField()
        #userteamname = CharField(null=True)   #该用户对应用户组名
        #userrolename = CharField(null=True)   #该用户对应角色组名
        res = MyBaseModel.returnList(new_users.select(new_users.username, new_users.description, new_users.userteamname, new_users.userrolename, new_users.userpass).dicts())

        if len(res) == 0:
            return {"status":0, "errorInfo":"无用户信息", "data":{}}
        
        data_res = {
            "colName": ["用户名", "描述", "所在角色组", "所在用户组", "密码"],
            "propName": ["name", "description", "roleTeamName", "userTeamName", "passWord"],
            "data":[]
        }

        for one_user in res:
            data_res["data"].append({"name":one_user["username"], "description":one_user["description"], "roleTeamName":one_user["userrolename"], "userTeamName":one_user["userteamname"], "passWord":one_user["userpass"]})
        
        return {"status":1, "errorInfo":"", "data":data_res}
