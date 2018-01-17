#coding=utf8

import orm
import pandas as pd
'''
selectModel=0   返回该用户所管理的班级列表
selectModel=1   返回该用户所管理的班级下的学生名单，如果有限制班级，则返回限制班级下的学生名单
'''
def getClassOrStuByUser(username,selectModel,limitClass=None):
    try:
        #先获取用户组号
        userteamid_list = orm.MyBaseModel.returnList(orm.new_users.select(orm.new_users.userteamname).where(orm.new_users.username == username).dicts(), key = "userteamname")
        if len(userteamid_list) != 1:
            return False, "未找到该用户"
        #再获得权限
        permission = orm.MyBaseModel.returnList(orm.new_user_team.select(orm.new_user_team.permission).where(orm.new_user_team.userteamname == userteamid_list[0]).dicts(), key = "permission")
        if len(permission) != 1:
            return False, "未找到该用户的用户组权限"
        permission = eval(permission[0])
        userManageClass=[classnum for classnum in permission.keys() if permission[classnum]==1]

        if selectModel==0:
            return userManageClass  #返回用户管理下的班级列表


        if limitClass!=None:    #根据限制班级的返修，修改管理班级的范围
            userManageClass=[classnum for classnum in limitClass if classnum in userManageClass]

        #一次获取所有学生数据,通过学生的班号来逐个判断是False还是True
        data_total = pd.DataFrame(orm.MyBaseModel.returnList(orm.stu_basic_info.select(orm.stu_basic_info.stuName, orm.stu_basic_info.sex, orm.stu_basic_info.stuID, orm.stu_basic_info.specialitiesid, orm.stu_basic_info.nationality, orm.stu_basic_info.apartmentNumber, orm.stu_basic_info.dormitoryNumber, orm.stu_basic_info.state, orm.stu_basic_info.stuClassNumber, orm.stu_basic_info.collegeid).dicts()))
        class_num_list = data_total["stuClassNumber"].tolist()

        compare_index = [False] * len(data_total.index)
        for index, con in enumerate(class_num_list):
            try:

                if str(class_num_list[index]) in userManageClass:
                    compare_index[index] = True     #该同学处于此老师的管理下
            except:
                continue

        return data_total[compare_index].to_dict("report")

    except:
        raise


