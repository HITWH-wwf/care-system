#coding=utf8

import pandas as pd
from api_define import focus_table
from orm import *
from judge_permission import judgeIfPermiss
from get_stu_basic_data_by_user_data import getBasicDataByUserName

class FocusTable(focus_table):

    def entry(self, response_self):
        body = eval(response_self.request.body)
        user_id = str(body["userId"])
        if judgeIfPermiss(user_id = user_id, mode = 1, page = "indexStudents") == False:
            return {"status":0, "errorInfo":"用户没有权限设置"}
        else:
            return self.getData(user_id)

    def funToRecognition(self, mode, id):
        """
        获取专业和学院信息，制成字典，供导出时使用：形如：{"020":"计算机科学与技术"}
        mode = 0时，id给学院号，返回学院名
        mode = 1时，id给专业号，返回专业名
        """
        try:
            self.collegeDict
            self.specialitiesid
        except:
            #一次拿出所有的专业、学院信息，存储在字典中
            specialitiesid = pd.DataFrame(MyBaseModel.returnList(school_specialities_info.select().dicts()))
            specialitiesid.index = specialitiesid["specialitiesid"]
            self.specialitiesid = specialitiesid["specialities"].to_dict()

            collegeDict = pd.DataFrame(MyBaseModel.returnList(school_college_info.select().dicts()))
            collegeDict.index = collegeDict["collegeid"]
            self.collegeDict = collegeDict["college"].to_dict()

        if mode == 0:
            try:
                return self.collegeDict[id]
            except:
                return "没有查询到该学院名"
        elif mode == 1:
            try:
                return self.specialitiesid[id]
            except:
                return "没有查询到该专业名"
        else:
            raise Exception("error mode in funToRecognition")

    def getData(self, user_name):
        """
        返回数据给前端
        """
        # print(user_name)
        ifOk, stu_basic_data = getBasicDataByUserName(user_name)
        if ifOk == False:
            return {"status":0, "errorInfo":stu_basic_data, "data":""}
        stu_basic_dataDf=pd.DataFrame(stu_basic_data)
        stu_basic_dataDf.sort_values(['state'],ascending=False,inplace=True)
        stu_basic_data=stu_basic_dataDf.to_dict('record')
        #将专业号和学院号替换为专业名和学院名
        for index,one_user in enumerate(stu_basic_data):
            one_user["specialitiesid"] = self.funToRecognition(mode = 1, id = one_user["specialitiesid"])
            one_user["collegeid"] = self.funToRecognition(mode = 0, id = one_user["collegeid"])
            if one_user["state"] == 0:
                one_user["state"] = "正常"
            elif one_user["state"] == 1:
                one_user["state"] = "学情关注"
            elif one_user["state"] == 2:
                one_user["state"] = "推介关注"
            elif one_user["state"] == 3:
                one_user["state"] = "长期关注"
            elif one_user["state"] == 4:
                one_user["state"] = "重点关注"
            else:
                one_user["state"] = "未知状态"

            stu_basic_data[index] = one_user
        # print(len(stu_basic_data), "in the focus table")
        data_res = {
            "colName": ["姓名", "性别", "学号", "专业", "公寓", "房间号", "学籍状态", "状态"],
            "propName": ["stuName", "sex", "stuID", "specialitiesid", "apartmentNumber", "dormitoryNumber", "schoolStatus", "state"],
            "data":stu_basic_data
        }
        # print(stu_basic_data[0])
        return {"status":1, "errorInfo":"", "data":data_res}
