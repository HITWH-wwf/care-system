from tornado_serve.orm import *
from tornado_serve.index.early_warning.change_early_warning_state import ChangeEarlyWarningState
from tornado_serve.index.early_warning.get_early_warning_stu import GetEarlyWarningStu
from tornado_serve.index.early_warning.get_stu_warning_history import GetStuWarningHistory
from tornado_serve.person.change_live_status import ChangeLiveStatus
from tornado_serve.person.change_school_status import ChangeSchoolStatus
from tornado_serve.person.stay_vacation import StayVacation
from tornado_serve.person.set_focus_color import SetFocusColor
from tornado_serve.system.early_warning_system_set import EarlyWarningSystemSet
import pandas as pd
from tornado_serve.office.stu_data_filter.get_stu_by_free import GetStuByFree
from tornado_serve.office.stu_data_filter.get_stu_by_fixed import GetStuByFixed
from tornado_serve.person.person_study_care_info.get_person_studycare_info import GetPersonStudyCareInfo
from tornado_serve.person.person_study_care_info.set_person_studycare_info import SetPersonStudyCareInfo
from tornado_serve.person.person_study_care_info.get_fudaoyuan_action_history import GetFudaoyuanActionHistory
from tornado_serve.person.person_study_care_info.get_to_examine_history import GetToExamineHistory
from tornado_serve.person.person_study_care_info.add_action_or_examine import AddActionOrExamine
from tornado_serve.index.get_study_care_table import GetStudyCareTable
from tornado_serve.office.export_count_table.generate_count_df import GenerateCountDf

def testChangeSchoolStatus():
    requestData={"userId":'wangjianting','stuId':'150410218','operation':'returnSchool'}
    result=ChangeSchoolStatus().entry(requestData)
    print(result)
    stu=MyBaseModel.returnList2(stu_basic_info.select(stu_basic_info.schoolStatus).where(stu_basic_info.stuID=='150410218'))
    stu=stu[0]
    print(stu.schoolStatus)


def testChangeLiveStatus():
    requestData = {"userId": 'wangjianting', 'stuId': '150410218','operation':'cancle',
        'kind':'studyWithParent'}
    result = ChangeLiveStatus().entry(requestData)
    print(result)
    stu = MyBaseModel.returnList2(
        stu_basic_info.select(stu_basic_info.studyWithParent).where(stu_basic_info.stuID == '150410218'))
    stu = stu[0]
    print(stu.studyWithParent)

def testStayVacation():
    requestData = {"userId": 'wangjianting', 'stuId': '150410218','vacation':'summer',
    'stayDate':[{'from':'2011-01-01','to':'2010-01-04'},{'from':'2010-11-01','to':'2010-12-04'}]}
    result = StayVacation().entry(requestData)
    print(result)
    stu = MyBaseModel.returnList2(
        stu_some_state.select(stu_some_state.vacationStayflag,stu_some_state.stayDate).where(stu_some_state.stuID == '150410218'))
    stu = stu[0]
    print(stu.vacationStayflag)
    print(stu.stayDate)

def testEarlyWarningSystemSet():
    requestData = {"userId": 'wangjianting','earlyWarningState':'allOpen' }
    result = EarlyWarningSystemSet().entry(requestData)
    print(result)

def testGetEarlyWarningStu():
    requestData = {"userId": 'wangjianting'}
    result = GetEarlyWarningStu().entry(requestData)
    print(result)

def testGetStuWarningHistory():
    requestData = {"userId": 'wangjianting','stuId':'150410218'}
    result = GetStuWarningHistory().entry(requestData)
    print(result)

def testChangeEarlyWarningState():
    requestData = {"userId": 'wangjianting', 'stuId': '150410218','operation':'cancle'}
    result = ChangeEarlyWarningState().entry(requestData)
    print(result)
    stu = MyBaseModel.returnList2(
        stu_some_state.select(stu_some_state.earlyWarningInfo).where(stu_some_state.stuID == '150410218'))
    stu = stu[0]
    print(stu.earlyWarningInfo)
    stu =MyBaseModel.returnList(stu_focus.select().where(stu_focus.stuID=='150410218'))
    print(stu)

def testSetFocusColor():
    requestData={"userId":'wangjianting','stuId':'150410219','showColor':'red'}
    result=SetFocusColor().entry(requestData)
    print(result)
    stu=MyBaseModel.returnList2(stu_basic_info.select(stu_basic_info.focusColor).where(stu_basic_info.stuID=='150410219'))
    stu=stu[0]
    print(stu.focusColor)


def testGetPersonStudyCareInfo():
    print(GetPersonStudyCareInfo().entry({'stuId':'150410218'}))

def testSetPersonStudyCareInfo():
    stuCareInfo={
        'stuId': '150410218', 'operate': 'checkPass',
        'studyInfo': {'type': ['测试'], 'remarks': '测试'} ,  # 学习,若无数据，则传空字符''，下同
         'thoughtInfo': {'type': ['宗教信仰'], 'remarks': '测试宗教'},  # 思想
        'economyInfo': {'type': '一般困难', 'remarks': 'str'},  # 经济
        'bodyInfo': '',  # 身体
        'networkInfo':'',  # 网络
        'sleepInfo': '',  # 公寓
    'burstInfo':'',  # 突发
    'peopleInfo':'',  # 人际
    'mentalityInfo':'',  # 心理
    'gayInfo':'',  # 同性恋
    'familyInfo':'',  # 单亲/孤儿
    'otherInfo': {'type': '无', 'remarks': 'str'}  # 其他问题
    }
    print(SetPersonStudyCareInfo().entry(stuCareInfo))

def testGetFudaoyuanActionHistory():
    print(GetFudaoyuanActionHistory().entry({'stuId':'150410218'}))

def testGetToExamineHistory():
    print(GetToExamineHistory().entry({'stuId':'150410218'}))

def testAddActionOrExamine():
    data={'stuId':'150410218', 'role': 'fushuji',   #/ 'fudaoyuan'
           'editUser':'test', 'content': '测试用例'
           }

    print(AddActionOrExamine().entry(data))

def testGetStudyCareTable():
    print(GetStudyCareTable().entry({'userId':'wangjianting'}))

# testGetStudyCareTable()
# testAddActionOrExamine()
# testGetFudaoyuanActionHistory()
# testGetToExamineHistory()
# testGetPersonStudyCareInfo()
# testSetPersonStudyCareInfo()




# testChangeSchoolStatus()
# testChangeLiveStatus()
# testStayVacation()
# testEarlyWarningSystemSet()
# testGetEarlyWarningStu()
# testGetStuWarningHistory()
# testChangeEarlyWarningState()
# testSetFocusColor()
requestData={  # "sessionId":....,
    "queryKind":{'type':'combine','kinds':['cost','sleep','score']},
    "returnKind":'stuList',    #若是combine，则设置为stuList
    'stuRange':{'rangeKind':'useClassId','rangeData':['1504102','1504101','1504103','1504104']}, #若按班级，参数为列表；按其余两个，参数为字符串
    'dateRange':'threeMonth',  #若用户未选择，则设为默认值，startDate=endDate='threeMonth'；成绩和学情的自由查询不需要此参数
    "cost":{
             'moneyRange':{'minMoney':0,'maxMoney':100},
             'countKind':'total'
            },

    'sleep':{
                'countKind':'noReturn',
                'appearTimes':{'minTimes':10,'maxTimes':100},  #若用户未选择，令appearTimes=1,即min和max都为1
            },
    'score':{
            'courseRange':'all',    #若未选择，值设为 'all'
            'countKind':'failCourse',    #若上面不是选择全部课程，这个强制设为failCourse，，min与max设为1！！！！！
            'countRange':{'min':1,'max':6}
            }
    # 'study':{
    #         'studyCareKind':['thoughtInfo',.....],#采用类似选择班级的方式进行选择，默认全选
    #         }/''
}
# print(GetStuByFree().entry(requestData))

requestDataFixed={
    "queryKind":{'type':'combine','kinds':['cost','sleep','score']},
    "returnKind":'stuList',    #若是combine，则设置为stuList
    "cost":'fixed1',
    'sleep':'fixed2',
    'score':'fixed1',
}
# print(GetStuByFixed().entry(requestDataFixed))