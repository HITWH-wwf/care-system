#coding=utf8

from judge_permission import judgeIfPermiss
from api_define import get_total_user_team
from orm import *

class GetTotalUserTeam(get_total_user_team):

    def entry(self, response_self):
            
        user_id = str(eval(response_self.request.body)["userId"])

        if not (judgeIfPermiss(user_id = user_id, mode = 1, page = "systemUsers") == True or judgeIfPermiss(user_id = user_id, mode = 1, page = "systemRoleTeam") == True or judgeIfPermiss(user_id = user_id, mode = 1, page = "systemUserTeam") == True):
            return {"status":0, "errorInfo":"用户没有权限查看", "data":{}}
        
        return self.returnData(user_id)

    def returnData(self, user_id):
        """
        前端期待的返回格式：
        {
            colName: ["用户组名称", "描述"],
            propName: ["name", "description"],
            data: [
                {
                    name: "一号用户组",
                    description: "巴拉巴拉一号",
                },
                {
                    name: "二号用户组",
                    description: "巴拉巴拉二号",
                }
            ]
        }
        """
        res = MyBaseModel.returnList(new_user_team.select(new_user_team.userteamname, new_user_team.description).dicts())

        if len(res) == 0:
            return {"status":0, "errorInfo":"无用户组信息", "data":{}}
        
        data_res = {
            "colName": ["用户组名称", "描述"],
            "propName": ["name", "description"],
            "data":[]
        }

        for one_user in res:
            data_res["data"].append({"name":one_user["userteamname"], "description":one_user["description"]})
        
        return {"status":1, "errorInfo":"", "data":data_res}
