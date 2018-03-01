from data_pretreatment.data_orm import *
import pandas as pd
from data_pretreatment.common_func.deal_dateortime_func import getBeforeDateTime,dateTimeChangeToInt
from data_pretreatment.common_func.deal_dateortime_func import strChangeToDateTime
'''
earlyWarningInfo={'costWarning':1/0,'costColor':blue/orange/yellow/red,'aboveOneWarning':'no/have/costWarning/...',..}
vacationStayflag='no/summer/winter'
stayDate=[{'startDate':'2010-01-01','endDate':'2010-01-01'},{}]
warningHistory=[{'appearDate':'2010-01-01','warningKind':'costWarning/aboveOneWarning','warningReason':['costFixed1/..',]},{}]
scoreWarningLevel:0  0/1/2/3/4
lastTimeCountDate:'2010-01-01'
'''
scoreFixed4=18
scoreFixed3=16
scoreFixed2=12
scoreFixed1=3

def initializeTable():
    restart=0
    allStuId=MyBaseModel.returnList2(stu_basic_info.select(stu_basic_info.stuID))
    with db_data.execution_context():
        allStu=MyBaseModel.returnList(stu_some_state.select())
        if len(allStu)==0:  #表示是初次运行
            restart=1
    if restart==1:
        logger.info('start initialize stu_some_state')
        with db_data.execution_context():
            query = stu_some_state.delete()  # 清空表
            query.execute()

        allStuState=[]
        for stu in allStuId:
            oneStu={'stuID':stu.stuID,'vacationStayflag':'no','stayDate':'[]','warningHistory':'[]','scoreWarningLevel':0,
                    'earlyWarningInfo':{'costWarning':0,'costColor':'blue','sleepWarning':0,
                                    'sleepColor':'blue','scoreWarning':0,'scoreColor':'blue',
                                    'aboveOneWarning':'no','aboveOneColor':'blue'
                                    },
                    'lastTimeCountDate':''
                    }
            allStuState.append(oneStu)

        with db_data.execution_context():
            with db_data.atomic():
                stu_some_state.insert_many(allStuState).execute()

        logger.info('finish initialize stu_some_state')

def updateState():
    logger.info('start update stu_some_state')
    print('start update stu_some_state')
    yesterday = getBeforeDateTime(1)
    lastTimeCountDate = MyBaseModel.returnList2(stu_some_state.select(stu_some_state.lastTimeCountDate).distinct())
    restart = 0  # 用于判断是否要重新更新表
    if len(lastTimeCountDate) > 1:  # 数据存在错误
        restart = 1
    elif lastTimeCountDate[0].lastTimeCountDate=='':    #first count
        restart=1
    elif len(lastTimeCountDate) > 0:  # 数据库中的统计信息是一天内完成的
        lastCountDate = strChangeToDateTime(lastTimeCountDate[0].lastTimeCountDate).date()
        if yesterday.date() != lastCountDate:  # 判断表里的数据不是最新的
            restart=1

    if restart==1:
        startUpdateState()

    logger.info('finish update stu_some_state')
    print('finish update stu_some_state')



def startUpdateState():
    stuCostCountDf=pd.DataFrame(MyBaseModel.returnList(stu_cost_count.select(stu_cost_count.stuID,stu_cost_count.everyDayCount)))
    stuSleepCountDf=pd.DataFrame(MyBaseModel.returnList(stu_sleep_count.select(stu_sleep_count.stuID,stu_sleep_count.fixedQueryCountInfo)))
    stuScoreCountDf=pd.DataFrame(MyBaseModel.returnList(stu_score_count.select(stu_score_count.stuID,stu_score_count.scoreCountInfo)))
    allStu = MyBaseModel.returnList2(stu_basic_info.select(stu_basic_info.stuID,stu_basic_info.schoolStatus,stu_basic_info.sleepInOrOut,stu_basic_info.studyWithParent))
    stuScoreCountDf.dropna(axis=1, inplace=True)
    stuCostCountDf.dropna(axis=1, inplace=True)
    stuSleepCountDf.dropna(axis=1, inplace=True)
    stuScoreCountDf.index=stuScoreCountDf['stuID']
    stuSleepCountDf.index = stuScoreCountDf['stuID']
    stuCostCountDf.index = stuScoreCountDf['stuID']
    stuScoreCountDict=stuScoreCountDf['scoreCountInfo'].to_dict()
    stuCostCountDict=stuCostCountDf['everyDayCount'].to_dict()
    stuSleepCountDict=stuSleepCountDf['fixedQueryCountInfo'].to_dict()
    for stuid in stuScoreCountDict.keys():
        stuCostCountDict[stuid]=eval(stuCostCountDict[stuid])
        stuSleepCountDict[stuid]=eval(stuSleepCountDict[stuid])
        stuScoreCountDict[stuid]=eval(stuScoreCountDict[stuid])
    yesterday=getBeforeDateTime(1)
    yesterdayToStr=str(yesterday.date())
    yesterdayToInt=dateTimeChangeToInt(yesterday)
    count=0
    for stu in allStu:
        count=count+1
        if count%500==0:
            logger.info(count)
        if stu.schoolStatus != '在读':
            with db_data.execution_context():
                oneStuState = stu_some_state.select().where(stu_some_state.stuID == stu.stuID)
                if len(oneStuState) == 0:
                    continue
                oneStuState = oneStuState[0]
                oneStuState.lastTimeCountDate=yesterdayToStr
                oneStuState.save()
            continue
        oneStuCostDf=pd.DataFrame(stuCostCountDict[stu.stuID])
        oneStuSleepDf=pd.DataFrame(stuSleepCountDict[stu.stuID])
        oneStuScore=stuScoreCountDict[stu.stuID]
        oneDayCost=oneStuCostDf[oneStuCostDf['today']==yesterdayToInt].to_dict('records')
        oneDayCost=oneDayCost[0]
        oneDaySleep=oneStuSleepDf[oneStuSleepDf['today']==yesterdayToInt].to_dict('records')
        oneDaySleep=oneDaySleep[0]
        warningFlag=0   #用于标记该学生是否发生预警
        oneHistory={'appearDate':'','warningKind':'','warningReason':[]}

        #对消费进行预警判断
        if oneDayCost['largerMaxFlag']==1:   #一次性消费超过50
            warningFlag=warningFlag+1
            oneHistory['appearDate'] = yesterdayToStr
            oneHistory['warningKind'] = 'costWarning'
            oneHistory['warningReason'].append('costFixed2')
        elif oneDayCost['smallerMinFlag']==1:   #一天累计消费小于1元
            warningFlag = warningFlag + 1
            oneHistory['appearDate'] = yesterdayToStr
            oneHistory['warningKind'] = 'costWarning'
            oneHistory['warningReason'].append('costFixed1')

        #对归寝进行预警判断
        if oneDaySleep['fixed2']==1:    #24小时无刷卡进出宿舍记录
            warningFlag = warningFlag + 1
            oneHistory['appearDate'] = yesterdayToStr
            oneHistory['warningKind'] = 'sleepWarning'
            oneHistory['warningReason'].append('sleepFixed2')
        elif oneDaySleep['fixed1']==1:  #23:30分前未回宿舍
            warningFlag = warningFlag + 1
            oneHistory['appearDate'] = yesterdayToStr
            oneHistory['warningKind'] = 'sleepWarning'
            oneHistory['warningReason'].append('sleepFixed1')

        #对成绩进行预警判断
        if oneStuScore['failCredit']>=scoreFixed4 :
            scoreWarningLevel=4
        elif oneStuScore['failCredit']>=scoreFixed3:
            scoreWarningLevel=3
        elif oneStuScore['failCredit']>=scoreFixed2:
            scoreWarningLevel=2
        elif oneStuScore['failNum']>=scoreFixed1:
            scoreWarningLevel=1
        else:
            scoreWarningLevel=0

        with db_data.execution_context():
            oneStuState=stu_some_state.select().where(stu_some_state.stuID==stu.stuID)
            if len(oneStuState)==0:
                continue
            oneStuState=oneStuState[0]
            warningHistory = eval(oneStuState.warningHistory)
            earlyWarningInfo = eval(oneStuState.earlyWarningInfo)
            oneStuState.lastTimeCountDate = yesterdayToStr
            if stu.sleepInOrOut=='是' or stu.studyWithParent=='是':   #对于校外住宿的学生，只关注是否发生学情预警
                if oneStuState.scoreWarningLevel<scoreWarningLevel:
                    oneHistory['appearDate'] = yesterdayToStr
                    oneHistory['warningKind'] = 'scoreWarning'
                    scoreKind='scoreFixed'+str(scoreWarningLevel)
                    oneHistory['warningReason']=[scoreKind]
                    oneStuState.scoreWarningLevel=scoreWarningLevel
                    warningHistory.append(oneHistory)
                    earlyWarningInfo['aboveOneWarning']='scoreWarning'
                    if earlyWarningInfo['scoreWarning']==1:     #上次就出现学籍预警，且未处理
                        earlyWarningInfo['scoreColor']='orange'
                    else:
                        earlyWarningInfo['scoreWarning'] = 1
                        earlyWarningInfo['scoreColor'] = 'yellow'

                    oneStuState.warningHistory = str(warningHistory)
                    oneStuState.earlyWarningInfo=str(earlyWarningInfo)
                    oneStuState.save()
            else:
                if scoreWarningLevel > oneStuState.scoreWarningLevel:  # 出现了学情预警
                    oneStuState.scoreWarningLevel = scoreWarningLevel
                    scoreKind = 'scoreFixed' + str(scoreWarningLevel)
                    oneHistory['warningReason'].append(scoreKind)
                    warningFlag=warningFlag+1
                    oneHistory['warningKind'] = 'scoreWarning'

                if warningFlag>1:
                    oneHistory['warningKind'] = 'aboveOne'
                    if earlyWarningInfo['aboveOneWarning'] == 'have':    #上次就出现综合预警，且未处理
                        earlyWarningInfo['aboveOneColor']='red'
                        oneHistory['warningKind']='aboveOne'
                    else:
                        earlyWarningInfo['aboveOneWarning'] = 'have'
                        earlyWarningInfo['aboveOneColor'] = 'orange'

                elif warningFlag==1:    #出现一种预警
                    if earlyWarningInfo['aboveOneWarning'] == 'no':   #之前并没有处于预警状态
                        earlyWarningInfo['aboveOneWarning']=oneHistory['warningKind']
                        changeColor=oneHistory['warningKind'].replace('Warning','Color')
                        earlyWarningInfo[changeColor]='yellow'
                    elif earlyWarningInfo['aboveOneWarning'] == 'have': #之前就处于综合预警状态
                        pass
                    else:       #之前就处于一种预警状态
                        if earlyWarningInfo['aboveOneWarning']==oneHistory['warningKind']:
                            changeColor = oneHistory['warningKind'].replace('Warning', 'Color')
                            earlyWarningInfo[changeColor] = 'orange'
                        else:
                            earlyWarningInfo['aboveOneWarning']='have'
                            earlyWarningInfo['aboveOneColor'] = 'orange'

                warningHistory.append(oneHistory)
                oneStuState.warningHistory = str(warningHistory)
                oneStuState.earlyWarningInfo = str(earlyWarningInfo)
                oneStuState.save()




