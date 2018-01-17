#coding=utf8

from judge_permission import judgeIfPermiss
from api_define import get_one_user_team
from orm import *
from common.get_team import getTeam
from get_total_class import getTotalClass
class GetOneUserTeam(get_one_user_team):

    def entry(self, response_self):
        body = eval(response_self.request.body)
        user_id = str(body["userId"])
        user_name_want = str(body["userTeamName"])

        if judgeIfPermiss(user_id = user_id, mode = 1, page = "systemUserTeam") == False:
            return {"status":0, "errorInfo":"用户没有权限查看",  "classNum":[], "ifCheck":[]}
        else:
            return self.returnData(user_name_want)

    
    def returnData(self, user_name_want):
        """
        前端期待的反馈
        data: {
            "1101401": "1",
            "1101141": "1",
            "1101142": "1",
            "1101143": "1",
            "1101144": "1",
            "1101145": "1",
            "1101146": "1",
            "1101147": "1",
            "1101148": "1",
            "1101149": "0",
        }
        """
        res = MyBaseModel.returnList(new_user_team.select(new_user_team.permission).where(new_user_team.userteamname == user_name_want).dicts())

        if len(res) == 0:
            return {"status":0, "errorInfo":"无此用户组",  "data":{}}
        power = eval(eval(str(res[0]))["permission"])
        classs = getTotalClass()
        for mclass in classs:
            if str(mclass) not in power:
                #应该是更新了班级数据
                power[str(mclass)] = 0
        for mclass in list(power):
            if mclass not in classs:
                power.pop(mclass)
        return {"status":1, "errorInfo":"", "data":power}