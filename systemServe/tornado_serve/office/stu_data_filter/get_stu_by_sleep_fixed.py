from tornado_serve.orm import *
from tornado_serve.common.get_class_or_stu_by_user import getClassOrStuByUser
import pandas as pd
from tornado_serve.office.stu_data_filter.return_model import sleepModel
from tornado_serve.common.deal_dateortime_func import intChangeToDateStr
from tornado_serve.common.deal_data_by_redis import getValue
class GetStuBySleepFixed():
    def entry(self,receiveRequest):
        self.requestData = eval(receiveRequest.request.body)
        # self.requestData = receiveRequest
        self.resultDf = None
        self.appearDateDict = {}
        userName=getValue(self.requestData['sessionId'])
        if userName==None:
            return {'status':0,'errorInfo':'登陆状态已过期，请重新登录'}

        inRoleStu = getClassOrStuByUser(self.requestData['userId'], 1)
        self.inRoleStuDf = pd.DataFrame(inRoleStu)
        self.selectStuIds = list(self.inRoleStuDf['stuID'])
        self.sleepCountResult = pd.DataFrame(MyBaseModel.returnList(
            stu_sleep_count.select(stu_sleep_count.stuID, stu_sleep_count.fixedQueryCountInfo).where(
                stu_sleep_count.stuID.in_(self.selectStuIds))))

        self.sleepCountResult.dropna(axis=1, inplace=True)
        self.sleepCountResult.index = self.sleepCountResult['stuID']
        self.sleepCountResult = self.sleepCountResult['fixedQueryCountInfo'].to_dict()
        for key in self.sleepCountResult.keys():
            self.sleepCountResult[key] = eval(self.sleepCountResult[key])  # {学号：全部记录,....}

        return self.getStuResultByCondition(self.requestData['returnKind'],self.requestData['queryKind'])

    def getStuResultByCondition(self,returnKind,queryKind):
        resultStu={}
        recordIdList = []
        for stu in self.selectStuIds:
            stuCountDf=pd.DataFrame(self.sleepCountResult[stu])
            stuCountDf=stuCountDf[stuCountDf[queryKind]==1]
            times=sum(stuCountDf[queryKind])
            if len(stuCountDf)==0:
                continue
            if returnKind=='stuRecord':
                if queryKind=='fixed1':
                    recordList=list(stuCountDf['inMaxId1'])
                    recordIdList=recordIdList+recordList
                    recordList = list(stuCountDf['outMaxId1'])
                    recordIdList=recordIdList+recordList
                    resultStu[stu]=times
                elif queryKind=='fixed3':
                    recordList = list(stuCountDf['inMaxId3'])
                    recordIdList = recordIdList + recordList
                    recordList = list(stuCountDf['outMaxId3'])
                    recordIdList = recordIdList + recordList
                    resultStu[stu] = times
                else:
                    resultStu[stu] = times
                    appearDateList=list(stuCountDf['today'])
                    self.appearDateDict[stu]=[intChangeToDateStr(x) for x in appearDateList]
            else:
                resultStu[stu] = times

        recordIdList=[x for x in recordIdList if x!='' and x>=0]
        recordIdList=set(recordIdList)
        self.inRoleStuDf.index = self.inRoleStuDf['stuID']
        stuBasicInfo = self.inRoleStuDf.to_dict('index')
        if returnKind=='stuList':
            resultData = []
            for stu in resultStu.keys():
                oneStu = stuBasicInfo[stu]
                oneStu['times'] = resultStu[stu]
                resultData.append(oneStu)
        else:
            if queryKind=='fixed2':
                resultData=[]
                for stu in resultStu.keys():
                    for oneDay in self.appearDateDict[stu]:
                        oneRecord = stuBasicInfo[stu].copy()
                        oneRecord['happenDate']=oneDay
                        resultData.append(oneRecord)
            else:
                if len(recordIdList) == 0:
                    return sleepModel(returnKind, queryKind, [])
                recordIdList=set(recordIdList)
                stuSleepRecord = pd.DataFrame(MyBaseModel.returnList(
                    entry_and_exit.select().where(entry_and_exit.id.in_(recordIdList)).group_by(entry_and_exit.stuID,
                    entry_and_exit.id).order_by(entry_and_exit.stuID.asc(), entry_and_exit.id.asc())))
                stuSleepRecord = stuSleepRecord.fillna({'entryDate': '无记录', 'exitDate': '无记录'})
                stuSleepRecord['entryDate'] = stuSleepRecord['entryDate'].astype('str')
                stuSleepRecord['exitDate'] = stuSleepRecord['exitDate'].astype('str')
                stuSleepRecord['stuName'] = '未记录'
                for stu in resultStu.keys():
                    stuSleepRecord.loc[stuSleepRecord[stuSleepRecord['stuID'] == stu].index, ('stuName')] = stuBasicInfo[stu]['stuName']
                    # oneStu=stuSleepRecord[stuSleepRecord['stuID']==stu]
                    # oneStu['stuName']=stuBasicInfo[stu]['stuName']
                    # stuBasicInfo[stu]['stuName']
                stuSleepRecord.drop(['id'],axis=1,inplace=True)
                resultData = stuSleepRecord.to_dict("report")
        return sleepModel(returnKind, queryKind, resultData)
