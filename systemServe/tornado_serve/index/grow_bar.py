#coding=utf8

import pandas as pd
from judge_permission import judgeIfPermiss
from api_define import grow_bar
from orm import *
from logConfig import logger

class GrowBar(grow_bar):

    def entry(self, response_self):

        body = eval(response_self.request.body)
        user_id = str(body["userId"])
        if judgeIfPermiss(user_id = user_id, mode = 1, page = "indexMajor") == False:
            return {"status":0, "errorInfo":"用户没有权限设置"}
        else:
            return self.getData(user_id)

    def funToRecognition(self, mode, id):
        """
        获取专业和学院信息，制成字典，供导出时使用：形如：{"020":"计算机科学与技术"}
        mode = 0时，id给学院号，返回学院名
        mode = 1时，id给专业号，返回专业名
        mode = 2时，id给学号，返回关注该学生的年月，格式为:2017-01
        """
        try:
            self.collegeDict
            self.specialitiesidDict
            self.stuFocusDict
        except:
            #一次拿出所有的专业、学院信息，存储在字典中
            specialitiesid = pd.DataFrame(MyBaseModel.returnList(school_specialities_info.select().dicts()))
            specialitiesid.index = specialitiesid["specialitiesid"]
            self.specialitiesidDict = specialitiesid["specialities"].to_dict()

            collegeDict = pd.DataFrame(MyBaseModel.returnList(school_college_info.select().dicts()))
            collegeDict.index = collegeDict["collegeid"]
            self.collegeDict = collegeDict["college"].to_dict()

            stuFocusDict = pd.DataFrame(MyBaseModel.returnList(stu_focus.select().dicts()))
            if len(stuFocusDict.index) == 0:
                self.stuFocusDict = {}
            else:
                stuFocusDict.index = stuFocusDict['stuID']
                self.stuFocusDict = stuFocusDict["createDate"].to_dict()

        if mode == 0:
            try:
                return self.collegeDict[id], True
            except:
                return "没有查询到该学院名", False
        elif mode == 1:
            try:
                return self.specialitiesidDict[id], True
            except:
                return "没有查询到该专业名", False
        elif mode == 2:
            try:
                return str(pd.to_datetime(self.stuFocusDict[id]).date())[0:-3], True
            except:
                return "没有查询到该学生的被关注时间", False
        else:
            raise Exception("error mode in funToRecognition")

    def getData(self, user_name):
        """
        返回数据给前端
        """
        #一次获取所有state非0和3的学生,即：把除去正常和毕业的都拿出来
        stu_basic_data = pd.DataFrame(MyBaseModel.returnList(stu_basic_info.select(stu_basic_info.stuID,
        stu_basic_info.specialitiesid, stu_basic_info.collegeid, stu_basic_info.state, stu_basic_info.grade
        ).where(stu_basic_info.state != 0, stu_basic_info.state != 3).dicts())).to_dict("report")
        ifOk = False
        #将专业号和学院号替换为专业名和学院名，状态转化为文字，并加上转为非正常状态的时间
        for index,one_user in enumerate(stu_basic_data):
            try:
                one_user["collegeid"], ifOk = self.funToRecognition(mode = 0, id = one_user["collegeid"])
                if ifOk == False:
                    continue
                one_user["focusDate"], ifOk = self.funToRecognition(mode = 2, id = one_user["stuID"])
                if ifOk == False:
                    continue
                stu_basic_data[index] = one_user
            except:
                logger.warning(one_user['stuID'], "GrowBarfail")

        res = {}
        data_pd = pd.DataFrame(stu_basic_data)
        data_pd['grade'] = data_pd['grade'].astype(str)
        #先拿到所有学生grade（年级）的集合
        grade_list = MyBaseModel.returnList(stu_basic_info.select(stu_basic_info.grade).distinct(stu_basic_info.grade).dicts(), key = "grade")
        res["date"] = list(data_pd.groupby(by = ["focusDate"]).count().index)
        college_data = data_pd.groupby(by=["focusDate", "grade"])["stuID"].count().unstack().fillna(0).to_dict("list")
        res = dict(res, **college_data)
        #补充其他可能不存在需要关注学生的学院信息
        for grade_name in grade_list:
            if str(grade_name) not in res:
                res[str(grade_name)] = [0] * len(res["date"])
        return {"status":1, "errorInfo":"", "data":res}
