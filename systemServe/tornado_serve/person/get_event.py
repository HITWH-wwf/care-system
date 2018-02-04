#coding=utf8
import pandas as pd
from judge_permission import judgeIfPermiss
from api_define import get_event
from orm import *

class GetEvent(get_event):

    def entry(self, response_self):
        try:
            body = eval(response_self.request.body)
            user_id = str(body["userId"])
            stu_id = str(body["stuId"])
            if judgeIfPermiss(user_id = user_id, mode = 1, page = "person") == False:
                return {"status":0, "errorInfo":"用户没有权限设置"}
            elif judgeIfPermiss(user_id = user_id, stuid = stu_id, mode = 0) == False:
                return {"status":0, "errorInfo":"用户没有权限设置"}
            else:
                return self.getData(stu_id)
        except (Exception) as e:
            # print(e, "GetEvent")
            raise

    def getData(self, stu_id):
        """
        前端期待的返回样式
        {
            colName: [
                "时间",
                "事件主题",
                "事件内容",
                "事件记录人"
            ],
            propName: [
                "time",
                "thmeme",
                "content",
                "author"
            ],
            data: [
                {
                    time: "2017-04-04 20:55:55",
                    thmeme: "王导员的一次记录",
                    content: "今天跟XXX聊天，感觉到XXX有XXX倾向，记录下",
                    author: "admin"
                },
                {
                    time: "2017-04-07 20:55:55",
                    thmeme: "李导员的一次记录",
                    content: "今天跟XXX聊天，感觉到XXX有XXX倾向，记录下",
                    author: "admin"
                }
            ]
        }
        """
        stu_basic_data = pd.DataFrame(MyBaseModel.returnList(new_event_message.select().where(new_event_message.stuId == stu_id).dicts())).to_dict("report")
        for index, con in enumerate(stu_basic_data):
            con["createDate"] = str(pd.to_datetime(con["createDate"]))
            stu_basic_data[index] = con
        data_res = {
            "colName": ["时间", "事件主题", "事件内容", "事件记录人"],
            "propName": ["createDate", "messTitle", "messContent", "fromUserId"],
            "data":stu_basic_data
        }

        return {"status":1, "errorInfo":"", "data":data_res}

