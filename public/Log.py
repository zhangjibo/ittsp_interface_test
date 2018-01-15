import os
import logging
import time
import threading
from public import ReadConfig


class Log:
    def __init__(self):
        # 设置日志目录
        self.resultPath = os.path.join(ReadConfig.proDir, "results")
        if not os.path.exists(self.resultPath):
            os.mkdir(self.resultPath)
        self.logPath = os.path.join(self.resultPath, time.strftime('%Y%m%d%H%M', time.localtime(time.time())))
        if not os.path.exists(self.logPath):
            os.mkdir(self.logPath)
        # 初始化
        self.logger = logging.getLogger()
        # 设置日志级别
        self.logger.setLevel(logging.INFO)
        # 创建一个FileHandler，用于写入日志文件
        fh = logging.FileHandler(os.path.join(self.logPath, "output.log"))
        # 设置日志格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(filename)s - %(funcName)s - '
                                      '%(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
        # 给logger添加handler
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    def get_logger(self):
        """
        get logger
        :return:
        """
        return self.logger

    def build_start_line(self, case_no):
        """
        write start line
        :return:
        """
        self.logger.info("--------" + case_no + " START--------")

    def build_end_line(self, case_no):
        """
        write end line
        :return:
        """
        self.logger.info("--------" + case_no + " END--------")

    def build_case_line(self, case_name, **json):
        """
        write test case line
        :param case_name:
        :param code:
        :param msg:
        :return:
        """
        self.logger.info(case_name + " - json:" + str(json))

    def get_report_path(self):
        """
        get report file path
        :return:
        """
        report_path = os.path.join(self.logPath, "report.html")
        return report_path

    def get_result_path(self):
        """
        get test result path
        :return:
        """
        return self.logPath

    def write_result(self, result):
        """

        :param result:
        :return:
        """
        result_path = os.path.join(self.logPath, "report.txt")
        fb = open(result_path, "wb")
        try:
            fb.write(result)
        except FileNotFoundError as ex:
            self.logger.error(str(ex))


class MyLog:
    log = None
    mutex = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    def get_log():

        if MyLog.log is None:
            MyLog.mutex.acquire()
            MyLog.log = Log()
            MyLog.mutex.release()

        return MyLog.log

if __name__ == '__main__':
    log = MyLog.get_log()
    log.build_case_line("instruct", **{'status': 200, 'text': '-1531917099'})
    # logger = log.get_logger()
    # logger.debug("test debug")
    # logger.info("test info")