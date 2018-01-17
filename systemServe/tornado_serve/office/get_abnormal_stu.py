#coding=utf8

from api_define import get_abnormal_stu,myurl
import pandas as pd
from orm import *
import requests
import time
from datetime import datetime,timedelta
from common.get_stu_basic_data_by_user_data import getBasicDataByUserName

class GetAbnormalStu(get_abnormal_stu):
    def entry(self,response_self):
        try:
            body = eval(response_self.request.body)
            maxmoney = str(body["card"]['consume'])
            moneydays = str(body['card']["number"])
            sleepdays = str(body['days'])
            sbjNumber=str(body['sbjNumber'])
            username=str(body['userId'])
            isflag,canseeid=getBasicDataByUserName(username)
            assert isflag==True

            if moneydays == '':
                moneydays = 0
            if sleepdays == '':
                sleepdays = 0
            if maxmoney=='':
                maxmoney=0
            if sbjNumber=='':
                sbjNumber=0

            allStuId=[]
            for stu in canseeid:
                singlestu={"specialitiesid":stu['specialitiesid'],"collegeid":stu['collegeid'],
                "state":stu['state'],"stuID":stu['stuID'],"stuName":stu['stuName'],"sex":stu['sex']}
                allStuId.append(singlestu)
            allStuId=str(allStuId)

            day = timedelta(days=1)
            enddate=datetime.today().date()
            startdate=(datetime.today()-day*364).date()
            request_data = {'startdate':str(startdate) , 'enddate':str(enddate), 'sleepdays': sleepdays,
                            'moneydays': moneydays, 'failnum':sbjNumber,'maxmoney': maxmoney,'allstuid':allStuId}

            r = requests.post(url=myurl, data=request_data)
            result = eval(r.text)
            if result['status'] == 1:
                abnormalStu=self.getData(result['data'])
                return abnormalStu
            else:
                return {"status": 0, "errorInfo": "操作失败", "data": ''}
        except (Exception) as e:
            raise e
            # return {"status": 0, "errorInfo": "操作失败", "data": ''}

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
            # 一次拿出所有的专业、学院信息，存储在字典中
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

    def getData(self, abnormalStus):
        """
        返回数据给前端
        """

        # ifOk, stu_basic_data = getBasicDataByUserName(user_name)
        # if ifOk == False:
        #     return {"status":0, "errorInfo":stu_basic_data, "data":""}

        # 将专业号和学院号替换为专业名和学院名
        stu_basic_data = []
        for one_user in abnormalStus:
            one_user["specialitiesid"] = self.funToRecognition(mode=1, id=one_user["specialitiesid"])
            one_user["collegeid"] = self.funToRecognition(mode=0, id=one_user["collegeid"])
            if one_user["state"] == 0:
                one_user["state"] = "正常"
            elif one_user["state"] == 1:
                one_user["state"] = "推介关注"
            elif one_user["state"] == 2:
                one_user["state"] = "重点关注"
            elif one_user["state"] == 3:
                one_user["state"] = "毕业"
            else:
                one_user["state"] = "未知状态"
            stu_basic_data.append(one_user)

        data_res = {
            "colName": ["学号","姓名", "性别", "专业", "状态"],
            "propName": ["stuID","stuName", "sex", "stuID", "specialitiesid", "state"],
            "data": stu_basic_data
        }
        return {"status": 1, "errorInfo": "", "data": data_res}

