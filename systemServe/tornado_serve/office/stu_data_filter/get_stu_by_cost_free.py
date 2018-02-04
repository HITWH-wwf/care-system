from tornado_serve.common.get_class_or_stu_by_user import getClassOrStuByUser
from tornado_serve.office.stu_data_filter.return_model import costModel
from tornado_serve.common.deal_dateortime_func import strDateTimeChangeToInt,intChangeToDateStr,getBeforeDateTime
from tornado_serve.orm import *
from datetime import datetime
import pandas as pd
import numpy as np

class GetStuByCostFree():
    def entry(self,receiveRequest):
        # self.requestData=receiveRequest
        self.requestData = eval(receiveRequest.request.body)
        stuRange = self.requestData['stuRange']

        dateRange = self.requestData['dateRange']
        if dateRange=='threeMonth':
            dateRange={}
            start=getBeforeDateTime(93)
            dateRange['startDate']=str(start.date())
            dateRange['endDate']=str(datetime.today().date())
        moneyRange = self.requestData['moneyRange']
        self.costCountResult = None
        self.selectStuIds = None
        self.inRoleStuDf = None  # stuRange['rangeData']
        stuFlag = self.getStuResultBystuRange(stuRange['rangeKind'], stuRange['rangeData'])
        if stuFlag['status'] == 0:
            return stuFlag
        return self.getStuResultByCondition(self.requestData['returnKind'],self.requestData['countKind'],
                    dateRange['startDate'],dateRange['endDate'],moneyRange['minMoney'],moneyRange['maxMoney'])

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
        self.costCountResult=pd.DataFrame(MyBaseModel.returnList(stu_cost_count.select(stu_cost_count.stuID,stu_cost_count.everyDayDetailRecord).where(
                            stu_cost_count.stuID.in_(self.selectStuIds))))
        self.costCountResult.dropna(axis=1, inplace=True)
        self.costCountResult.index = self.costCountResult['stuID']
        self.costCountResult = self.costCountResult['everyDayDetailRecord'].to_dict()
        for key in self.costCountResult.keys():
            self.costCountResult[key] = eval(self.costCountResult[key])   #{学号：全部记录,....}
        return {'status': 1}

    def getStuResultByCondition(self,returnKind,countKind,startDate,endDate,minMoney,maxMoney):
        startDate=strDateTimeChangeToInt(startDate)
        endDate=strDateTimeChangeToInt(endDate)
        resultStuDetail={}
        resultStuTotalTimes={}
        for stu in self.selectStuIds:
            stuCountDf=pd.DataFrame(self.costCountResult[stu])
            stuCountDf=stuCountDf.round(2)
            stuCountDf=stuCountDf[(stuCountDf['today']>=startDate)&(stuCountDf['today']<=endDate)]
            if countKind=='total':
                stuCountDf=stuCountDf[(stuCountDf['todayCostSum']>=minMoney)&(stuCountDf['todayCostSum']<=maxMoney)]
                resultStuTotalTimes[stu] = len(stuCountDf)
                resultStuDetail[stu]=stuCountDf[['today','todayCostSum']].to_dict('report')

            else:
                stuCountDf.index=stuCountDf['today']
                stuCountDict=stuCountDf['everyRecord'].to_dict()
                totalTimes=0
                oneStuRecord=[]
                for key in stuCountDict.keys():
                    oneDayDetail=np.array(stuCountDict[key])
                    times=len(oneDayDetail[(oneDayDetail>=minMoney)&(oneDayDetail<=maxMoney)])
                    if times>0:
                        totalTimes=totalTimes+times
                        line={'today':key,'times':times}
                        oneStuRecord.append(line)
                resultStuTotalTimes[stu]=totalTimes
                resultStuDetail[stu]=oneStuRecord

        self.inRoleStuDf.index = self.inRoleStuDf['stuID']
        stuBasicInfo = self.inRoleStuDf.to_dict('index')
        if returnKind== 'stuList':
            resultData=[]
            for stu in resultStuTotalTimes.keys():
                if resultStuTotalTimes[stu]>0:
                    oneStu=stuBasicInfo[stu]
                    oneStu['times']=resultStuTotalTimes[stu]
                    resultData.append(oneStu)
        else:
            resultData = []
            if len(resultStuDetail.keys())==0:
                return costModel(returnKind, countKind, [])
            if countKind=='single':
                for stu in resultStuDetail.keys():
                    for line in resultStuDetail[stu]:
                        oneStu=stuBasicInfo[stu].copy()
                        oneStu['date']=intChangeToDateStr(line['today'])
                        oneStu['times']=line['times']
                        resultData.append(oneStu)
            else:
                for stu in resultStuDetail.keys():
                    for line in resultStuDetail[stu]:
                        oneStu=stuBasicInfo[stu].copy()
                        oneStu['date']=intChangeToDateStr(line['today'])
                        oneStu['todayCostSum']=line['todayCostSum']
                        resultData.append(oneStu)


        return costModel(returnKind,countKind,resultData)
