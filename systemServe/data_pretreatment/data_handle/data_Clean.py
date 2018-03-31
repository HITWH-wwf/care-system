from data_pretreatment.data_orm import *

def cleanStuBasicInfo():    #step1
    print('start')
    with db_data.execution_context():
        allStu=stu_basic_info.select()
        for stu in allStu:
            stu.schoolStatus='在读'
            stu.sleepInOrOut='否'
            stu.studyWithParent='否'
            stu.save()
    print('end')

def cleanStuBasicInfoWithStuFocus1():   #规范校外住宿与家长陪读字段   step3
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

def cleanStuBasicInfoWithStuFocus2():   #规范关注颜色等级字段，关注等级   step4
    print('start')
    with db_data.execution_context():
        allStu = stu_basic_info.select()
        for stu in allStu:
            if stu.state == 1:  # 推介关注
                stu.state=2
                stu.focusColor = 'orange'
            elif stu.state == 2:    #重点关注
                stu.state = 4
                stu.focusColor = 'red'
            else:
                stu.focusColor = 'blue'
            stu.save()

    print('end')


def cleanStuFocus():    #更新关注等级   step2
    print('start')
    with db_data.execution_context():
        focusStu=stu_focus.select()
        for stu in focusStu:
            if stu.level==1:    #推介关注
                stu.level=2
            elif stu.level==2:
                stu.level=4

            stu.save()

    print('end')