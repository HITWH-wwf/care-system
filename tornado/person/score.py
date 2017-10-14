#coding=utf8
import pandas as pd
from judge_permission import judgeIfPermiss
from api_define import person_score
from orm import *


class PersonScore(person_score):

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
            # print(e, "PersonScore")
            raise

    def getData(self, stu_id):
        """
        {
        totalNum: 30,//查询到的该生的考试数量
        failNum: 15,//其中挂科的数量
        colName: ["课程号", "课序号", "初始成绩", "补考成绩", "考试时间", "是否重修"],
        propName: ["courseID", "courseIndex", "initialScore", "makeUpScore", "examDate", "repairOrNot"],
        data: [
            {
                courseID: "EC5444646355",//课程号
                courseIndex: "1",//课序号
                initialScore: "45.2", //初始成绩
                makeUpScore: "0",//补考成绩
                examDate: "2017-01-04 20:20:50",//考试时间
                repairOrNot: "是"//是否重修
            },
            {
                courseID: "EC5444646355",//课程号
                courseIndex: "1",//课序号
                initialScore: "45.2", //初始成绩
                makeUpScore: "0",//补考成绩
                examDate: "2017-01-04 20:20:50",//考试时间
                repairOrNot: "是"//是否重修
            }
        ]
    }
        """
        data_res = {
        "colName": ["课程号", "课序号","课程名" ,"考试成绩","考试时间","备注","学分","课程类型","考试/考察"],
        "propName": ["courseID", "courseIndex","courseName", "examScore", "examDate", "remarks","credit","courseKind","examKind"],
        "data": []
        }
        #一次获取所有的成绩数据分析并返回结果

        exam_data_temp = MyBaseModel.returnList(exam_results.select().where(exam_results.stuID ==stu_id).dicts())
        # print(exam_data_temp)
        for recode in exam_data_temp:
            if recode['remarks'] == "":
                recode['remarks'] = '无'
        exam_data = pd.DataFrame(exam_data_temp)
        if len(exam_data.index) != 0:
            exam_score = pd.Series(exam_data["examScore"].dropna().tolist())
            data_res["totalNum"] = len(exam_score.index)
            data_res["failNum"] = len(exam_score[exam_score < 60].index)
        else:
            data_res["totalNum"] = 0
            data_res["failNum"] = 0
        data_res["data"] = exam_data.fillna("").to_dict("report")
        for index,con in enumerate(data_res["data"]):
            con["examDate"] = str(pd.to_datetime(con["examDate"]).date())
            data_res["data"][index] = con
        #for index, con in enumerate(data_res["data"]):
        #    if con["makeUpScore"] == None or len(str(["makeUpScore"])) == 0:
        #        con["makeUpScore"]


        return {"status":1, "errorInfo":"", "data":data_res}
