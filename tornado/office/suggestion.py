#coding=utf8

import datetime
from judge_permission import judgeIfPermiss
from api_define import suggestion
from orm import *

class Suggestion(suggestion):

    def entry(self, response_self):
        """response为tornado下get函数接收到前端数据后的self"""
        body = eval(response_self.request.body)
        user_id = str(body["userId"])
        content = str(body["content"])
        start = str(body["start"])
        if judgeIfPermiss(user_id = user_id, mode = 1, page = "officeSuggestions") == False:
            return {"status":0, "errorInfo":"用户没有权限设置"}
        else:
            return self.insertInMysql(user_id, content, start)

    def insertInMysql(self, user_id, content, start):
        """将data中用户组信息入库"""
        """
            createDate = DateTimeField(null=True)
            info = CharField(null=True)
            start = FloatField(null=True)
            userId = CharField(null=True)
        """

        try:
            with db.execution_context():
                new_feedback.create(**{"createDate":str(datetime.datetime.now()), "info":content, "start": float(start), "userId":user_id})
        except:
            raise
            # return {"status":0, "errorInfo":"数据库新增信息失败，请稍候重试"}
        return {"status":1, "errorInfo":""}
