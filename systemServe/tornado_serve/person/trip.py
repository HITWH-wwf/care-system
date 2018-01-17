#coding=utf8

import pandas as pd
import datetime
from api_define import person_trip
from orm import *
from judge_permission import judgeIfPermiss

class PersonTrip(person_trip):

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
            # print(e, "PersonTrip")
            raise

    def getData(self, stu_id):
        """
        totalNum: 30,
        failNum: 10,
        normolWord: "正常时间归寝",
        unNormolWord: "晚于23点归寝",
        colName: [
            "通过公寓号",
            "离开时间",
            "进入时间"
        ],
        propName: [
            "department",
            "exitTime",
            "entryTime"
        ],
        data: [
            {
                department: "2#",
                exitTime: "2017-01-01 20:33:45",
                entryTime: "2017-01-01 20:00:00"
            },
            {
                department: "2#",
                exitTime: "2017-01-01 20:33:45",
                entryTime: "2017-01-01 20:00:00"
            },
            {
                department: "2#",
                exitTime: "2017-01-01 20:33:45",
                entryTime: "2017-01-01 20:00:00"
            }
        ]
        """
        data_res = {
            "totalNum": 0,
            "failNum": 0,
            "normolWord": "正常时间归寝",
            "unNormolWord": "晚于23点归寝",
            "colName": [
                "通过公寓号",
                "离开时间",
                "进入时间"
            ],
            "propName": [
                "apartmentNumber",
                "exitDate",
                "entryDate"
            ],
            "data": []
        }
        #获取近7天的所有数据
        with db.execution_context():
            max_date = entry_and_exit.select(entry_and_exit.entryDate).where(entry_and_exit.stuID == stu_id).aggregate(fn.Max(entry_and_exit.entryDate))
        if max_date == None:
            return {"status":0, "errorInfo":"没有数据", "data": data_res}
        the_time = str((pd.to_datetime(max_date) - datetime.timedelta(days = 179)))

        data_pd = pd.DataFrame(MyBaseModel.returnList(entry_and_exit.select(entry_and_exit.apartmentNumber, entry_and_exit.exitDate, entry_and_exit.entryDate).where(entry_and_exit.stuID == stu_id, entry_and_exit.entryDate >= the_time).dicts()))

        #找出在23点后，3点前归寝的
        totalNum = len(data_pd["entryDate"].dropna().index)
        hour_list = data_pd["entryDate"].dropna().apply(lambda x: x.hour)
        failNum = len(data_pd[((hour_list >= 23)&(hour_list <= 24))|((hour_list >= 0)&(hour_list <= 3))].index)
        data_res["totalNum"] = totalNum
        data_res["failNum"] = failNum

        def funToStr(x):
            """
            将可能含有np.nan字样的日期列，转成字符串形式
            """
            if pd.isnull(x):
                return ""
            else:
                return str(pd.to_datetime(x))

        data_pd['entryDate'] = data_pd['entryDate'].apply(funToStr)
        data_pd['exitDate'] = data_pd['exitDate'].apply(funToStr)
        data_res["data"] = data_pd.to_dict("report")

        return {"status":1, "errorInfo":"", "data": data_res}
