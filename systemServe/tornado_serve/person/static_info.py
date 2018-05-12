#coding=utf8

import pandas as pd
from api_define import static_info
from orm import *
from judge_permission import judgeIfPermiss

class StaticInfo(static_info):

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
            # print(e, "StaticInfo")
            raise


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

    def getData(self, stu_id):
        """
        basicInfo: {
            colName: ["学号", "班号", "姓名", "性别", "民族", "政治面貌", "学历", "身份证号", "公寓号", "宿舍号", "毕业高中", "手机号", "家庭地址", "父亲姓名", "父亲工作单位", "父亲手机号", "母亲姓名", "母亲工作单位", "母亲手机号"],
            propName: ["stuID", "stuClassNumber", "stuName", "sex", "nationality", "politicalLandscape", "stuEducation", "idNumber", "apartmentNumber", "dormitoryNumber", "graduatedHighSchool", "stuMobileNumber", "homeAddress", "fatherName", "fatherWorkUnit", "fatherMobileNumber", "motherName", "motherWorkUnit", "motherMobileNumber"],
            data: {
                stuID: "110410120",
                stuClassNumber: "1104101",
                stuName: "张三",
                sex: "男",
                nationality: "汉族",
                politicalLandscape: "党员",
                stuEducation: "本科",
                idNumber: "610112411512210598",
                apartmentNumber: "6",
                dormitoryNumber: "404",
                graduatedHighSchool: "XX高中",
                stuMobileNumber: "18363120012",
                homeAddress: "XX省XX市场",
                fatherName: "张三爸",
                fatherWorkUnit: "XX工作单位",
                fatherMobileNumber: "18363120013",
                motherName: "张三妈",
                motherWorkUnit: "XX工作单位",
                motherMobileNumber: "18363120014"
            }
        },
        focusInfo: {
            focusReason: "延期毕业",
            focusLevel: "推介关注"//当为正常或者毕业时，Reason为空
        }
        """

        stu_basic_data = pd.DataFrame(MyBaseModel.returnList(stu_basic_info.select().where(stu_basic_info.stuID == stu_id).dicts())).to_dict("report")
        if len(stu_basic_data) == 0:
            return {"status":0, "errorInfo":"没有在数据库中找到该学生的数据", "data":""}

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
            elif one_user["state"]==4 :
                one_user["state"] = "重点关注"
            else:
                one_user["state"] = "未知状态"

            stu_basic_data[index] = one_user

        data_res = {
            "colName": ["学号", "班号", "姓名", "性别", "民族", "政治面貌", "学历", "身份证号", "公寓号", "宿舍号", "毕业高中", "手机号", "家庭地址", "父亲姓名", "父亲工作单位", "父亲手机号", "母亲姓名", "母亲工作单位", "母亲手机号","学籍状态","校外住宿","家长陪读","转专业","转入专业","降级"],
            "propName": ["stuID", "stuClassNumber", "stuName", "sex", "nationality", "politicalLandscape", "stuEducation", "idNumber", "apartmentNumber", "dormitoryNumber", "graduatedHighSchool", "stuMobileNumber", "homeAddress", "fatherName", "fatherWorkUnit", "fatherMobileNumber", "motherName", "motherWorkUnit", "motherMobileNumber","schoolStatus"
                         ,"sleepInOrOut","studyWithParent","turnProfessional","turnInProfessional","downgrade"],
            "data":stu_basic_data[0]
        }
        if stu_basic_data[0]['state'] == '正常':
            focusInfo = {"focusReason":"无", "focusLevel":stu_basic_data[0]['state'] }
        else:
            try:
                focusReason = MyBaseModel.returnList(stu_focus.select(stu_focus.reason).where(stu_focus.stuID == stu_id).dicts(), key = "reason")[0]
            except:
                focusReason = ""
            focusInfo = {"focusReason":focusReason, "focusLevel":stu_basic_data[0]['state'] }
        return {"status":1, "errorInfo":"", "basicInfo":data_res, "focusInfo":focusInfo}
