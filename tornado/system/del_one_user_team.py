#coding=utf8

from judge_permission import judgeIfPermiss
from api_define import del_one_user_team
from orm import *
from common.get_id_from_users_team import getIdFromUsersTeam

class DelOneUserTeam(del_one_user_team):

    def entry(self, response_self):

        body = eval(response_self.request.body)
        user_id = str(body["userId"])
        user_team_name = str(body["userTeamName"])

        if judgeIfPermiss(user_id=user_id, mode=1, page="systemUserTeam") == False:
            return {"status":0, "errorInfo":"用户没有权限设置"}
        elif len(MyBaseModel.returnList(new_user_team.select().where(new_user_team.userteamname == user_team_name).dicts())) == 0:
            return {"status":0, "errorInfo":"不存在所要删除用户组"}
        elif len(MyBaseModel.returnList(new_users.select().where(new_users.userteamname == user_team_name).dicts())) != 0:
            return {"status":0, "errorInfo":"还有用户存在于该用户组内,无法执行删除操作"}
        else:
            return self.delMysql(user_team_name)

    def delMysql(self, user_team_name):
        try:
            with db.execution_context():
                new_user_team.delete().where(new_user_team.userteamname == user_team_name).execute()
        except:
            raise
            # return {"status":0, "errorInfo":"删除过程中出错，请稍候重试"}
        return {"status":1, "errorInfo":""}
