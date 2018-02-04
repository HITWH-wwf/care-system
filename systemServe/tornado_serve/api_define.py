# coding=utf8

# Index Page API


myurl='http://127.0.0.1:8002/getabnormalstu'

users = [
  {'name':'root','pwd':'123456'},
  {'name':'root','pwd':'wf520..' },
  {'name':'root','pwd':'Huawei@123'},
  {'name':'root','pwd':'nslab'},
]


class change_user_pwd():
    def entry():
        pass

class grow_line():

    def entry():
        pass

class update_focus():
    def entry():
        pass

class grow_bar():
    def entry():
        pass


class focus_table():
    def entry():
        pass

# Personal Page API


class static_info():
    def entry():
        pass


class person_trip():
    def entry():
        pass

class person_score():
    def entry():
        pass

class person_card():
    def entry():
        pass


class cancel_focus():
    def entry():
        pass


class add_focus():
    def entry():
        pass

class get_event():
    def entry():
        pass

class add_event():
    def entry():
        pass

# Office Page API


class export():
    def entry():
        pass


class suggestion():
    def entry():
        pass

# System Admin Page API


class get_total_user_team():
    def entry():
        pass


class get_one_user_team():
    def entry():
        pass


class set_one_user_team():
    def entry():
        pass


class del_one_user_team():
    def entry():
        pass

class add_one_user_team():
    def entry():
        pass

#---------------------------------------


class get_total_role_team():
    def entry():
        pass


class get_one_role_team():
    def entry():
        pass


class set_one_role_team():
    def entry():
        pass


class del_one_role_team():
    def entry():
        pass


class add_one_role_team():
    def entry():
        pass
#-------------------------------------


class get_total_user():
    def entry():
        pass


class get_one_user():
    """
    查看一个用户的基本信息，前端发来的信息为：
    "userId":"admin",
    "userName":"用户一",
    本函数接收该信息，判断userId用户是否拥有查看权限，并按权限查询结果返回：
    {
    "status":1,//1表示成功，0表示失败
    "errorInfo":"用户没有权限查看",//status为0时，前端展示errorinfo
    "data":{
        "userName":"用户一",
        "description":"巴拉巴拉",
        "userTeam":"用户组一",
        "roleTeam":"角色组一"
        }
    }
    """
    def entry():
        pass


class set_one_user():
    """
    设定一个用户的信息，前端发来的信息为：
    "userId": "admin",
    "userName": "用户一",
    "data": {
        "userName": "用户一",
        "description": "巴拉巴拉",
        "userTeam": "用户组一",
        "roleTeam": "角色组一",
        "oldPassWord": "1234", //oldPassWord与newPassword成对出现。如果在data中没有该关键字，则表示不需要修改密码。
        "newPassWord": "6789"
    }
    本函数接收该信息，判断userId用户是否拥有设定权限，并按权限查询结果返回：
    {
    "status": 1, //1表示成功，0表示失败
    "errorInfo": "用户没有权限设置", //status为0时，前端展示errorinfo
    }
    """
    def entry():
        pass


class del_one_user():
    def entry():
        pass


class add_one_user():
    """
    添加一个用户，前端发送来的信息为：
    "userId": "admin",
    "data": {
        "userName": "用户三",
        "description": "巴拉巴拉",
        "userTeam": "用户组一",
        "roleTeam": "角色组一",
        "passWord": "1234",
    }
    本函数接收该信息，判断userId用户是否拥有该权限并根据结果将其添加入库，返回：
    {
    "status": 1, #1表示成功，0表示失败
    "errorInfo": "用户没有权限设置", #status为0时，前端展示errorinfo
    }
    """
    def entry():
        pass

# Data Maintain Page API


class update_basic():
    def entry():
        pass


class update_score():
    def entry():
        pass

# Login Page API for session and Login


class login_if_pass():
    def entry():
        pass


class login_session():
    def entry():
        pass


class get_abnormal_stu():
    def entry():
        pass


class get_user_role():
    def entry():
        pass
