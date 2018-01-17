#coding=utf8

from judge_permission import judgeIfPermiss
from get_total_page import getTotalPage
from api_define import get_one_role_team
from orm import *

class GetOneRoleTeam(get_one_role_team):

    def entry(self, response_self):
        body = eval(response_self.request.body)
        user_id = str(body["userId"])
        role_name_want = str(body["roleTeamName"])

        if judgeIfPermiss(user_id = user_id, mode = 1, page = "systemRoleTeam") == False:
            return {"status":0, "errorInfo":"用户没有权限查看", "data":{}}
        else:
            return self.returnData(role_name_want)


    def returnData(self, role_name_want):
    
        res = MyBaseModel.returnList(new_user_role.select(new_user_role.permission).where(new_user_role.userrolename == role_name_want).dicts())

        if len(res) == 0:
            return {"status":0, "errorInfo":"无此角色组", "data":{}}
        power = eval(eval(str(res[0]))["permission"])
        pages = getTotalPage()
        for page in pages:
            if str(page) not in power:
                #应该是更新了页面
                power[str(page)] = 0
        return {"status":1, "errorInfo":"", "data":power}