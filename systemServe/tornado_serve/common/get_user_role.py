#coding=utf8

import sys
sys.path.append("..")

import redis
import orm
# import watch_redis
# m_redis = watch_redis.m_redis
from get_total_page import getTotalPage

def getUserRole(userid):
    """给一个用户编号，函数返回该用户对应的角色组权限"""
    this_userid_team = orm.MyBaseModel.returnList(orm.new_users.select(orm.new_users.userrolename).where(orm.new_users.username == userid).dicts(), key = "userrolename")
    if len(this_userid_team) != 1:
        return False
    this_permission = orm.MyBaseModel.returnList(orm.new_user_role.select(orm.new_user_role.permission).where(orm.new_user_role.userrolename == this_userid_team[0]).dicts(), key = "permission")
    assert len(this_permission) == 1
    #转成字典形式
    this_permission = eval(this_permission[0])
    #判断是否需要增加新的页面
    the_total_page = getTotalPage()
    if set(the_total_page) != set(this_permission):
        for new_page in set(the_total_page) - set(this_permission):
            this_permission[new_page] = 0
    return this_permission
