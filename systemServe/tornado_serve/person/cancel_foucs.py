#coding=utf8

import sys
sys.path.append("..")

from judge_permission import judgeIfPermiss

from api_define import cancel_focus
from orm import *

class CancelFocus(cancel_focus):

    def entry(self, response_self):
        # "stuId":"11012231",
        # "userId":"admin",
        body = eval(response_self.request.body)
        user_id = str(body["data"]["userId"])
        stu_id = str(body["data"]["stuId"])
        if judgeIfPermiss(user_id = user_id, mode = 1, page = "person") == False:
            return {"status":0, "errorInfo":"该用户没有权限设置"}
        elif judgeIfPermiss(user_id = user_id, stuid = stu_id, mode = 0) == False:
            return {"status":0, "errorInfo":"用户没有操作该学生的权限"}
        else:
            return self.setData(stu_id)

    def setData(self, stu_id):
        """
        向数据库中插入数据
        """
        try:
            with db.execution_context():
                data = {"state": 0,'focusColor':'blue'}
                stu_focus.delete().where(stu_focus.stuID == stu_id).execute()
                stu_basic_info.update(**data).where(stu_basic_info.stuID == stu_id).execute()
        except:
            raise
            # return {"status":0, "errorInfo":"数据库新增信息失败，请稍候重试"}
        return {"status":1, "errorInfo":""}
