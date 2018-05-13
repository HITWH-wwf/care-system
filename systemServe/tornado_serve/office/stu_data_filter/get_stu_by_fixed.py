#coding=utf-8
from tornado_serve.common.get_class_or_stu_by_user import getClassOrStuByUser
from tornado_serve.common.deal_data_by_redis import getValue,getFlagValue
import pandas as pd
from tornado_serve.office.stu_data_filter.get_stu_by_cost_fixed import GetStuByCostFixed
from tornado_serve.office.stu_data_filter.get_stu_by_score_fixed import GetStuByScoreFixed
from tornado_serve.office.stu_data_filter.get_stu_by_sleep_fixed import GetStuBySleepFixed
from tornado_serve.office.stu_data_filter.get_stu_by_study_info import GetStuByStudyInfo
from tornado_serve.office.stu_data_filter.return_model import combineModel
class GetStuByFixed():
    def entry(self,receiveRequest):
        self.requestData = eval(receiveRequest.request.body)
        # self.requestData=receiveRequest
        userName = getValue(self.requestData['sessionId'])
        # userName='wangjianting'
        if userName == None:
            return {'status': 0, 'errorInfo': '登陆状态已过期，请重新登录'}

        self.requestData['userId']=userName
        self.queryKind=self.requestData['queryKind']
        filters = {'cost': GetStuByCostFixed, 'sleep': GetStuBySleepFixed, 'score': GetStuByScoreFixed,
                   'study': GetStuByStudyInfo}  # 过滤器字典
        filtersOrder=['study','score','sleep','cost']   #过滤器过滤顺序，安排合适能加快过滤速度

        filterFlagKey={'score':'isUpdataScoreFlag','sleep':'isUpdataSleepFlag',\
                       'cost':'isUpdataCostFlag'}
        for one in self.queryKind['kinds']:
            if one in filterFlagKey.keys():
                if getFlagValue(filterFlagKey[one]) != '0' or getFlagValue('isDeleteFlag') != '0':  # 当前在更新
                    return {'status': 0, 'errorInfo': "数据正在更新中，请稍后再试", 'data': ''}


        if self.queryKind['type']=='single':
            kinds=self.queryKind['kinds']
            return filters[kinds]().entry(self.requestData)
        else:
            inRoleStu = getClassOrStuByUser(self.requestData['userId'], 1)
            self.inRoleStuDf = pd.DataFrame(inRoleStu)
            self.selectStuIds = list(self.inRoleStuDf['stuID'])

            #责任链模式
            for one in filtersOrder:
                if one in self.queryKind['kinds']:
                    self.selectStuIds = filters[one]().entry(self.requestData, self.selectStuIds)
                    # print(len(self.selectStuIds))
                    if len(self.selectStuIds) == 0:
                        break

            resultData = self.inRoleStuDf[self.inRoleStuDf['stuID'].isin(self.selectStuIds)]
            return combineModel(resultData.to_dict('record'))