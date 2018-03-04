from data_pretreatment.data_orm import *
from data_pretreatment.data_handle.state_count import startUpdateState
from data_pretreatment.common_func.deal_dateortime_func import getBeforeDateTime
from data_pretreatment.common_func.deal_dateortime_func import strChangeToDateTime
from data_pretreatment.common_func.deal_data_by_file import getDictDataFromFile,setDataInFile
'''
earlyWarningInfo={'costWarning':1/0,'costColor':blue/orange/yellow/red,'aboveOneWarning':'no/have/costWarning/...',..}
vacationStayflag='no/summer/winter'
stayDate=[{'from':'2010-01-01','to':'2010-01-01'},{}]
warningHistory=[{'appearDate':'2010-01-01','warningKind':'costWarning/aboveOneWarning','warningReason':['costFixed1/..',]},{}]
scoreWarningLevel:0  0/1/2/3/4
lastTimeCountDate:'2010-01-01'
'''


def initializeTable():
    restart=0
    allStuId=MyBaseModel.returnList2(stu_basic_info.select(stu_basic_info.stuID))
    with db_data.execution_context():
        allStu=MyBaseModel.returnList(stu_some_state.select())
        # if len(allStu)==0:  #表示是初次运行
        #     restart=1
        #     print('i am in this')
        if len(allStuId)!=len(allStu):
            restart=1
            print('i am in this is no equal')

    if restart==1:
        logger.info('start initialize stu_some_state')
        with db_data.execution_context():
            query = stu_some_state.delete()  # 清空表
            query.execute()

        allStuState=[]
        count=0
        for stu in allStuId:
            oneStu={'stuID':stu.stuID,'vacationStayflag':'no','stayDate':'[]','warningHistory':'[]','scoreWarningLevel':0,
                    'earlyWarningInfo':{'costWarning':0,'costColor':'blue','sleepWarning':0,
                                    'sleepColor':'blue','scoreWarning':0,'scoreColor':'blue',
                                    'aboveOneWarning':'no','aboveOneColor':'blue'
                                    },
                    'lastTimeCountDate':''
                    }
            allStuState.append(oneStu)
            count=count+1
            if count%500==0 or count==len(allStuId):
                with db_data.execution_context():
                    with db_data.atomic():
                        stu_some_state.insert_many(allStuState).execute()
                allStuState=[]
        logger.info('finish initialize stu_some_state')

def updateState():
    logger.info('start update stu_some_state')
    print('start update stu_some_state')
    nowDate=getBeforeDateTime(0)
    nowDateStr=str(nowDate.date())
    restart = 0  # 用于判断是否要重新更新表
    # if len(lastTimeCountDate) > 1:  # 数据存在错误
    #     restart = 1
    systemConf=getDictDataFromFile()
    if systemConf['lastStateUpdateDate']!=nowDateStr:
        restart=1
    # if lastTimeCountDate[0].lastTimeCountDate=='':    #first count
    #     restart=1
    # elif len(lastTimeCountDate) > 0:  # 数据库中的统计信息是一天内完成的
    #     lastCountDate = strChangeToDateTime(lastTimeCountDate[0].lastTimeCountDate).date()
    #     if yesterday.date() != lastCountDate:  # 判断表里的数据不是最新的
    #         restart=1

    if restart==1:
        startUpdateState()
        systemConf['lastStateUpdateDate']=nowDateStr
        setDataInFile(str(systemConf))
    logger.info('finish update stu_some_state')
    print('finish update stu_some_state')








