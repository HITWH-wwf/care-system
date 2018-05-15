#coding=utf-8
from tornado_serve.orm import MyBaseModel,stu_all_aspect_info
from tornado_serve.common.deal_data_by_redis import getValue
from tornado_serve.common.judge_permission import judgeIfPermiss

class GetFudaoyuanActionHistory(object):
    def entry(self,receiveRequest):
        self.requestData = eval(receiveRequest.request.body)
        userName = getValue(self.requestData['sessionId'])
        # self.requestData=receiveRequest
        stuId=self.requestData['stuId']
        # userName='wangjianting'
        if userName == None:
            return {'status': 0, 'errorInfo': '登陆状态已过期，请重新登录'}
        elif judgeIfPermiss(user_id=userName, mode=1, page="personStudyInfo") == False:
            return {"status": 0, "errorInfo": "用户没有操作此页面的权限"}
        elif judgeIfPermiss(user_id = userName, stuid = stuId, mode = 0) == False:
            return {"status":0, "errorInfo":"用户没有操作该学生的权限"}
        else:
            thisStu=MyBaseModel.returnList(stu_all_aspect_info.select(stu_all_aspect_info.fudaoyuan).where(stu_all_aspect_info.stuID==stuId))
            if len(thisStu)==0:
                return {'status':0,'errorInfo':'查询不到该学生的相关记录'}
            thisStu=thisStu[0]
            tableData=eval(thisStu['fudaoyuan'])
            return {
                    "status": 1,
                    "colName": ['时间', '操作的用户名','采取措施'],
                    "propName": ['time', 'editUser', 'content'],
                    "tableData": tableData,
                    "info": '请求成功'
                }