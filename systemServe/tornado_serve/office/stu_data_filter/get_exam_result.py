from tornado_serve.orm import *
from tornado_serve.common.get_class_or_stu_by_user import getClassOrStuByUser
from tornado_serve.office.stu_data_filter.return_model import scoreModel
import pandas as pd
class GetExamResult():
    def entry(self,receiveRequest):
        self.requestData = eval(receiveRequest.request.body)
        # self.requestData=receiveRequest
        stuRange=self.requestData['stuRange']
        courseRange=self.requestData['courseRange']
        self.resultDf=None
        stuFlag=self.getResultByStuRange(stuRange['rangeKind'],stuRange['rangeData'])
        if stuFlag['status']==0:
            return stuFlag
        if len(self.resultDf)>0:
            self.resultDf.drop(['courseIndex', 'stuClass', 'examSemester', 'examDate', 'courseKind', 'remarks'],
                               axis=1, inplace=True)
        else:
            return {'status': 0, 'errorInfo': '未查询到相关内容'}

        if courseRange!='all':
            self.getResultByCourseRange(courseRange['rangeKind'],courseRange['rangeData'])

        if len(self.resultDf)>0:
            resultData=self.resultDf.to_dict("report")
            return scoreModel('stuRecord','queryScore',resultData)
        else:
            return {'status':0,'errorInfo':'未查询到相关内容'}


    def getResultByStuRange(self,rangeKind,rangeData):
        if rangeKind =='useClassId':
            self.resultDf=pd.DataFrame(MyBaseModel.returnList(exam_results.select(exam_results.stuID,exam_results.stuName,exam_results.courseName,
                                exam_results.credit,exam_results.examKind,exam_results.examScore,exam_results.courseID).where(exam_results.stuClass.in_(rangeData))))
        else:
            inRoleStu=getClassOrStuByUser(self.requestData['userId'],1)
            inRoleStuDf=pd.DataFrame(inRoleStu)
            if rangeKind=='useStuId':
                if len(inRoleStuDf[inRoleStuDf['stuID']==rangeData])>0:
                    self.resultDf = pd.DataFrame(MyBaseModel.returnList(
                        exam_results.select(exam_results.stuID, exam_results.stuName, exam_results.courseName,
                                            exam_results.credit, exam_results.examKind, exam_results.examScore,exam_results.courseID).where(exam_results.stuID==rangeData)))
                else:
                    return {'status':0,'errorInfo':'该学生不存在或您无权限查看'}
            else:
                if len(inRoleStuDf[inRoleStuDf['stuName'] == rangeData]) > 0:
                    self.resultDf = pd.DataFrame(MyBaseModel.returnList(
                        exam_results.select(exam_results.stuID, exam_results.stuName, exam_results.courseName,
                                            exam_results.credit, exam_results.examKind, exam_results.examScore,exam_results.courseID).where(
                            exam_results.stuID == rangeData)))
                else:
                    return {'status': 0, 'errorInfo': '该学生不存在或您无权限查看'}
        return {'status':1}

    def getResultByCourseRange(self,rangeKind,rangeData):
        if rangeKind=='courseNum':
            self.resultDf=self.resultDf[self.resultDf['courseID']==rangeData]
        elif rangeKind=='courseName':
            self.resultDf = self.resultDf[self.resultDf['courseName'] == rangeData]



