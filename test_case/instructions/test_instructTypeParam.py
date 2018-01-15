import unittest
import paramunittest
from public import ReadConfig
from public.Log import MyLog
from public.MyHttp import Http
from public.GetData import get_xls
from public.OracleOperation import MyOracle
from public.GetData import get_cookie
from public.GetData import get_until

rc = ReadConfig.ReadConfig("808_config.ini")
h = Http()
orc = MyOracle()
instrBackRecordJsonList_xls = get_xls("instruct_data.xlsx", "instruct")
print(instrBackRecordJsonList_xls)


@paramunittest.parametrized(*instrBackRecordJsonList_xls)
class TestInstructTypeParam(unittest.TestCase):
    def setParameters(self, case_name, method, vehicleIds, cmdCode, cmdVal, sendTitle, paramCode, paramName, Id):
        self.case_name = str(case_name)
        self.method = str(method)
        self.vehicleIds = str(vehicleIds)
        self.cmdCode = str(cmdCode)
        self.cmdVal = str(cmdVal)
        self.sendTitle = str(sendTitle)
        self.paramCode = str(paramCode)
        self.paramName = str(paramName)
        self.Id = str(Id)
        self.return_json = None
        self.result_json = None
        self.session_id = get_cookie()

    def description(self):
        """
        描述
        :return:
        """
        self.case_name

    def setUp(self):
        """
        测试用例开始前布置环境，查询车辆的vehicleId，记录日志
        :return:
        """
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()
        sql = "SELECT VEHICLE_ID FROM V_VEHICLEINFO WHERE ID_NUMBER  LIKE '%s'" % rc.get_vehicle("ID_NUMBER")
        vid = orc.executeSQL(sql)
        self.vehicleIds = orc.get_one(vid)[0]
        print(self.vehicleIds)

    def test_Instruct(self):
        # 1、设置url
        url = rc.get_interface_url("instructTypeParam")
        h.set_url(url)

        # self.session_id = "Thp26DXAKwSrjGroUXpFD9lPwbV698WQVYT0KPi6vKK72MEeAuGY!-1564142059"
        # 2、设置header
        header = {"ocde": "0", "username": "system", "password": "system%40123", "orgCode": "B", "JSESSIONID": self.session_id
                  , "TOPMENU": "%2Fhome.do"}
        h.set_headers(header)
        # 3、设置data，请求参数
        data = {"vehicleIds": self.vehicleIds, "cmdCode": self.cmdCode, "cmdVal": self.cmdVal,
                "sendTitle": self.sendTitle, "paramCode": self.paramCode, "paramName": self.paramName,
                "id": self.Id}
        h.set_data(data)
        # 4、发送请求
        res = h.post()
        if res.status_code == 200:
            self.return_json = h.post().json()
            print(self.return_json)
            # 5、检查结果
            # 先获取指令反馈结果，调用get_until()方法
            try:
                rollcallId = self.return_json["text"]
            except TypeError as e:
                self.logger.error(e)
            self.result_json = get_until(self.vehicleIds, rollcallId, 65, self.session_id)

            self.checkResult()
        else:
            self.logger.error("地址%s的Status Code:%s" % (url, res.status_code))

    def checkResult(self):
        if self.result_json:
            if self.result_json[0]["result"] == 0:
                msg = "指令(%s)：成功！终端返回信息：[%s]" % (self.case_name, self.result_json[0]["backInfo"])
            elif self.result_json[0]["result"] == 1:
                msg = "指令(%s)：超时！终端返回信息：[%s]" % (self.case_name, self.result_json[0]["backInfo"])
            else:
                msg = "指令(%s)：未发送！终端返回信息：[%s]" % (self.case_name, self.result_json[0]["backInfo"])

            self.assertEqual(self.result_json[0]["result"], 0, msg=msg)

    def tearDown(self):
        # 用例执行后把self.return_json记录要日志中
        self.log.build_case_line(self.case_name, **self.return_json)

if __name__ == '__main__':
    # 在unittest.main()中加 verbosity 参数可以控制输出的错误报告的详细程度，默认是 1，
    # 如果设为 0，则不输出每一用例的执行结果，即没有上面的结果中的第1行；如果设为 2，则输出详细的执行结果

    unittest.main(verbosity=2)
