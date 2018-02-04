#coding=utf8

# import watch_redis
import orm
import os

def getTotalClass(mode = 0):
    """
    函数返回当前用户组可能存在权限，即：返回当前数据库内所有班级
    mode=0返回一条列表
    mode=1返回字典，字典的keys为所有页面名集合，value均为0
    """
    #暂时不使用redis做缓存，直接去数据库里面取
    #m_redis = watch_redis.m_redis
    #try:
    #    ans = eval(m_redis.get("stu_total_class"))
    #except:
    #    raise("redis 内不存在stu_total_class")
    #return ans
    if mode == 0:
        class_list = orm.MyBaseModel.returnList(orm.stu_basic_info.select(orm.stu_basic_info.stuClassNumber).distinct(orm.stu_basic_info.stuClassNumber).dicts(), key = 'stuClassNumber')
        return [str(con) for con in class_list]

    elif mode == 1:
        class_dict = {}
        class_list = orm.MyBaseModel.returnList(orm.stu_basic_info.select(orm.stu_basic_info.stuClassNumber).distinct(orm.stu_basic_info.stuClassNumber).dicts(), key = 'stuClassNumber')
        for class_name in class_list:
            class_dict[str(class_name)] = 0
        return class_dict
    else:
        raise Exception("wrong mode")
