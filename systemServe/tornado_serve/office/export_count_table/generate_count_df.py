from tornado_serve.common.get_class_or_stu_by_user import getClassOrStuByUser
from tornado_serve.orm import MyBaseModel,stu_all_aspect_info
from tornado_serve.common.deal_dateortime_func import getGradeByYear
from tornado_serve.office.export_count_table.some_setting_info import getSelectState,getCollegeDict,getCareKindList
import pandas as pd

class GenerateCountDf():
    def entry(self,userName):
        self.userName=userName      #这个变量尚未使用，如果日后需要改变统计的学生范围，可以修改此处用户的管理学生范围
        self.countStuId=[]
        stuBasicInfoDf=self.getStuBasicInfoDf()
        stuCareInfoDf=self.getStuCareInfoCountDf()
        resultDf=pd.merge(stuCareInfoDf,stuBasicInfoDf,on='stuID')
        return resultDf


    def getStuBasicInfoDf(self):    #获取包括学生的学号，学院，年级信息
        inRoleStu=getClassOrStuByUser('admin',1)
        stuBasicInfo=[]
        collegeDict=getCollegeDict()
        gradeDict=getGradeByYear()
        for stu in inRoleStu:
            try:
                oneStu={}
                oneStu['stuID']=stu['stuID']
                oneStu['grade']=gradeDict[stu['stuClassNumber'][0:2]]
                oneStu['college']=collegeDict[stu['stuClassNumber'][2:4]]
                stuBasicInfo.append(oneStu)
                self.countStuId.append(oneStu['stuID'])
            except:
                #非法班级或学号
                pass
        return pd.DataFrame(stuBasicInfo)

    def getStuCareInfoCountDf(self):
        inRoleStu=MyBaseModel.returnList(stu_all_aspect_info.select().where(stu_all_aspect_info.stuID.in_(self.countStuId) and stu_all_aspect_info.stuState==1))
        careKindList=getCareKindList()
        stuCareInfo=[]
        selectState=getSelectState()
        oneType=['studyInfo', 'thoughtInfo','burstInfo']    #复选框，可多选
        twoType=['bodyInfo', 'networkInfo','sleepInfo','familyInfo']
        for stu in inRoleStu:
            oneStu = {}
            oneStu['stuID'] =stu['stuID']
            for kind in careKindList:
                oneCareInfo = eval(stu[kind])
                oneStu[kind] = 0
                if len(oneCareInfo['type'])==0:
                    continue
                if kind=='economyInfo':
                    oneStu[kind]=selectState[kind][oneCareInfo['nowState']]
                elif kind in oneType:
                    for oneKind in oneCareInfo['type']:
                        oneStu[kind]+=selectState[kind][oneKind]
                elif kind in twoType:
                    oneStu[kind] = selectState[kind][oneCareInfo['type']]
                else:
                    oneStu[kind]=1

            stuCareInfo.append(oneStu)


