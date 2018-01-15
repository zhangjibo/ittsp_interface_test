# -*- coding:utf-8 -*-
# __author:Administrator
# date: 2017/12/28
import os
import cx_Oracle
from public import ReadConfig
from public.Log import MyLog

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
rc = ReadConfig.ReadConfig("808_config.ini")


class MyOracle:

    """
    oracle数据库操作
    """
    global username, password, ip, post, service_name
    username = rc.get_oracle('USERNAME')
    password = rc.get_oracle('PASSWORD')
    ip = rc.get_oracle('IP')
    post = rc.get_oracle('POST')
    service_name = rc.get_oracle('SERVICE_NAME')

    def __init__(self):
        """
        初始化
        """
        self.dns = cx_Oracle.makedsn(ip, post, service_name)
        self.conn = None
        self.cursor = None
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()

    def ReConnect(self):
        """
        建立连接
        """
        try:
            self.conn = cx_Oracle.connect(username, password, self.dns)
            self.cursor = self.conn.cursor()
            self.logger.info("Connect DB successfully!")
        except ConnectionError as e:
            self.logger.error(e)

    def closeDB(self):
        """
        关闭连接
        """
        self.conn.close()
        self.logger.info("Database closed!")
        self.conn = None

    def executeSQL(self, sql):
        """
        数据操作
        :param sql:
        :return:
        """
        self.ReConnect()
        self.cursor.execute(sql)
        self.conn.commit()
        return self.cursor

    def get_all(self, cursor):
        """
        get all result after execute sql
        :param cursor:
        :return:
        """
        value = cursor.fetchall()
        return value

    def get_one(self, cursor):
        """
        get one result after execute sql
        :param cursor:
        :return:
        """
        value = cursor.fetchone()
        return value

if __name__ == '__main__':
    test = MyOracle()
    # test.ReConnect()
    # ex = test.executeSQL("SELECT VEHICLE_ID FROM V_VEHICLEINFO WHERE ID_NUMBER  LIKE '测A22332'")
    # sql = "SELECT VEHICLE_ID FROM V_VEHICLEINFO WHERE ID_NUMBER  LIKE '%s'" % rc.get_vehicle("ID_NUMBER")
    sql = "SELECT CONTENT FROM N_INSTRBACK WHERE VEHICLE_ROLL_CALL_ID = '-1514058777'"
    ex = test.executeSQL(sql)
    # 查询结果到列表
    print(test.get_one(ex)[0])
