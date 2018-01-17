#coding=utf8
import orm

def dojob_by_mode_0(userid, stuid):
    """
    给一个用户编号加学生学号，函数通过该用户对应用户组的权限，返回True或者False，True代表该用户拥有该学生的权限，False代表该用户没有权限操作该学生，如果输入的学生id或者userid不存在，函数仍返回False
    """
    try:
        #先获取用户组名
        userteamid_list = orm.MyBaseModel.returnList(orm.new_users.select(orm.new_users.userteamname
        ).where(orm.new_users.username == userid).dicts(), key = "userteamname")
        if len(userteamid_list) != 1:
            return False
        #再获得权限
        permission = orm.MyBaseModel.returnList(orm.new_user_team.select(orm.new_user_team.permission
        ).where(orm.new_user_team.userteamname == userteamid_list[0]).dicts(), key = "permission")
        if len(permission) != 1:
            return False
        permission = eval(permission[0])
        #获得班号
        class_num = orm.MyBaseModel.returnList(orm.stu_basic_info.select(orm.stu_basic_info.stuClassNumber
        ).where(orm.stu_basic_info.stuID == stuid).dicts(), key = "stuClassNumber")[0]
    except:
        return False

    #返回鉴权结果
    if class_num in permission :
        return permission[class_num]
    elif int(class_num) in permission :
        return permission[int(class_num)]
    else:
        return False

def dojob_by_mode_1(userid, page):
    """
    给一个用户编号加页面名（'index'、‘person’、‘officeExport’等），函数通过该用户对应角色组权限，返回True或者False，True代表该用户可以看该页面，否则表示不可以。如果输入的页面名不存在，函数仍返回False
    """
    page = page.lower()
    #先获取角色组号
    userrolename = orm.MyBaseModel.returnList(orm.new_users.select(orm.new_users.userrolename).where(orm.new_users.username == userid).dicts(), key = "userrolename")
    if len(userrolename) != 1:
        return False
    #再获得权限
    permission = orm.MyBaseModel.returnList(orm.new_user_role.select(orm.new_user_role.permission).where(orm.new_user_role.userrolename == userrolename[0]).dicts(), key = "permission")
    permission = eval(permission[0])
    #返回鉴权结果
    if page in permission :
        return permission[page]
    else:
        return False

def judgeIfPermiss(user_id = None, stuid = None, page = None, mode = 0):
    """
    mode为0时：给一个用户编号加学生学号，函数通过该用户对应用户组的权限，返回True或者False，True代表该用户拥有该学生的权限，False代表该用户没有权限操作该学生，如果输入的学生id或者userid不存在，函数仍返回False
    mode为1时：给一个用户编号加页面名（'index'、‘person’、‘officeExport’等），函数通过该用户对应角色组权限，返回True或者False，True代表该用户可以看该页面，否则表示不可以。如果输入的页面名不存在，函数仍返回False
    """
    if mode == 0:
        return dojob_by_mode_0(user_id, stuid)
    elif mode == 1:
        return dojob_by_mode_1(user_id, page)
    else:
        raise Exception("wrong mode in judgeIfPermiss")
