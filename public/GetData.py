# -*- coding:utf-8 -*-
#__author:Administrator
#date: 2018/1/4
import os
import json
from public.MyHttp import Http
from xlrd import open_workbook
from public import ReadConfig
from public.Log import MyLog
import requests
import time

rc = ReadConfig.ReadConfig("808_config.ini")
ht = Http()
log = MyLog.get_log()
logger = log.get_logger()


def get_xls(xls_name, sheet_name):
    """
    获取excel表中指定sheet数据，保存到列表中返回
    :param xls_name: excel文件名
    :param sheet_name: sheet表名
    :return:
    """
    cls = []
    xls_path = os.path.join(ReadConfig.proDir, "test_case_data", xls_name)
    # print(xls_path)
    file = open_workbook(xls_path)
    sheet = file.sheet_by_name(sheet_name)
    sheet_nrows = sheet.nrows
    for i in range(sheet_nrows):
        if sheet.row_values(i)[0] != u'case_name':
            cls.append(sheet.row_values(i))
    return cls


def get_json(response, key):
    """
    获取http请求，以json返回，获取指定key的value
    :param response:http请求返回
    :param key:json字典键
    :return:json_value
    """
    return_json = response.json()
    json_value = return_json[key]
    return json_value


def get_cookie():
    """
    获取cookie，
    :return: 返回一个字典
    """
    data = {"username": rc.get_bs("USERNAME"), "password": rc.get_bs("PASSWORD"), "orgCode": rc.get_bs("ORG_CODE")}
    session = requests.session()
    login_url = "http://%s:%s%s" % (rc.get_bs("IP"), rc.get_bs("POST"), rc.get_interface_url("login"))
    result = session.post(login_url, data=data)
    cookies = requests.utils.dict_from_cookiejar(session.cookies)
    return cookies["JSESSIONID"]


def get_until(vid, rollcallId, timout, session_id, frequency=1):
    """
    定时查寻指令反馈结果
    :param id: vehicleRollCallID
    :param timout:超时时间
    :param frequency:查询频率
    :return:指定反馈
    """
    # 获取指令反馈接口
    ht.set_url(rc.get_interface_url("getrefreshListByVids"))
    # session_id = get_cookie()["JSESSIONID"]
    ht.set_headers({"ocde": "0", "username": "system", "password": "system%40123", "orgCode": "B"
                    , "JSESSIONID": session_id, "TOPMENU": "%2Fhome.do"})
    ht.set_data({"vids": vid, "rollcallId": rollcallId})
    end_time = time.time() + timout
    while True:
        response = ht.post()
        if response.status_code == 200:
            response_json = ht.post().json()
            try:
                if response_json[0]["result"]:
                    return response_json
            except TypeError as e:
                print(e)
            time.sleep(frequency)
            if time.time() > end_time:
                return response_json
        else:
            logger.error("地址%s的Status Code:%s" % (rc.get_interface_url("getrefreshListByVids"), response.status_code))
            return None




# print(get_until("2524", "-1514058522", 65, "4CuLEQ2Zohgdm9Osiu0mhca1NW25OyJjdvsmza9Vhj2Y6N607JVq!-1564142059"))
# print(get_xls("instruct_data.xlsx", "instruct"))
print(get_cookie())

