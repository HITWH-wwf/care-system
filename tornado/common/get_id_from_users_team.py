#coding=utf8

import sys
sys.path.append("..")

# import redis
import orm
# import watch_redis
# m_redis = watch_redis.m_redis
from get_total_class import getTotalClass

def getIdFromUsersTeam(username):
    """给一个用户名组，函数返回该用户组名对应的id，若未找到，返回0"""
    this_id = orm.MyBaseModel.returnList(orm.new_user_team.select(orm.new_user_team.id).where(orm.new_user_team.userteamname == username).dicts())
    if len(this_id) != 1:
        return 0
    else:
        return this_id[0]

def getUsersTeamFromId(usernameid):
    """给一个用户名组，函数返回该用户组名对应的id，若未找到，返回False"""
    userteamname = orm.MyBaseModel.returnList(orm.new_user_team.select(orm.new_user_team.userteamname).where(orm.new_user_team.id == usernameid).dicts())
    if len(userteamname) != 1:
        return False
    else:
        return userteamname[0]
