from tornado_serve.orm import *
from tornado_serve.index.early_warning.change_early_warning_state import ChangeEarlyWarningState
from tornado_serve.index.early_warning.get_early_warning_stu import GetEarlyWarningStu
from tornado_serve.index.early_warning.get_stu_warning_history import GetStuWarningHistory
from tornado_serve.person.change_live_status import ChangeLiveStatus
from tornado_serve.person.change_school_status import ChangeSchoolStatus
from tornado_serve.person.stay_vacation import StayVacation
from tornado_serve.person.set_focus_color import SetFocusColor
from tornado_serve.system.early_warning_system_set import EarlyWarningSystemSet



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

# testChangeSchoolStatus()
# testChangeLiveStatus()
# testStayVacation()
# testEarlyWarningSystemSet()
# testGetEarlyWarningStu()
# testGetStuWarningHistory()
# testChangeEarlyWarningState()
# testSetFocusColor()


