#coding=utf8

import sys
sys.path.append("..")

# import redis
import orm
# import watch_redis
# m_redis = watch_redis.m_redis
from get_total_class import getTotalClass

def getTeam(userid):
    """给一个用户编号，函数返回该用户对应的用户组权限"""
    this_userid_team = orm.MyBaseModel.returnList(orm.new_users.select(orm.new_users.userteamid).where(orm.new_users.username == userid).dicts())
    if len(this_userid_team) != 1:
        return False
    this_permission = orm.MyBaseModel.returnList(orm.new_user_team.select(orm.new_user_team.permission).where(orm.new_user_team.id == this_userid_team[0]).dicts())
    assert len(this_permission) == 1
    #转成字典形式
    this_permission = eval(this_permission)

    #判断是否需要增加新的班级
    the_total_class = getTotalClass()
    if set(the_total_class) != set(this_permission):
        for new_class in set(the_total_class) - set(this_permission):
            this_permission[new_class] = 0
    return this_permission
