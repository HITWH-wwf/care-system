from data_pretreatment.data_orm import *
from data_pretreatment.common_func.deal_dateortime_func import *
import pandas as pd
import numpy as np

'''
everyDayDetailRecord:{'today':20100101,'everyRecord':[],'todayCostSum':11.3}
everyDayCount:{'today':20100101,'todayCostSum':11.3,'largerMaxFlag':0/1,'largerMaxRecordId':[111,],'smallerMinFlag':1/0}
'''
maxMoney=50     #超过多少额度
minMoney=1      #小于多少额度
continueDays=1  #连续多少天
countDays=93

def costCount(stuId):
    stuCostRecord = MyBaseModel.returnList(
        stu_transaction_record.select(stu_transaction_record.id, stu_transaction_record.turnover,stu_transaction_record.tradingTime).where(
            stu_transaction_record.stuID == stuId))
    everyDayDetailRecord = []
    everyDayCount = []
    yesterday = getBeforeDateTime(1)
    if len(stuCostRecord) == 0:  # 该学生没有任何消费记录
        for i in range(countDays):
            nowCountDate = getBeforeDateTime((i + 1))
            oneEveryDayDetailRecord = {'today':dateTimeChangeToInt(nowCountDate),'everyRecord':[],'todayCostSum':0}
            oneEveryDayCount = {'today':dateTimeChangeToInt(nowCountDate),'todayCostSum':0,'largerMaxFlag':0,'largerMaxRecordId':[],'smallerMinFlag':1}
            everyDayDetailRecord.append(oneEveryDayDetailRecord)
            everyDayCount.append(oneEveryDayCount)
        return {'stuID': stuId, 'everyDayDetailRecord':everyDayDetailRecord, 'everyDayCount': everyDayCount,
                    'lastTimeCountDate': str(yesterday.date())}
    else:
        stuDf = pd.DataFrame(stuCostRecord)
        stuDf['turnover']=-stuDf['turnover']       #对交易金额取反，让消费变为正，充值为负
        for i in range(countDays):
            nowCountDate = getBeforeDateTime((i + 1))
            nowCountNextDate = getBeforeDateTime(i)
            stuNowDateRecord = stuDf[(stuDf['tradingTime'] >= nowCountDate) & (stuDf['tradingTime'] < nowCountNextDate)]
            oneEveryDayDetailRecord = {'today':dateTimeChangeToInt(nowCountDate),'everyRecord':[],'todayCostSum':0}
            oneEveryDayCount = {'today':dateTimeChangeToInt(nowCountDate),'todayCostSum':0,'largerMaxFlag':0,'largerMaxRecordId':[],'smallerMinFlag':1}

            if len(stuNowDateRecord)==0:    #当天没有消费记录
                everyDayDetailRecord.append(oneEveryDayDetailRecord)
                everyDayCount.append(oneEveryDayCount)
                continue
            else:
                oneEveryDayDetailRecord['everyRecord']=list(stuNowDateRecord[stuNowDateRecord['turnover']>0]['turnover'])
                oneEveryDayCount['todayCostSum']=stuNowDateRecord[stuNowDateRecord['turnover']>0]['turnover'].sum()
                oneEveryDayDetailRecord['todayCostSum']=oneEveryDayCount['todayCostSum']
                if oneEveryDayCount['todayCostSum']>minMoney:
                    oneEveryDayCount['smallerMinFlag']=0    #累计消费大于1元
                largerMaxMoneyRecord=stuNowDateRecord[stuNowDateRecord['turnover']>maxMoney]['id']
                if len(largerMaxMoneyRecord)>0:
                    oneEveryDayCount['largerMaxFlag']=1
                    oneEveryDayCount['largerMaxRecordId']=list(largerMaxMoneyRecord)
                everyDayDetailRecord.append(oneEveryDayDetailRecord)
                everyDayCount.append(oneEveryDayCount)

        return {'stuID': stuId, 'everyDayDetailRecord':everyDayDetailRecord, 'everyDayCount': everyDayCount,
                    'lastTimeCountDate': str(yesterday.date())}