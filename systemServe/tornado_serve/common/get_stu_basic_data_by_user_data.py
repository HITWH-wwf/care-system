#coding=utf8

import os
import orm
import pandas as pd

def getBasicDataByUserName(username):
    """
    函数返回当前该用户所在的用户组，当前能看到的所有学生基础数据，返回的内容为列表嵌套字典，字典内部key为数据库表的集合
    """
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
        # print(permission)
    except:
        raise
        # return False, "用户获取出错，请稍候重试"

    #一次获取所有学生数据,通过学生的班号来逐个判断是False还是True
    data_total = pd.DataFrame(orm.MyBaseModel.returnList(orm.stu_basic_info.select(orm.stu_basic_info.stuName, orm.stu_basic_info.sex, orm.stu_basic_info.stuID, orm.stu_basic_info.specialitiesid, orm.stu_basic_info.nationality, orm.stu_basic_info.apartmentNumber, orm.stu_basic_info.dormitoryNumber, orm.stu_basic_info.idNumber, orm.stu_basic_info.politicalLandscape, orm.stu_basic_info.stuEducation, orm.stu_basic_info.graduatedHighSchool, orm.stu_basic_info.stuMobileNumber, orm.stu_basic_info.homeMobileNumber, orm.stu_basic_info.state, orm.stu_basic_info.stuClassNumber, orm.stu_basic_info.collegeid, orm.stu_basic_info.homeAddress).dicts()))
    class_num_list = data_total["stuClassNumber"].tolist()

    compare_index = [False] * len(data_total.index)
    for index, con in enumerate(class_num_list):
        try:
            # print(permission[str(class_num_list[index])], "  in the stu_basic_data_by_user_data")
            if permission[str(class_num_list[index])] == True:
                compare_index[index] = True
        except:
            #更新了班级信息，但是没有更新对应的用户组权限
            continue
    # print(len(compare_index),"  in the stu_basic_data_by_user_data", compare_index)
    # print(data_total[compare_index])
    return True, data_total[compare_index].to_dict("report")



