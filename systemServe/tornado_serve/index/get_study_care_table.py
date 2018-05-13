#coding=utf-8
from tornado_serve.orm import stu_all_aspect_info,MyBaseModel
from tornado_serve.common.judge_permission import judgeIfPermiss
from tornado_serve.common.deal_data_by_redis import getValue
from tornado_serve.common.get_class_or_stu_by_user import getClassOrStuByUser
import pandas as pd
'''
关于stu_all_aspect_info表中stuState字段的值说明
0：取消关注状态    1：学情关注
2：修改未提交      3：取消未通过
4：关注未通过      5：取消待审核
6：关注待审核
'''
class GetStudyCareTable(object):
    def entry(self,receiveRequest):
        self.requestData = eval(receiveRequest.request.body)
        userName = getValue(self.requestData['sessionId'])
        # userName='wangjianting'
        if userName == None:
            return {'status': 0, 'errorInfo': '登陆状态已过期，请重新登录'}
        if judgeIfPermiss(user_id=userName, mode=1, page="studyInfoStu") == False:
            return {"status": 0, "errorInfo": "用户没有操作此页面的权限"}
        else:
            inRoleStu = getClassOrStuByUser(userName, 1)
            self.inRoleStuDf = pd.DataFrame(inRoleStu)
            self.selectStuIds = list(self.inRoleStuDf['stuID'])
            self.inRoleStuDf.index=self.inRoleStuDf['stuID']
            stuBasicInfo=self.inRoleStuDf.to_dict('index')
            self.resultStu=MyBaseModel.returnList(stu_all_aspect_info.select(stu_all_aspect_info.stuID,stu_all_aspect_info.stuState).where(\
                    stu_all_aspect_info.stuID.in_(self.selectStuIds) and stu_all_aspect_info.stuState > 0).order_by(stu_all_aspect_info.stuState.desc(),
                                                    stu_all_aspect_info.stuID.asc()))
            tableData=[]
            stuStateInfo=['学情关注','修改未提交','取消未通过','关注未通过','取消待审核','关注待审核']
            for stu in self.resultStu:
                oneStu=stuBasicInfo[stu['stuID']]
                oneStu['stuState']=stuStateInfo[stu['stuState']]
                tableData.append(oneStu)

            return {
                    "status": 1,
                    "colName": ['学号', '姓名','班级','专业','学情状态'],
                    "propName": ['stuID', 'stuName', 'stuClassNumber', 'major','stuState'],
                    "tableData": tableData,
                    "info": '请求成功'
                    }

