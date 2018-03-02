#coding=utf8

import sys
import datetime
sys.path.append("..")

from judge_permission import judgeIfPermiss

from api_define import add_focus
from orm import *

class AddFocus(add_focus):

    def entry(self, response_self):
        body = eval(response_self.request.body)
        user_id = str(body["data"]["userId"])
        stu_id = str(body["data"]["stuId"])
        level = str(body["data"]["focusLevel"])
        reason = str(body["data"]["reson"])
        # sleepInOrOut = str(body["data"]["sleepInOrOut"])
        # studyWithParent = str(body["data"]["studyWithParent"])

        if judgeIfPermiss(user_id = user_id, mode = 1, page = "person") == False:
            return {"status":0, "errorInfo":"用户没有页面设置权限"}
        elif judgeIfPermiss(user_id = user_id, stuid = stu_id, mode = 0) == False:
            return {"status":0, "errorInfo":"用户没有用户组权限设置"}
        else:
            return self.setData(stu_id, reason, level)

    def setData(self, stu_id, reason, level):
        """
        向数据库中插入数据
        """
        try:
            with db.execution_context():
                stu_focus.create(**{"stuID": stu_id,"style":1, "reason": reason, "level": int(level), "createDate": str(datetime.datetime.now())})

                # if level == '2':
                #     newstate=2
                # elif level == '1':
                #     newstate=1

                newstate=int(level)
                stu=stu_basic_info.select().where(stu_basic_info.stuID == stu_id).get()
                stu.state=newstate
                stu.save()
        except:
            raise
            # return {"status":0, "errorInfo":"数据库新增信息失败，请稍候重试"}
        return {"status":1, "errorInfo":""}
