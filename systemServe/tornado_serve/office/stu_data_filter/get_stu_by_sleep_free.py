from tornado_serve.orm import *
from tornado_serve.common.get_class_or_stu_by_user import getClassOrStuByUser
import pandas as pd
from datetime import datetime
from tornado_serve.office.stu_data_filter.return_model import sleepModel
from tornado_serve.common.deal_dateortime_func import strDateTimeChangeToInt,getBeforeDateTime
class GetStuBySleepFree():
    def entry(self,receiveRequest):
        self.requestData = eval(receiveRequest.request.body)
        # self.requestData=receiveRequest
        stuRange = self.requestData['stuRange']
        dateRange=self.requestData['dateRange']
        appearTimes=self.requestData['appearTimes']
        if dateRange=='threeMonth':
            dateRange={}
            start=getBeforeDateTime(93)
            dateRange['startDate']=str(start.date())
            dateRange['endDate']=str(datetime.today().date())
        self.sleepCountResult=None
        self.selectStuIds=None
        self.inRoleStuDf=None                   #stuRange['rangeData']
        stuFlag = self.getStuResultBystuRange(stuRange['rangeKind'],stuRange['rangeData'])
        if stuFlag['status'] == 0:
            return stuFlag
        return self.getStuResultByCondition(self.requestData['returnKind'],self.requestData['countKind'],
                    dateRange['startDate'],dateRange['endDate'],appearTimes['minTimes'],appearTimes['maxTimes'])



    def getStuResultBystuRange(self,rangeKind,rangeData):

        if rangeKind=='useClassId':
            inRoleStu = getClassOrStuByUser(self.requestData['userId'], 1,rangeData)
            self.inRoleStuDf = pd.DataFrame(inRoleStu)
            self.selectStuIds = list(self.inRoleStuDf['stuID'])
        else:
            inRoleStu = getClassOrStuByUser(self.requestData['userId'], 1)
            self.inRoleStuDf = pd.DataFrame(inRoleStu)
            if rangeKind=='useStuId':
                if len(self.inRoleStuDf[self.inRoleStuDf['stuID'] == rangeData]) > 0:
                    self.selectStuIds=[rangeData]
                else:
                    return {'status': 0, 'errorInfo': '该学生不存在或您无权限查看'}
            else:
                self.selectStuIds = list(self.inRoleStuDf[self.inRoleStuDf['stuName'] == rangeData]['stuID'])
                if len(self.selectStuIds)==0:
                    return {'status': 0, 'errorInfo': '该学生不存在或您无权限查看'}
        self.sleepCountResult=pd.DataFrame(MyBaseModel.returnList(stu_sleep_count.select(stu_sleep_count.stuID,stu_sleep_count.freeQueryCountInfo).where(
                            stu_sleep_count.stuID.in_(self.selectStuIds))))
        self.sleepCountResult.dropna(axis=1, inplace=True)
        self.sleepCountResult.index = self.sleepCountResult['stuID']
        self.sleepCountResult = self.sleepCountResult['freeQueryCountInfo'].to_dict()
        for key in self.sleepCountResult.keys():
            self.sleepCountResult[key] = eval(self.sleepCountResult[key])   #{学号：全部记录,....}

        return {'status': 1}

    def getStuResultByCondition(self,returnKind,countKind,startDate,endDate,minTimes,maxTimes):
        startDate=strDateTimeChangeToInt(startDate)
        endDate=strDateTimeChangeToInt(endDate)
        resultStu={}
        recordIdList = []
        for stu in self.selectStuIds:
            stuCountDf=pd.DataFrame(self.sleepCountResult[stu])
            stuCountDf=stuCountDf[(stuCountDf['today']>=startDate)&(stuCountDf['today']<=endDate)]
            times=sum(stuCountDf[countKind])
            if times>=minTimes and times<=maxTimes:
                if returnKind=='stuRecord':
                    recordList=list(stuCountDf[stuCountDf[countKind]==1]['inMaxId'])
                    recordIdList=recordIdList+recordList
                    recordList = list(stuCountDf[stuCountDf[countKind] == 1]['outMaxId'])
                    recordIdList=recordIdList+recordList
                    resultStu[stu]=times
                else:
                    resultStu[stu] = times
        recordIdList=[x for x in recordIdList if x!='' and x>=0]
        self.inRoleStuDf.index = self.inRoleStuDf['stuID']
        stuBasicInfo = self.inRoleStuDf.to_dict('index')
        if returnKind== 'stuList':
            resultData=[]
            for stu in resultStu.keys():
                oneStu=stuBasicInfo[stu]
                oneStu['times']=int(resultStu[stu])
                resultData.append(oneStu)
        else:
            if len(recordIdList)==0:
                return sleepModel(returnKind, countKind, [])
            recordIdList=set(recordIdList)
            stuSleepRecord=pd.DataFrame(MyBaseModel.returnList(entry_and_exit.select().where(entry_and_exit.id.in_(recordIdList)).group_by(entry_and_exit.stuID,entry_and_exit.id).order_by(
                entry_and_exit.stuID.asc(), entry_and_exit.id.asc()
            )
            ))
            stuSleepRecord=stuSleepRecord.fillna({'entryDate':'无记录','exitDate':'无记录'})
            stuSleepRecord['entryDate']=stuSleepRecord['entryDate'].astype('str')
            stuSleepRecord['exitDate'] = stuSleepRecord['exitDate'].astype('str')
            resultData=[]
            stuSleepRecord['stuName']='未记录'
            for stu in resultStu.keys():
                stuSleepRecord.loc[stuSleepRecord[stuSleepRecord['stuID']==stu].index,('stuName')]=stuBasicInfo[stu]['stuName']
                # oneStu=stuSleepRecord[stuSleepRecord['stuID']==stu]
                # oneStu['stuName']=stuBasicInfo[stu]['stuName']
                    # stuBasicInfo[stu]['stuName']
            resultData=stuSleepRecord.to_dict("report")

        return sleepModel(returnKind,countKind,resultData)





