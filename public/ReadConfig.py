# -*- coding:utf-8 -*-
# __author:Administrator
# date: 2017/12/28
import os
import configparser

# 不要使用这种获取项目根目录的方式，如果在其它类中引用，是相对其它类的目录进行。
# proDir1 = os.path.abspath(os.path.join(os.getcwd(), ".."))

proDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
conf_path = proDir + r"\config\\"


class ReadConfig:
    """
    创建ConfigParser对象，读取指定目录conf_path配置文件config_name
    """
    def __init__(self, config_name):
        self.conf = configparser.ConfigParser()
        # 中文乱码问题需要添加encoding="utf-8-sig"
        self.conf.read(conf_path + config_name, encoding="utf-8-sig")

    def get_bs(self, name):
        value = self.conf.get("BS", name)
        return value

    def get_oracle(self, name):
        value = self.conf.get("ORACLE", name)
        return value

    def get_vehicle(self, name):
        value = self.conf.get("VEHICLE", name)
        return value

    def get_interface_url(self, name):
        value = self.conf.get("INTERFACE_URL", name)
        return value

if __name__ == '__main__':
    co = ReadConfig("808_config.ini")
    print(co.get_bs("IP"))
    print(proDir)
    # print(proDir1)



