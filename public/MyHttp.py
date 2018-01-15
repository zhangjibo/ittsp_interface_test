# -*- coding:utf-8 -*-
# __author:Administrator
# date: 2017/12/28
import requests
from public import ReadConfig
from public.Log import MyLog
from public.OracleOperation import MyOracle
# from public.GetData import get_cookie
rc = ReadConfig.ReadConfig("808_config.ini")


class Http:

    def __init__(self):
        self.scheme = rc.get_bs("SCHEME")
        self.ip = rc.get_bs("IP")
        self.port = rc.get_bs("POST")
        self.timeout = rc.get_bs("TIMEOUT")
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()
        self.headers = {}
        self.data = {}
        self.url = None
        self.files = {}
        self.state = 0

    def set_url(self, url):
        """
        接口路径
        :param url:
        :return:
        """
        self.url = "%s://%s:%s%s" % (self.scheme, self.ip, self.port, url)
        # print(self.url)

    def set_headers(self, header):
        """
        cookies为header中的一个键值对，所以可以在header中添加
        :param header:
        """
        self.headers = header

    def set_data(self, data):
        """
        传的参数json\params等
        :param data:
        :return:
        """
        self.data = data

    def get(self):
        """
        get请求
        :return:
        """
        try:
            # 当headers传的cookies时，要把键值对id改成cookies
            response = requests.get(self.url, cookies=self.headers, timeout=float(self.timeout))
            return response
        except TimeoutError as e:
            self.logger.error(e)
            return None

    def post(self):
        """
        post请求
        :return:
        """
        try:
            # 当headers传的cookies时，要把键值对id改成cookies
            response = requests.post(self.url, cookies=self.headers, data=self.data, timeout=float(self.timeout))
            return response
        except TimeoutError as e:
            self.logger.error(e)
            return None


if __name__ == '__main__':
    # ht = Http()
    # ht.set_url(rc.get_interface_url("instructTypeParam"))
    # print(ht.url)
    #
    # # session_id = get_cookie()["JSESSIONID"]
    #
    # ht.set_headers({"ocde": "0", "username": "system", "password": "system%40123", "orgCode": "B",
    #                 "JSESSIONID": "n7UI0CUZnu70hhwC0lgorbLquqdEN30iDKRPzxcH2VX9NEtSXifs!-1564142059", "TOPMENU": "%2Fhome.do"})
    # print(ht.headers)
    #
    # orc = MyOracle()
    # sql = "SELECT VEHICLE_ID FROM V_VEHICLEINFO WHERE ID_NUMBER  LIKE '%s'" % rc.get_vehicle("ID_NUMBER")
    # vid = orc.executeSQL(sql)
    #
    # str_vid = orc.get_one(vid)
    # print("string:", str(str_vid))
    # vehicleIds = str_vid[0]
    #
    # ht.set_data({"vehicleIds": vehicleIds, "cmdCode": "1", "cmdVal": "1", "sendTitle": "点名", "paramCode": "param",
    #              "paramName": "", "id": "Z1000101"})
    # print(ht.data)
    #
    # # 获取结果的json(),可以像字典一样取值
    # d_res = ht.post().json()
    # print(d_res)
    # print(d_res["status"])
    # # 再把status传到另一个接口中获取数据
    # print(d_res["text"])



    ht = Http()
    ht.set_url(rc.get_interface_url("instructTypeParam"))
    ht.set_headers({"ocde": "0", "username": "system", "password": "system%40123", "orgCode": "B"
                    , "JSESSIONID": "LrKMJ9rCUZZPYt0Mp4veUaKvRYRcWqQqwWVlvAVsQlJ0vyYFiPIv!-1564142059", "TOPMENU": "%2Fhome.do"})
    ht.set_data({"vehicleIds": "52100001", "cmdCode": "1", "cmdVal": "1", "sendTitle": "点名", "paramCode": "param",
                 "paramName": "", "id": "Z1000101"})
    # res = ht.post()
    # status = res.status_code
    # print(type(status))

    res = ht.post().json()
    print(res)
