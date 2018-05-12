#coding=utf-8
from tornado_serve.common.get_class_or_stu_by_user import getClassOrStuByUser
from tornado_serve.common.deal_data_by_redis import getValue
import pandas as pd
from tornado_serve.office.stu_data_filter.get_stu_by_cost_free import GetStuByCostFree
from tornado_serve.office.stu_data_filter.get_stu_by_score_free import GetStuByScoreFree
from tornado_serve.office.stu_data_filter.get_stu_by_sleep_free import GetStuBySleepFree
from tornado_serve.office.stu_data_filter.get_stu_by_study_info import GetStuByStudyInfo
from tornado_serve.office.stu_data_filter.return_model import combineModel
class GetStuByFree():
    def entry(self,receiveRequest):
        self.requestData = eval(receiveRequest.request.body)
        # self.requestData=receiveRequest
        userName = getValue(self.requestData['sessionId'])
        # userName='wangjianting'
        if userName == None:
            return {'status': 0, 'errorInfo': '登陆状态已过期，请重新登录'}

        self.requestData['userId']=userName
        self.queryKind=self.requestData['queryKind']
        filters = {'cost': GetStuByCostFree, 'sleep': GetStuBySleepFree, 'score': GetStuByScoreFree,
                   'study': GetStuByStudyInfo}  # 过滤器字典
        filtersOrder=['study','score','sleep','cost']   #过滤器过滤顺序，安排合适能加快过滤速度

        if self.queryKind['type']=='single':
            kinds=self.queryKind['kinds']
            return filters[kinds]().entry(self.requestData)
        else:
            self.stuRange=self.requestData['stuRange']
            stuFlag=self.getStuResultBystuRange(self.stuRange['rangeKind'],self.stuRange['rangeData'])
            if stuFlag['status']==0:
                return stuFlag
            else:
                for one in filtersOrder:
                    if one in self.queryKind['kinds']:
                        self.selectStuIds=filters[one]().entry(self.requestData,self.selectStuIds)
                        # print(len(self.selectStuIds))
                        if len(self.selectStuIds)==0:
                            break

                resultData=self.inRoleStuDf[self.inRoleStuDf['stuID'].isin(self.selectStuIds)]
                return combineModel(resultData.to_dict('record'))




    def getStuResultBystuRange(self,rangeKind,rangeData):   #获取被筛选的学生名单

        if rangeKind=='useClassId':
            inRoleStu = getClassOrStuByUser(self.requestData['userId'], 1,rangeData)
            self.inRoleStuDf = pd.DataFrame(inRoleStu)
            self.selectStuIds = list(self.inRoleStuDf['stuID'])
        else:
            inRoleStu = getClassOrStuByUser(self.requestData['userId'], 1)
            self.inRoleStuDf = pd.DataFrame(inRoleStu)
            if rangeKind=='useStuId':
                if len(self.inRoleStuDf[self.inRoleStuDf['stuID'] == rangeData]) > 0:
                    self.selectStuIds=[rangeData]
                else:
                    return {'status': 0, 'errorInfo': '该学生不存在或您无权限查看'}
            else:
                self.selectStuIds = list(self.inRoleStuDf[self.inRoleStuDf['stuName'] == rangeData]['stuID'])
                if len(self.selectStuIds)==0:
                    return {'status': 0, 'errorInfo': '该学生不存在或您无权限查看'}

        return {'status': 1}