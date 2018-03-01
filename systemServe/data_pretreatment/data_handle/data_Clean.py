from data_pretreatment.data_orm import *

def cleanStuBasicInfo():
    print('start')
    with db_data.execution_context():
        allStu=stu_basic_info.select()
        for stu in allStu:
            stu.schoolStatus='在读'
            stu.sleepInOrOut='否'
            stu.studyWithParent='否'
            stu.save()
    print('end')

def cleanStuBasicInfoWithStuFocus():
    print('start')
    focusStu=MyBaseModel.returnList2(stu_focus.select())
    for stu in focusStu:
        if stu.sleepInOrOut=='校外住宿' or stu.sleepInOrOut=='1':
            with db_data.execution_context():
                thisStu=stu_basic_info.select().where(stu_basic_info.stuID==stu.stuID)
                if len(thisStu)>0:
                    thisStu=thisStu[0]
                    thisStu.sleepInOrOut='是'
                    thisStu.save()
        if stu.studyWithParent=='1':
            with db_data.execution_context():
                thisStu = stu_basic_info.select().where(stu_basic_info.stuID == stu.stuID)
                if len(thisStu)>0:
                    thisStu = thisStu[0]
                    thisStu.studyWithParent = '是'
                    thisStu.save()

    print('end')
