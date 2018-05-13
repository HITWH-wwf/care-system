#coding=utf-8
from tornado_serve.orm import stu_all_aspect_info,MyBaseModel
from tornado_serve.common.get_class_or_stu_by_user import getClassOrStuByUser
from tornado_serve.office.stu_data_filter.return_model import studyInfoModel
import pandas as pd
class GetStuByStudyInfo():
    def entry(self,receiveRequest,waitFilteStuId=None):
        # self.requestData = eval(receiveRequest.request.body)
        self.requestData = receiveRequest
        self.waitFilteStuId = waitFilteStuId
        stuRange = self.requestData.get('stuRange','all')
        stuFlag=self.getStuResultBystuRange(stuRange)
        if stuFlag['status'] == 0:
            return stuFlag
        condition=self.requestData['study']
        return self.getStuResultByCondition(condition['studyCareKind'],condition['countKind'])



    def getStuResultBystuRange(self,stuRange):
        if self.waitFilteStuId is not None: #组合查询的
            self.selectStuIds=self.waitFilteStuId
            self.inRoleStuDf=[]
        elif stuRange=='all':   #固定查询的
            inRoleStu = getClassOrStuByUser(self.requestData['userId'], 1)
            self.inRoleStuDf = pd.DataFrame(inRoleStu)
            self.selectStuIds = list(self.inRoleStuDf['stuID'])
        else:   #自由查询的
            if stuRange['rangeKind'] == 'useClassId':
                inRoleStu = getClassOrStuByUser(self.requestData['userId'], 1, stuRange['rangeData'])
                self.inRoleStuDf = pd.DataFrame(inRoleStu)
                self.selectStuIds = list(self.inRoleStuDf['stuID'])
            else:
                inRoleStu = getClassOrStuByUser(self.requestData['userId'], 1)
                self.inRoleStuDf = pd.DataFrame(inRoleStu)
                if stuRange['rangeKind'] == 'useStuId':
                    if len(self.inRoleStuDf[self.inRoleStuDf['stuID'] == stuRange['rangeData']]) > 0:
                        self.selectStuIds = [stuRange['rangeData']]
                    else:
                        return {'status': 0, 'errorInfo': '该学生不存在或您无权限查看'}
                else:
                    self.selectStuIds = list(self.inRoleStuDf[self.inRoleStuDf['stuName'] == stuRange['rangeData']]['stuID'])
                    if len(self.selectStuIds) == 0:
                        return {'status': 0, 'errorInfo': '该学生不存在或您无权限查看'}

        self.stuStudyInfo=MyBaseModel.returnList(stu_all_aspect_info.select().where(stu_all_aspect_info.stuID.in_(self.selectStuIds) and \
                                stu_all_aspect_info.stuState==1))   #此部分只筛选处于关注的学生
        return {'status': 1}

    def getStuResultByCondition(self,studyCareKinds,countKind):
        resultStu={}
        resultStuId = []
        if countKind=='onlyOne':
            for stu in self.stuStudyInfo:
                nums=0
                for oneCareKind in studyCareKinds:
                    if stu[oneCareKind]!='':
                        nums+=1

                if nums>0:
                    resultStu[stu['stuID']]=nums
                    resultStuId.append(stu['stuID'])
        else:
            for stu in self.stuStudyInfo:
                for oneCareKind in studyCareKinds:
                    if stu[oneCareKind]=='':
                        break
                else:
                    resultStuId.append(stu['stuID'])

        if self.waitFilteStuId is not None:
            return resultStuId
        else:
            resultData=[]
            self.inRoleStuDf.index = self.inRoleStuDf['stuID']
            stuBasicInfo = self.inRoleStuDf.to_dict('index')
            kinds=len(studyCareKinds)
            for stuID in resultStuId:
                oneStu=stuBasicInfo[stuID]
                if countKind == 'onlyOne':
                    oneStu['appearKinds']=resultStu[stuID]
                else:
                    oneStu['appearKinds']=kinds

                resultData.append(oneStu)

            return studyInfoModel(resultData)


