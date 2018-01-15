# -*- coding:utf-8 -*-
#__author:Administrator
#date: 2018/1/3

import os
import unittest
from public import ReadConfig
from public.Log import MyLog
from public import HTMLTestRunner_PY3


class RunTest:
    def __init__(self):
        """
        初始化需要的参数
        :return:
        """
        global log, logger, resultPath
        # log初始化
        log = MyLog.get_log()
        self.logger = log.get_logger()
        # 定义结果保存路径
        self.resultPath = log.get_report_path()
        # 取得config\caselist.txt文件路径
        self.caseListFile = os.path.join(ReadConfig.conf_path, "caselist.txt")
        # 取得test_case文件路径
        self.caseFile = os.path.join(ReadConfig.proDir, "test_case")
        # 定义一个空列表，用于保存类名
        self.caseList = []

    def get_case_list(self):
        """
        获取config\caselist.txt中的每一行，以#号开头的除外
        且添加到列表self.caseList进行返回
        :return: self.caseList
        """
        f = open(self.caseListFile)
        for value in f.readlines():
            if value != '' and not value.startswith("#"):
                self.caseList.append(value.replace("\n", ""))
        f.close()
        return self.caseList

    def get_case_suite(self):
        """
        获取测试集
        :return:
        """
        # 获取config\caselist.txt中的每一行
        self.get_case_list()
        # 定义测试集对象
        test_suite = unittest.TestSuite()
        # 初始化一个列表，存在所有的测试模块
        suite_module = []
        # 获取className ,把所有case中测试集添加到suite_module列表中
        for case in self.caseList:
            case_name = case.split("/")[-1]
            # print(case_name + ".py")
            discover = unittest.defaultTestLoader.discover(self.caseFile, pattern=case_name + ".py", top_level_dir=None)
            suite_module.append(discover)

        # 获取列表中所有的测试模块，添加到测试集test_suite中
        if len(suite_module) > 0:
            for suite in suite_module:
                for test_name in suite:
                    test_suite.addTest(test_name)
        else:
            return None
        return test_suite

    def run(self):
        try:
            # 获取测试集
            suit = self.get_case_suite()
            print("suit:", suit)
            # 判断测试集是否为None
            if suit is not None:
                self.logger.info("********TEST START********")
                f = open(self.resultPath, 'wb')
                # 使用HTMLTestRunner输出html报告
                runner = HTMLTestRunner_PY3.HTMLTestRunner(stream=f, title='Test Report',
                                                           description='Test Description', verbosity=2)
                # 运行测试用例
                runner.run(suit)
            else:
                self.logger.info("Have no case to test.")
        except Exception as e:
            self.logger.error(str(e))
        finally:
            self.logger.info("*********TEST END*********")
            f.close()


if __name__ == '__main__':

    testRun = RunTest()
    testRun.run()
