#coding=utf8

from api_define import get_total_role_team
from orm import *
from judge_permission import judgeIfPermiss

class GetTotalRoleTeam(get_total_role_team):

    def entry(self, response_self):
        
        user_id = str(eval(response_self.request.body)["userId"])

        if not (judgeIfPermiss(user_id = user_id, mode = 1, page = "systemUsers") == True or judgeIfPermiss(user_id = user_id, mode = 1, page = "systemRoleTeam") == True or judgeIfPermiss(user_id = user_id, mode = 1, page = "systemUserTeam") == True):
            return {"status":0, "errorInfo":"用户没有权限查看", "data":{}}
        
        return self.returnData(user_id)

    def returnData(self, user_id):
        """
        前端期待的返回形式：
            {
            colName: ["角色组名称", "描述"],
            propName: ["name", "description"],
            data: [
                {
                    "name": "一号角色组",
                    "description": "巴拉巴拉",
                },
                {
                    "name": "二号角色组",
                    "description": "巴拉巴拉",
                }
            ]
        }
        """
        res = MyBaseModel.returnList(new_user_role.select(new_user_role.userrolename, new_user_role.description).dicts())

        if len(res) == 0:
            return {"status":0, "errorInfo":"无角色组信息", "data":{}}
        
        data_res = {
            "colName": ["角色组名称", "描述"],
            "propName": ["name", "description"],
            "data":[]
        }
        for one_role in res:
            data_res["data"].append({"name":one_role["userrolename"], "description":one_role["description"]})
        
        return {"status":1, "errorInfo":"", "data":data_res}