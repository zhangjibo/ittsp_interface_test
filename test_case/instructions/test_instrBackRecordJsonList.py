# -*- coding:utf-8 -*-
#__author:Administrator
#date: 2018/1/4

import unittest
import paramunittest
from public.GetData import get_xls
instrBackRecordJsonList_xls = get_xls("instruct_data.xlsx", "instruct")
print(instrBackRecordJsonList_xls)


@paramunittest.parametrized(*instrBackRecordJsonList_xls)
class TestInter(unittest.TestCase):
    def setParameters(self, case_name, method, v_id, cmd_code, cmd_val, send_title, param_code, param_name, Id, status):
        self.case_name = str(case_name)
        self.method = str(method)
        self.vehicleIds = str(v_id)
        self.cmdCode = str(cmd_code)
        self.cmdVal = str(cmd_val)
        self.sendTitle = str(send_title)
        self.paramCode = str(param_code)
        self.paramName = str(param_name)
        self.Id = str(Id)
        self.status = str(status)

    def test_add(self):
        """比较a,b"""
        self.assertEqual(self.case_name, '点名')


if __name__ == '__main__':
    # 在unittest.main()中加 verbosity 参数可以控制输出的错误报告的详细程度，默认是 1，
    # 如果设为 0，则不输出每一用例的执行结果，即没有上面的结果中的第1行；如果设为 2，则输出详细的执行结果
    unittest.main(verbosity=2)