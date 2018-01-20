#coding=utf8

from tornado_serve.orm import *
import pandas as pd
'''
selectModel=0   返回该用户所管理的班级列表
selectModel=1   返回该用户所管理的班级下的学生名单，如果有限制班级，则返回限制班级下的学生名单
学生名单包含学生基本信息：学号，姓名，专业
'''
def getClassOrStuByUser(username,selectModel,limitClass=None):
    try:
        #先获取用户组号
        userteamid_list = MyBaseModel.returnList(new_users.select(new_users.userteamname).where(new_users.username == username).dicts(), key = "userteamname")
        if len(userteamid_list) != 1:
            return False, "未找到该用户"
        #再获得权限
        permission = MyBaseModel.returnList(new_user_team.select(new_user_team.permission).where(new_user_team.userteamname == userteamid_list[0]).dicts(), key = "permission")
        if len(permission) != 1:
            return False, "未找到该用户的用户组权限"
        permission = eval(permission[0])
        userManageClass=[classnum for classnum in permission.keys() if permission[classnum]==1]

        if selectModel==0:
            return userManageClass  #返回用户管理下的班级列表


        if limitClass!=None:    #根据限制班级的返修，修改管理班级的范围
            userManageClass=[classnum for classnum in limitClass if classnum in userManageClass]

        #一次获取所有学生数据,通过学生的班号来逐个判断是False还是True
        data_total = pd.DataFrame(MyBaseModel.returnList(stu_basic_info.select( stu_basic_info.stuID,stu_basic_info.stuName, stu_basic_info.specialitiesid, stu_basic_info.stuClassNumber).dicts()))
        class_num_list = data_total["stuClassNumber"].tolist()

        compare_index = [False] * len(data_total.index)
        for index, con in enumerate(class_num_list):
            try:

                if str(class_num_list[index]) in userManageClass:
                    compare_index[index] = True     #该同学处于此老师的管理下
            except:
                continue

        data_total.dropna(axis=1, inplace=True)
        data_total=data_total[compare_index].to_dict("report")
        majorTotal = pd.DataFrame(MyBaseModel.returnList(school_specialities_info.select(school_specialities_info.specialitiesid,
                                            school_specialities_info.specialities)))
        majorTotal.index = majorTotal["specialitiesid"]
        majors = majorTotal["specialities"].to_dict()
        for i in range(len(data_total)):
            try:
                data_total[i]['major']=majors[data_total[i]['specialitiesid']]
            except:
                data_total[i]['major']='查询不到该学生专业'

        return data_total
    except:
        raise



