#coding=utf8

# import watch_redis
import os
import configparser

def getTotalPage(mode = 0):
    """
    函数返回当前角色组可能存在权限，即：返回当前系统的所有页面名
    mode=0返回一条列表
    mode=1返回字典，字典的keys为所有页面名集合，value均为0
    """
    #m_redis = watch_redis.m_redis
    #try:
    #    ans = eval(m_redis.get("stu_total_page"))
    #except:
    #    raise("redis 内不存在stu_total_page")
    #return ans
    file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/ini/page.ini"
    text = configparser.ConfigParser()
    text.read(file_path, encoding = "GBK")
    if "page" not in text.sections():
        assert ("error:page.ini不识别，未查询到page标签") == 0
    if mode == 0:
        page_list = []
        for con in text["page"]:
            page_list.append(con)
        return page_list
    elif mode == 1:
        page_dict = {}
        for con in text["page"]:
            page_dict[con] = 0
        return page_dict
    else:
        assert ("wrong mode") == 0
