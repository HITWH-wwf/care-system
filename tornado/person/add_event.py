#coding=utf8

from judge_permission import judgeIfPermiss
import pandas as pd
from api_define import add_event
from orm import *

class AddEvent(add_event):

    def entry(self, response_self):
        # "stuId":"11012231",
        # "userId":"admin",
        # "theme":"记录一次谈话",
        # "time":"2017-01-01 20:20:22",
        # "content":"巴拉巴拉"
        body = eval(response_self.request.body)
        user_id = str(body['data']["userId"])
        stu_id = str(body["data"]["stuId"])
        theme = str(body["data"]["theme"])
        time = str(pd.to_datetime(body["data"]["time"]))
        content = str(body["data"]["content"])
        if judgeIfPermiss(user_id = user_id, mode = 1, page = "person") == False:
            return {"status":0, "errorInfo":"用户没有权限设置"}
        elif judgeIfPermiss(user_id = user_id, stuid = stu_id, mode = 0) == False:
            return {"status":0, "errorInfo":"用户没有权限设置"}
        else:
            return self.setData(stu_id, theme, time, content, user_id)

    def setData(self, stu_id, theme, time, content, user_id):
        """
        向数据库中插入数据
        """
        try:
            with db.execution_context():
                new_event_message.create(**{"createDate": time, "fromUserId": user_id, "messContent": content, "messTitle": theme, "stuId": stu_id})
        except:
            raise
            # return {"status":0, "errorInfo":"数据库新增信息失败，请稍候重试"}
        return {"status":1, "errorInfo":""}

