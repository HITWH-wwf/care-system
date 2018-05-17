from data_pretreatment.data_orm import *
import pandas as pd
from data_pretreatment.common_func.deal_data_by_file import getDictDataFromFile
from data_pretreatment.common_func.deal_dateortime_func import getBeforeDateTime,dateTimeChangeToInt,strDateTimeChangeToInt
scoreFixed4=18
scoreFixed3=16
scoreFixed2=12
scoreFixed1=3

def startUpdateState():
    systemConf=getDictDataFromFile()
    if systemConf['isOpen']=='close':
        logger.info('earlyWarningSystem is close')
        return 0
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
            # with db_data.execution_context():
            #     oneStuState = stu_some_state.select().where(stu_some_state.stuID == stu.stuID)
            #     if len(oneStuState) == 0:
            #         continue
            #     oneStuState = oneStuState[0]
            #     oneStuState.lastTimeCountDate=yesterdayToStr
            #     oneStuState.save()
            continue
        elif systemConf['isOpen']=='halfOpen':
            if judgeIsStaySchool(stu.stuID)==False:
                continue
            #判断是不是留校生，是的话，接着往下执行，不是的话，直接跳过
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
        if systemConf['costWarning']=='close':
          pass
        elif oneDayCost['largerMaxFlag']==1:   #一次性消费超过50
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
        if systemConf['sleepWarning']=='close':
            pass
        elif oneDaySleep['fixed2']==1:    #24小时无刷卡进出宿舍记录
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
        if systemConf['scoreWarning']=='close':
            scoreWarningLevel = 0
        elif oneStuScore['failCredit']>=scoreFixed4 :
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
            if oneStuState.lastTimeCountDate == yesterdayToStr: #该学生最新的预警信息已经统计过
                continue
            oneStuState.lastTimeCountDate = yesterdayToStr
            if stu.sleepInOrOut=='是' or stu.studyWithParent=='是':   #对于校外住宿的学生，只关注是否发生学业预警
                if oneStuState.scoreWarningLevel<scoreWarningLevel:
                    oneHistory['appearDate'] = yesterdayToStr
                    oneHistory['warningKind'] = 'scoreWarning'
                    scoreKind='scoreFixed'+str(scoreWarningLevel)
                    oneHistory['warningReason']=[scoreKind]
                    oneStuState.scoreWarningLevel=scoreWarningLevel
                    warningHistory.append(oneHistory)
                    earlyWarningInfo['aboveOneWarning']='scoreWarning'
                    if earlyWarningInfo['scoreWarning']==1:     #上次就出现学业预警，且未处理
                        earlyWarningInfo['scoreColor']='orange'
                    else:
                        earlyWarningInfo['scoreWarning'] = 1
                        earlyWarningInfo['scoreColor'] = 'yellow'

                    oneStuState.warningHistory = str(warningHistory)
                    oneStuState.earlyWarningInfo=str(earlyWarningInfo)
                    oneStuState.save()
            else:
                if scoreWarningLevel > oneStuState.scoreWarningLevel:  # 出现了学业预警
                    oneStuState.scoreWarningLevel = scoreWarningLevel
                    scoreKind = 'scoreFixed' + str(scoreWarningLevel)
                    oneHistory['warningReason'].append(scoreKind)
                    warningFlag=warningFlag+1
                    oneHistory['warningKind'] = 'scoreWarning'
                    oneHistory['appearDate'] = yesterdayToStr
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
                if oneHistory['appearDate'] != '':
                    warningHistory.append(oneHistory)
                oneStuState.warningHistory = str(warningHistory)
                oneStuState.earlyWarningInfo = str(earlyWarningInfo)
                oneStuState.save()

def judgeIsStaySchool(stuId):   #属于留校期间，返回True，其余情况返回False
    with db_data.execution_context():
        thisStu=stu_some_state.select().where(stu_some_state.stuID==stuId)
        if len(thisStu)==0:
            return False
        thisStu=thisStu[0]
        if thisStu.vacationStayflag=='no':
            return False
        stayDate=eval(thisStu.stayDate)
        yesterday=getBeforeDateTime(1)
        yesterdayToInt=dateTimeChangeToInt(yesterday)
        overdue=[]
        isStaySchoolFlag=0
        for line in stayDate:
            if strDateTimeChangeToInt(line['from'])<=yesterdayToInt and strDateTimeChangeToInt(line['to'])>=yesterdayToInt:
                isStaySchoolFlag=1
            if strDateTimeChangeToInt(line['to'])<yesterdayToInt:  #已经不处于留校期间了
                overdue.append(line)

        for line in overdue:
            stayDate.remove(line)
        if len(stayDate)==0:
            thisStu.vacationStayflag='no'
            thisStu.stayRemarks=''
        thisStu.stayDate=str(stayDate)
        thisStu.save()
        if isStaySchoolFlag==1:
            return True
        else:
            return False

