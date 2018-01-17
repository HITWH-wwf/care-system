#coding=utf8

from judge_permission import judgeIfPermiss
from get_total_class import getTotalClass
from api_define import set_one_user_team
from orm import *

class SetOneUserTeam(set_one_user_team):
    """
    设置一个用户组：
    "userId":"admin",
    "userTeamName":"一号用户组",
    "data":{
        //0表示未勾选，1表示勾选
        "1101401":"0",
        "1101141":"1",
        "1101142":"1",
        "1101143":"1",
        "1101144":"0",
        "1101145":"1",
        "1101146":"1",
        "1101147":"1",
        "1101148":"0",
        "1101149":"0",
    }
    本函数接收该信息，判断userId用户是否拥有该权限并根据结果将其修改入库，返回：
    {
    "status":1,//1表示成功，0表示失败
    "errorInfo":"该用户没有权限"//status为0时，前端展示errorinfo
    }
    """
    def entry(self, response_self):

        body = eval(response_self.request.body)
        user_id = str(body["userId"])
        user_team_name = str(body["userTeamName"])
        data = eval(str(body["data"]))

        if judgeIfPermiss(user_id=user_id, mode=1, page="systemUserTeam") == False:
            return {"status":0, "errorInfo":"用户没有权限设置"}
        elif len(MyBaseModel.returnList(new_user_team.select().where(new_user_team.userteamname == user_team_name).dicts())) == 0:
            return {"status":0, "errorInfo":"不存在所要设置的用户组"}
        else:
            return self.updateMysql(user_team_name, data)

    def updateMysql(self, user_team_name, data):
        """更改数据库内的数据"""

        if not set(data) == set(getTotalClass()):
            return {"status":0, "errorInfo":"设置的用户组项与系统当前不符"}
        try:
            with db.execution_context():
                new_user_team.update(**{"permission":str(data)}).where(new_user_team.userteamname == user_team_name).execute()
        except:
            raise
            # return {"status":0, "errorInfo":"更新数据库过程中出错，请稍候重试"}
        return {"status":1, "errorInfo":""}
