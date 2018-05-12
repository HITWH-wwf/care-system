from tornado_serve.orm import *
from tornado_serve.common.get_class_or_stu_by_user import getClassOrStuByUser
import pandas as pd
from tornado_serve.office.stu_data_filter.return_model import costModel
from tornado_serve.common.deal_dateortime_func import intChangeToDateStr,getBeforeDateTime,dateTimeChangeToInt
class GetStuByCostFixed():
    def entry(self,receiveRequest,waitFilteStuId=None):
        # self.requestData = eval(receiveRequest.request.body)
        self.requestData = receiveRequest
        self.waitFilteStuId=waitFilteStuId
        if self.waitFilteStuId is not None:
            self.inRoleStuDf = []
            self.selectStuIds = self.waitFilteStuId
        else:
            inRoleStu = getClassOrStuByUser(self.requestData['userId'], 1)
            self.inRoleStuDf = pd.DataFrame(inRoleStu)
            self.selectStuIds = list(self.inRoleStuDf['stuID'])

        self.costCountResult = pd.DataFrame(MyBaseModel.returnList(
            stu_cost_count.select(stu_cost_count.stuID, stu_cost_count.everyDayCount).where(
                stu_cost_count.stuID.in_(self.selectStuIds))))

        self.costCountResult.dropna(axis=1, inplace=True)
        self.costCountResult.index = self.costCountResult['stuID']
        self.costCountResult = self.costCountResult['everyDayCount'].to_dict()
        for key in self.costCountResult.keys():
            self.costCountResult[key] = eval(self.costCountResult[key])  # {学号：全部记录,....}

        result=self.getStuResultByCondition(self.requestData['returnKind'], self.requestData['cost'])

        return result

    def getStuResultByCondition(self, returnKind, queryKind):
        resultStu = {}
        recordIdList = []
        needCountDays=getBeforeDateTime(3)	#固定查询需要统计的天数
        dateLevel=dateTimeChangeToInt(needCountDays)
        resultStuId=[]
        for stu in self.selectStuIds:
            stuCountDf = pd.DataFrame(self.costCountResult[stu])
            stuCountDf=stuCountDf[stuCountDf['today']>=dateLevel]
            stuCountDf=stuCountDf.round(2)
            if queryKind=='fixed1':
                stuCountDf = stuCountDf[stuCountDf['smallerMinFlag'] == 1]
                times = sum(stuCountDf['smallerMinFlag'])
            else:
                stuCountDf = stuCountDf[stuCountDf['largerMaxFlag'] == 1]
                times = sum(stuCountDf['largerMaxFlag'])
            if len(stuCountDf)==0:
                continue
            if self.waitFilteStuId is not None:
                resultStuId.append(stu)
                continue

            if returnKind == 'stuRecord':
                if queryKind == 'fixed1':
                    happenDateList=list(stuCountDf['today'])
                    # print(happenDateList)
                    happenDateList=[intChangeToDateStr(x) for x in happenDateList]
                    resultStu[stu]=happenDateList
                else:
                    recordList = list(stuCountDf['largerMaxRecordId'])
                    for line in recordList:
                        recordIdList=recordIdList+line
                    resultStu[stu]=times
            else:
                resultStu[stu] = times

        if self.waitFilteStuId is not None:
            return resultStuId


        self.inRoleStuDf.index = self.inRoleStuDf['stuID']
        stuBasicInfo = self.inRoleStuDf.to_dict('index')
        resultData = []
        if returnKind== 'stuList':
            for stu in resultStu.keys():
                oneStu = stuBasicInfo[stu]
                oneStu['times'] = int(resultStu[stu])
                resultData.append(oneStu)
            # for stu in result:
            #     resultData.append(result)
        else:
            recordIdList = [x for x in recordIdList if x != '' and x >= 0]
            recordIdList = set(recordIdList)
            if queryKind=='fixed2':
                totalRecordInfoDf=pd.DataFrame(self.getRecordInfo(recordIdList))
                totalRecordInfoDf.dropna(axis=1,inplace=True)
                totalRecordInfoDf.drop(['id'],axis=1,inplace=True)
                totalRecordInfoDf['stuName'] = '未记录'
                for stu in resultStu.keys():
                    totalRecordInfoDf.loc[totalRecordInfoDf[totalRecordInfoDf['stuID']==stu].index,('stuName')]=stuBasicInfo[stu]['stuName']
                resultData = totalRecordInfoDf.to_dict("report")
            else:
                for stu in resultStu.keys():
                    for oneDay in resultStu[stu]:
                        oneRecord = stuBasicInfo[stu].copy()
                        oneRecord['happenDate'] = oneDay
                        resultData.append(oneRecord)
        return costModel(returnKind,queryKind,resultData)

    def getRecordInfo(self,recordIdList):
        totalRecordInfo=MyBaseModel.returnList(stu_transaction_record.select().where(stu_transaction_record.id.in_(recordIdList
            )).group_by(stu_transaction_record.stuID,stu_transaction_record.id))
        for i in range(len(totalRecordInfo)):
            if totalRecordInfo[i]['merchantAccount'] == None or len(totalRecordInfo[i]['merchantAccount']) == 0:
                totalRecordInfo[i]['merchantAccount'] = "未知"
            else:
                totalRecordInfo[i]['merchantAccount'] = self.funAccountToName(totalRecordInfo[i]['merchantAccount'])
            costTime = str(totalRecordInfo[i]['tradingTime'])
            totalRecordInfo[i]['tradingTime'] = costTime
        return totalRecordInfo

    def funAccountToName(self, account):

        name = MyBaseModel.returnList(merchant_date.select(merchant_date.merchantName).where(merchant_date.merchantAccount == account).dicts(), key = "merchantName")
        #返回的name是一个列表，列表中的元素是一个字符串，不是字典
        if len(name) == 0:
            return ""
        else:
            return name[0]
