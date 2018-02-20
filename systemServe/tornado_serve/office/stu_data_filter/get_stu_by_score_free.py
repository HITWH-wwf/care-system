import pandas as pd
from tornado_serve.orm import *
from tornado_serve.common.get_class_or_stu_by_user import getClassOrStuByUser
from tornado_serve.office.stu_data_filter.return_model import scoreModel
class GetStuByScoreFree():
    def entry(self,receiveRequest):
        self.requestData = eval(receiveRequest.request.body)
        # self.requestData=receiveRequest
        stuRange = self.requestData['stuRange']
        courseRange = self.requestData['courseRange']
        countRange=self.requestData['countRange']
        self.resultDf = None
        if courseRange=='all':
            stuFlag=self.getResultByStuRange(stuRange['rangeKind'],stuRange['rangeData'])
            if stuFlag['status']==0:
                return stuFlag
            else:
                return self.getLastResultByCountKind(self.requestData['returnKind'],self.requestData['countKind'],countRange['min'],countRange['max'])

        else:
            self.getResultByCourseRange(courseRange['rangeKind'],courseRange['rangeData'])
            stuFlag=self.getResultByStuRangeNextCourseRange(stuRange['rangeKind'],stuRange['rangeData'])
            if stuFlag['status']==0:
                return stuFlag
            return self.getLastResultStuWithCourse(self.requestData['returnKind'])

    def getLastResultByCountKind(self,returnKind,countKind,minNum,maxNum):
        if countKind=='failCourse':
            self.resultDf=self.resultDf[(self.resultDf['failNum']>=minNum)&(self.resultDf['failNum']<=maxNum)]
        elif countKind=='totalCredit':
            self.resultDf = self.resultDf[(self.resultDf['gainTotalCredit'] >= minNum) & (self.resultDf['gainTotalCredit'] <= maxNum)]
        else:
            self.resultDf = self.resultDf[(self.resultDf['failCredit'] >= minNum) & (self.resultDf['failCredit'] <= maxNum)]

        if len(self.resultDf)==0:
            return {'status': 0, 'errorInfo': '未查询到相关内容'}

        if returnKind=='stuRecord':
            if countKind=='totalCredit':
                allSuccessIdList=list(self.resultDf['successId'])
                allSuccessId=[]
                for line in allSuccessIdList:
                    allSuccessId=allSuccessId+line
                self.resultDf = pd.DataFrame(MyBaseModel.returnList(
                    exam_results.select(exam_results.stuID, exam_results.stuName, exam_results.courseName,
                                        exam_results.credit, exam_results.examKind, exam_results.examScore,
                                        exam_results.courseID).where(exam_results.id.in_(allSuccessId))))
            else:
                allFailIdList = list(self.resultDf['failId'])
                allFailId = []
                for line in allFailIdList:
                    allFailId = allFailId + line

                self.resultDf = pd.DataFrame(MyBaseModel.returnList(
                    exam_results.select(exam_results.stuID, exam_results.stuName, exam_results.courseName,
                                        exam_results.credit, exam_results.examKind, exam_results.examScore,
                                        exam_results.courseID).where(exam_results.id.in_(allFailId))))
            self.resultDf.dropna(axis=1, inplace=True)
            resultData = self.resultDf.to_dict("report")
            return scoreModel('stuRecord', 'queryScore', resultData)


        else:
            inRoleStu = getClassOrStuByUser(self.requestData['userId'], 1)
            inRoleStuDf = pd.DataFrame(inRoleStu)
            inRoleStuDf.index=inRoleStuDf['stuID']
            inRoleStuList=inRoleStuDf.to_dict('index')
            # self.resultDf.index = self.resultDf['stuID']
            if countKind == 'totalCredit':
                tempResult=self.resultDf['gainTotalCredit'].to_dict()
                resultData=[]
                for stu in tempResult.keys():
                    oneStu=inRoleStuList[stu]
                    oneStu['gainTotalCredit']=float(tempResult[stu])
                    resultData.append(oneStu)
            elif countKind=='failCourse':
                tempResult = self.resultDf['failNum'].to_dict()
                resultData = []
                for stu in tempResult.keys():
                    oneStu = inRoleStuList[stu]
                    oneStu['failNum'] = int(tempResult[stu])
                    resultData.append(oneStu)
            else:
                tempResult = self.resultDf['failCredit'].to_dict()
                resultData = []
                for stu in tempResult.keys():
                    oneStu = inRoleStuList[stu]
                    oneStu['failCredit'] = float(tempResult[stu])
                    resultData.append(oneStu)

            return scoreModel('stuList', countKind, resultData)

    def getResultByStuRange(self,rangeKind,rangeData):
        if rangeKind=='useClassId':
            inRoleStu = getClassOrStuByUser(self.requestData['userId'], 1,rangeData)
            inRoleStuDf = pd.DataFrame(inRoleStu)
            inRoleStuId=list(inRoleStuDf['stuID'])
            scoreCountResult=pd.DataFrame(MyBaseModel.returnList(stu_score_count.select(stu_score_count.stuID,stu_score_count.scoreCountInfo).where(stu_score_count.stuID.in_(inRoleStuId))))
            scoreCountResult.index=scoreCountResult['stuID']
            scoreCountResult=scoreCountResult['scoreCountInfo'].to_dict()
            self.resultDf=pd.DataFrame([eval(line) for line in scoreCountResult.values()],index=scoreCountResult.keys())
        else:
            inRoleStu = getClassOrStuByUser(self.requestData['userId'], 1)
            inRoleStuDf = pd.DataFrame(inRoleStu)
            if rangeKind == 'useStuId':
                if len(inRoleStuDf[inRoleStuDf['stuID'] == rangeData]) > 0:
                    scoreCountResult = pd.DataFrame(MyBaseModel.returnList(stu_score_count.select(stu_score_count.stuID,stu_score_count.scoreCountInfo).where(
                        stu_score_count.stuID==rangeData)))
                    scoreCountResult.index = scoreCountResult['stuID']
                    scoreCountResult = scoreCountResult['scoreCountInfo'].to_dict()
                    self.resultDf = pd.DataFrame([eval(line) for line in scoreCountResult.values()],index=scoreCountResult.keys())
                else:
                    return {'status': 0, 'errorInfo': '该学生不存在或您无权限查看'}
            else:
                stuIds=list(inRoleStuDf[inRoleStuDf['stuName']==rangeData]['stuID'])
                if len(stuIds) > 0:
                    scoreCountResult = pd.DataFrame(
                        MyBaseModel.returnList(stu_score_count.select(stu_score_count.stuID,stu_score_count.scoreCountInfo).where(
                            stu_score_count.stuID.in_(stuIds))))
                    scoreCountResult.index = scoreCountResult['stuID']
                    scoreCountResult = scoreCountResult['scoreCountInfo'].to_dict()
                    self.resultDf = pd.DataFrame([eval(line) for line in scoreCountResult.values()],index=scoreCountResult.keys())
                else:
                    return {'status': 0, 'errorInfo': '该学生不存在或您无权限查看'}
        return {'status':1}

    def getLastResultStuWithCourse(self,returnKind):
        self.resultDf=self.resultDf[self.resultDf['examScore']<60]
        if len(self.resultDf)>0:
            self.resultDf.drop(['courseIndex', 'stuClass', 'examSemester', 'examDate', 'courseKind', 'remarks'], axis=1,
                               inplace=True)
            if returnKind=='stuRecord':
                resultData = self.resultDf.to_dict("report")
                return scoreModel('stuRecord', 'failCourse', resultData)
            else:
                inRoleStu = getClassOrStuByUser(self.requestData['userId'], 1)
                inRoleStuDf = pd.DataFrame(inRoleStu)
                inRoleStuDf['number']=1
                self.resultDf.index=self.resultDf['stuID']
                inRoleStuDf=inRoleStuDf[inRoleStuDf['stuID'].isin(list(self.resultDf.index))]
                resultData=inRoleStuDf.to_dict('report')
                return scoreModel('stuList','failCourse', resultData)
        else:
            {'status': 0, 'errorInfo': '未查询到相关内容'}

    def getResultByStuRangeNextCourseRange(self,rangeKind,rangeData):
        if len(self.resultDf)==0:
            {'status': 0, 'errorInfo': '未查询到相关内容'}
        if rangeKind =='useClassId':
            self.resultDf=self.resultDf[self.resultDf['stuClass'].isin(rangeData)]
        else:
            inRoleStu=getClassOrStuByUser(self.requestData['userId'],1)
            inRoleStuDf=pd.DataFrame(inRoleStu)
            if rangeKind=='useStuId':
                if len(inRoleStuDf[inRoleStuDf['stuID']==rangeData])>0:
                    self.resultDf=self.resultDf[self.resultDf['stuID']==rangeData]
                else:
                    return {'status':0,'errorInfo':'该学生不存在或您无权限查看'}
            else:
                if len(inRoleStuDf[inRoleStuDf['stuName'] == rangeData]) > 0:
                    self.resultDf = self.resultDf[self.resultDf['stuName'] == rangeData]
                else:
                    return {'status': 0, 'errorInfo': '该学生不存在或您无权限查看'}
        if len(self.resultDf)==0:
            {'status': 0, 'errorInfo': '未查询到相关内容'}
        return {'status':1}

    def getResultByCourseRange(self, rangeKind, rangeData):
        if rangeKind=='courseNum':
            self.resultDf = pd.DataFrame(MyBaseModel.returnList(
                exam_results.select(exam_results.stuID, exam_results.stuName, exam_results.stuClass,exam_results.courseName,
                exam_results.credit, exam_results.examKind, exam_results.examScore,
                exam_results.courseID).where(exam_results.courseID==rangeData)))
        elif rangeKind == 'courseName':
            self.resultDf = pd.DataFrame(MyBaseModel.returnList(
                exam_results.select(exam_results.stuID, exam_results.stuName, exam_results.stuClass,exam_results.courseName,
                exam_results.credit, exam_results.examKind, exam_results.examScore,
                exam_results.courseID).where(exam_results.courseName==rangeData)))



