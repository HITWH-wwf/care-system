#coding=utf8

import sys
sys.path.append("..")

import redis
import orm
# import watch_redis
# m_redis = watch_redis.m_redis
from get_total_class import getTotalClass

def getIdFromRoleTeam(page):
    """给一个页面名，函数返回该页面名对应的id，若未找到，返回0"""
    this_id = orm.MyBaseModel.returnList(orm.new_user_role.select(orm.new_user_role.id).where(orm.new_user_role.userrolename == page).dicts())
    if len(this_id) != 1:
        return 0
    else:
        return this_id[0]

def getRoleTeamFromId(pageid):
    """给一个页面id，函数返回该页面id对应的页面名，若未找到，返回False"""
    this_page = orm.MyBaseModel.returnList(orm.new_user_role.select(orm.new_user_role.userrolename).where(orm.new_user_role.id == pageid).dicts())
    if len(this_page) != 1:
        return False
    else:
        return this_page[0]
