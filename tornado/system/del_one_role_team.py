#coding=utf8

from judge_permission import judgeIfPermiss
from api_define import del_one_role_team
from orm import *
from common.get_id_from_roles_team import getIdFromRoleTeam

class DelOneRoleTeam(del_one_role_team):

    def entry(self, response_self):

        body = eval(response_self.request.body)
        user_id = str(body["userId"])
        role_team_name = str(body["roleTeamName"])

        if judgeIfPermiss(user_id=user_id, mode=1, page="systemRoleTeam") == False:
            return {"status":0, "errorInfo":"用户没有权限设置"}
        elif len(MyBaseModel.returnList(new_user_role.select().where(new_user_role.userrolename == role_team_name).dicts())) == 0:
            return {"status":0, "errorInfo":"不存在所要删除的角色组"}
        elif len(MyBaseModel.returnList(new_users.select().where(new_users.userrolename == role_team_name).dicts())) != 0:
            return {"status":0, "errorInfo":"还有用户存在于该角色组内,无法删除"}
        else:
            return self.delMysql(role_team_name)

    def delMysql(self, role_team_name):
        try:
            with db.execution_context():
                new_user_role.delete().where(new_user_role.userrolename == role_team_name).execute()
        except:
            raise
            # return {"status":0, "errorInfo":"删除过程中出错，请稍候重试"}

        return {"status":1, "errorInfo":""}

