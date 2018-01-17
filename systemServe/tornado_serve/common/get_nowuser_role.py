#coding=utf8

import sys
sys.path.append("..")
from tornado.orm import *

def getNowUserRole(userId):
    nowuser =MyBaseModel.returnList(new_users.select().where(new_users.username == userId))
    assert len(nowuser)==1,'搜索不到该用户名'
    nowRole=MyBaseModel.returnList(new_user_role.select().where(new_user_role.userrolename==nowuser[0].userrolename))
    assert len(nowRole)==1,'搜索不到该用户对应的角色组'
    roles=nowRole[0]['permission']
    user_roles={}
    user_roles['indexMajor']=roles['indexmajor']
    user_roles['indexStudents']=roles['indexstudents']
    user_roles['person']=roles['person']
    user_roles['officeDataExpore']=roles['officedataexpore']
    user_roles['officeSuggestions']=roles['officesuggestions']
    user_roles['systemUserTeam']=roles['systemuserteam']
    user_roles['systemUsers']=roles['systemusers']
    user_roles['systemRoleTeam']=roles['systemroleteam']
    user_roles['dataUpdateBasic']=roles['dataupdatebasic']
    user_roles['dataUpdateScore']=roles['dataupdatescore']
    user_roles['dataFilter']=1       #这部分到时候数据库变化后要改
    return user_roles
