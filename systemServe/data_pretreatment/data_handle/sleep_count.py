from data_pretreatment.common_func.deal_dateortime_func import *
import numpy as np
import pandas as pd
from data_pretreatment.data_orm import *
'''
freeQueryCount={'today':20170101,'laterReturn':1/0,'noReturn':1/0,'inMaxId':12312,'outMaxId':123123}
fixedQueryCount={'today':20170101,'fixed1':1/0,'inMaxId1':1231,'outMaxId1':123,'fixed2':0/1,'fixed3':0/1,'inMaxId3':123,'outMaxId3':123}

fixed1:23：30前无刷卡归宿舍记录
fixed2:24小时内无任何出入记录
fixed3:23:30-5：00归寝室记录
'''

countDays=93    #额外多计算一天,保存94天的记录
freeLaterReturn=230000  #表示23:00:00
fixedNoReturn=233000    #表示23:30:00
fixedReturnStart=233000 #表示23:30:00
fixedReturnEnd=50000    #表示5:00:00

def sleepCount(stuId):
    stuSleepRecord=MyBaseModel.returnList(entry_and_exit.select(entry_and_exit.id,entry_and_exit.exitDate,entry_and_exit.entryDate).where(entry_and_exit.stuID==stuId))
    freeQueryCount = []
    fixedQueryCount = []
    yesterday=getBeforeDateTime(1)
    if len(stuSleepRecord)==0:  #该学生没有任何出入寝室记录
        for i in range(countDays):
            nowCountDate = getBeforeDateTime((i + 1))
            oneFreeRecord = {'today': dateTimeChangeToInt(nowCountDate), 'laterReturn': 0, 'noReturn': 1, 'inMaxId': '',
                             'outMaxId': ''}
            oneFixedRecord = {'today': dateTimeChangeToInt(nowCountDate), 'fixed1': 1, 'inMaxId1': '', 'outMaxId1': '',
                              'fixed2': 1, 'fixed3': 0,
                              'inMaxId3': '', 'outMaxId3': ''}
            freeQueryCount.append(oneFreeRecord)
            fixedQueryCount.append(oneFixedRecord)

        return {'stuID':stuId,'freeQueryCountInfo':freeQueryCount,'fixedQueryCountInfo':fixedQueryCount,'lastTimeCountDate':str(yesterday.date())}
    stuDf=pd.DataFrame(stuSleepRecord)
    for i in range(countDays):
        nowCountDate=getBeforeDateTime((i+1))
        nowCountNextDate=getBeforeDateTime(i)
        stuEntry=stuDf[(stuDf['entryDate']>=nowCountDate)&(stuDf['entryDate']<nowCountNextDate)]['entryDate']
        stuExit = stuDf[(stuDf['exitDate'] >= nowCountDate) & (stuDf['exitDate'] < nowCountNextDate)]['exitDate']
        if len(stuExit)==0:
            exitMaxRecordList=[]
        else:
            exitMax = stuDf.loc[stuExit.idxmax()].to_dict()
            exitMaxRecordList=[exitMax]

        if len(stuEntry)==0:
            entryMaxRecordList=[]
        else:
            entryMax=stuDf.loc[stuEntry.idxmax()].to_dict()
            entryMaxRecordList=[entryMax]

        if len(entryMaxRecordList)==0 and len(exitMaxRecordList)==0:    #24小时内无任何出入记录
            oneFreeRecord = {'today':dateTimeChangeToInt(nowCountDate), 'laterReturn': 0, 'noReturn': 1, 'inMaxId':'', 'outMaxId':''}
            oneFixedRecord = {'today':dateTimeChangeToInt(nowCountDate), 'fixed1': 1, 'inMaxId1':'', 'outMaxId1':'', 'fixed2':1, 'fixed3':0,
                              'inMaxId3':'', 'outMaxId3':''}
            freeQueryCount.append(oneFreeRecord)
            fixedQueryCount.append(oneFixedRecord)
            continue
        elif len(entryMaxRecordList)==0:     #没有归寝记录
            entryMaxRecord={'entryDate':nowCountDate,'id':-1}     #则默认归寝时间是今天凌晨
            exitMaxRecord=exitMaxRecordList[0]

        elif len(exitMaxRecordList)==0:     #没有外出记录

            exitMaxRecord={'exitDate':nowCountDate,'id':-1}      #则默认外出时间是今天凌晨
            entryMaxRecord=entryMaxRecordList[0]
        else:
            entryMaxRecord=entryMaxRecordList[0]
            exitMaxRecord=exitMaxRecordList[0]


        oneFreeRecord = {'today':dateTimeChangeToInt(nowCountDate), 'laterReturn': 0, 'noReturn': 0, 'inMaxId': '', 'outMaxId': ''}
        oneFixedRecord = {'today':dateTimeChangeToInt(nowCountDate), 'fixed1': 0, 'inMaxId1': '', 'outMaxId1': '', 'fixed2': 0, 'fixed3': 0,
                          'inMaxId3': '', 'outMaxId3': ''}

        #晚归
        if entryMaxRecord['entryDate']>exitMaxRecord['exitDate'] and compareTime(entryMaxRecord['entryDate'],freeLaterReturn):
            oneFreeRecord['laterReturn']=1
            oneFreeRecord['inMaxId']=entryMaxRecord['id']
            oneFreeRecord['outMaxId']=exitMaxRecord['id']

        #未归
        if exitMaxRecord['exitDate']>entryMaxRecord['entryDate']:
            oneFreeRecord['noReturn']=1
            oneFreeRecord['inMaxId'] = entryMaxRecord['id']
            oneFreeRecord['outMaxId'] = exitMaxRecord['id']

        #23：30前无刷卡归宿舍记录
        if (entryMaxRecord['entryDate']>exitMaxRecord['exitDate'] and compareTime(entryMaxRecord['entryDate'],fixedNoReturn)) or (exitMaxRecord['exitDate']>entryMaxRecord['entryDate']):
            oneFixedRecord['fixed1']=1
            oneFixedRecord['inMaxId1']=entryMaxRecord['id']
            oneFixedRecord['outMaxId1']=exitMaxRecord['id']

        #fixed3: 23:30 - 5：00归寝室
        stuEntry2 = stuDf[(stuDf['entryDate']>=nowCountNextDate)&(stuDf['entryDate']<getBeforeDateTime(i-1))]['entryDate']   #这个-1要注意
        if len(stuEntry2)==0:
            nextEntryMinRecordList=[]
        else:
            nextEntryMin = stuDf.loc[stuEntry2.idxmin()].to_dict()
            nextEntryMinRecordList=[nextEntryMin]
        if len(nextEntryMinRecordList)>0:
            nextEntryMinRecord=nextEntryMinRecordList[0]
        else:
            nextEntryMinRecord={'entryDate':strChangeToDateTime('2010-01-01','6:00:00'),'id':-1}  #因为后面只用到时间部分，不涉及日期，所以这里偷懒了

        if entryMaxRecord['entryDate']>exitMaxRecord['exitDate'] and compareTime(entryMaxRecord['entryDate'],fixedReturnStart):
            oneFixedRecord['fixed3']=1
            oneFixedRecord['inMaxId3']=entryMaxRecord['entryDate']
            oneFixedRecord['outMaxId3']=exitMaxRecord['exitDate']
        elif exitMaxRecord['exitDate']>entryMaxRecord['entryDate'] and compareTime(nextEntryMinRecord['entryDate'],fixedReturnEnd)==0:
            oneFixedRecord['fixed3'] = 1
            oneFixedRecord['inMaxId3'] = nextEntryMinRecord['entryDate']
            oneFixedRecord['outMaxId3'] = exitMaxRecord['exitDate']

        freeQueryCount.append(oneFreeRecord)
        fixedQueryCount.append(oneFixedRecord)

    return {'stuID': stuId, 'freeQueryCountInfo': freeQueryCount, 'fixedQueryCountInfo': fixedQueryCount,
            'lastTimeCountDate': str(yesterday.date())}
