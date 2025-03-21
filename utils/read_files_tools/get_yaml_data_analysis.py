#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import os
from typing import Union, Text, List

from utils import config
from utils.cache_process.cache_control import CacheHandler
from utils.other_tools.models import RequestType, Method, TestCaseEnum
from utils.other_tools.models import TestCase
from utils.read_files_tools.yaml_control import GetYamlData
from utils.other_tools.handle_excel import HandleExcel
from utils.other_tools.handle_parameterize import Parameterize

class CaseDataCheck:
    """
    yaml 数据解析, 判断数据填写是否符合规范
    """

    def __init__(self, file_path):
        self.file_path = file_path
        if os.path.exists(self.file_path) is False:
            raise FileNotFoundError("用例地址未找到")

        self.case_data = None
        self.case_id = None

    def _assert(self, attr: Text):
        assert attr in self.case_data.keys(), (
            f"用例ID为 {self.case_id} 的用例中缺少 {attr} 参数，请确认用例内容是否编写规范."
            f"当前用例文件路径：{self.file_path}"
        )

    def check_params_exit(self):
        for enum in list(TestCaseEnum._value2member_map_.keys()):
            if enum[1]:
                self._assert(enum[0])

    def check_params_right(self, enum_name, attr):
        _member_names_ = enum_name._member_names_
        assert attr.upper() in _member_names_, (
            f"用例ID为 {self.case_id} 的用例中 {attr} 填写不正确，"
            f"当前框架中只支持 {_member_names_} 类型."
            f"如需新增 method 类型，请联系管理员."
            f"当前用例文件路径：{self.file_path}"
        )
        return attr.upper()

    @property
    def get_method(self) -> Text:

        return self.check_params_right(
            Method,
            self.case_data.get(TestCaseEnum.METHOD.value[0])
        )

    @property
    def get_host(self) -> Text:
        host = (
                self.case_data.get(TestCaseEnum.HOST.value[0]) +
                self.case_data.get(TestCaseEnum.URL.value[0])
        )
        return host

    @property
    def get_request_type(self):
        return self.check_params_right(
            RequestType,
            self.case_data.get(TestCaseEnum.REQUEST_TYPE.value[0])
        )

    @property
    def get_dependence_case_data(self):
        _dep_data = self.case_data.get(TestCaseEnum.DE_CASE.value[0])
        if _dep_data:
            assert self.case_data.get(TestCaseEnum.DE_CASE_DATA.value[0]) is not None, (
                f"程序中检测到您的 case_id 为 {self.case_id} 的用例存在依赖，但是 {_dep_data} 缺少依赖数据."
                f"如已填写，请检查缩进是否正确， 用例路径: {self.file_path}"
            )
        return self.case_data.get(TestCaseEnum.DE_CASE_DATA.value[0])

    @property
    def get_assert(self):
        _assert_data = self.case_data.get(TestCaseEnum.ASSERT_DATA.value[0])
        assert _assert_data is not None, (
            f"用例ID 为 {self.case_id} 未添加断言，用例路径: {self.file_path}"
        )
        return _assert_data

    @property
    def get_sql(self):
        _sql = self.case_data.get(TestCaseEnum.SQL.value[0])
        # 判断数据库开关为开启状态，并且sql不为空
        if config.mysql_db.switch and _sql is None:
            return None
        return _sql


class CaseData(CaseDataCheck):

    def case_process(self, case_id_switch: Union[None, bool] = None):
        data = GetYamlData(self.file_path).get_yaml_data()
        case_list = []
        for key, values in data.items():
            # 公共配置中的数据，与用例数据不同，需要单独处理
            if key != 'case_common':
                """判断请求类型"""
                if values['method'] == 'get':
                    pass
                """通过正则匹配对入参数据参数化处理,加密处理"""
                values_new = copy.deepcopy(values)
                # 判断是否需要做参数化
                if values_new['parameterize'] != True:
                    # headers内容参数化处理
                    try:
                        for header_param_keys,header_param_values in values_new['headers'].items():
                            if header_param_values is not None:
                                header_param_values = Parameterize.to_param(header_param_values)
                            values_new['headers'][header_param_values] = header_param_values
                    except Exception as E:
                        pass

                    # data内容参数处理
                    try:
                        for param_keys_data, param_values_data in values_new['data'].items():
                            if param_values_data is not None:
                                param_values_data = Parameterize.to_param(param_values_data)
                            values_new['data'][param_keys_data] = param_values_data
                    except Exception as E:
                        pass
                    # 替换
                    self.case_data = values_new

                # 需要参数化，excel中获取测试数据
                else:
                    excel = HandleExcel(values['sheet_name'],
                                        filename=data['case_common']['excel_file_name'])
                    excel_data = excel.read_excel_obj()
                    headers_list = []
                    data_list = []
                    assert_list = []
                    sql_list = []
                    for excel_case_data in excel_data:

                        try:
                            excel_case_data.headers.items()
                        except Exception as e:
                            data_res01 =None
                        else:
                            data_res01 = excel_case_data.headers
                            for param_keys_headers0, param_values_headers0 in excel_case_data.headers.items():
                                if param_keys_headers0 is not None:
                                    param_values_headers0 = Parameterize.to_param(param_values_headers0)
                                try:
                                    param_values_headers_eval = eval(param_values_headers0)
                                except Exception as e:
                                        data_res01[param_keys_headers0] = param_values_headers0
                                else:
                                    if isinstance(param_values_headers_eval, list) :
                                        data_res01[param_keys_headers0] = param_values_headers_eval
                                    elif isinstance(param_values_headers_eval,int):
                                        data_res01[param_keys_headers0] = param_values_headers0
                        headers_list.append(data_res01)

                        try:
                            excel_case_data.data.items()
                        except Exception as e:
                            data_res02 =None
                        else:
                            data_res02 = excel_case_data.data
                            for param_keys_data0, param_values_data0 in excel_case_data.data.items():
                                if param_keys_data0 is not None:
                                    param_values_data0 = Parameterize.to_param(param_values_data0)
                                try:
                                    param_values_data_eval = eval(param_values_data0)
                                except Exception as e:
                                    data_res02[param_keys_data0] = param_values_data0
                                else:
                                    if isinstance(param_values_data_eval, list):
                                        data_res02[param_keys_data0] = param_values_data_eval
                                    elif isinstance(param_values_data_eval, int):
                                        data_res02[param_keys_data0] = param_values_data0
                        data_list.append(data_res02)

                        assert_list.append(excel_case_data.assert_data)
                        sql_list.append(excel_case_data.sql)

                    res_headers = {}
                    for headers_keys, headers_values in list(enumerate(headers_list)):
                        headers_key = '{}'.format(headers_keys)
                        res_headers[headers_key] = headers_values

                    res_data = {}
                    for data_keys, data_values in list(enumerate(data_list)):
                        data_key = '{}'.format(data_keys)
                        res_data[data_key] = data_values

                    res_assert = {}
                    for ass_keys, ass_values in list(enumerate(assert_list)):
                        ass_key = '{}'.format(ass_keys)
                        res_assert[ass_key] = ass_values

                    res_sql = []
                    for sql_keys,sql_values in list(enumerate(sql_list)):
                        sql_values = Parameterize.to_param(sql_values)
                        if sql_values is None:
                            res_sql.append(sql_values)
                        else:
                            res_sql.append([sql_values])

                    values['headers'] = res_headers
                    values['data'] = res_data
                    values['assert'] = res_assert
                    values['sql'] = res_sql
                    values['is_param'] = True
                    self.case_data = values
                self.case_data = values
                self.case_id = key
                super().check_params_exit()
                case_date = {
                    'method': self.get_method,
                    'is_run': self.case_data.get(TestCaseEnum.IS_RUN.value[0]),
                    'url': self.get_host,
                    'detail': self.case_data.get(TestCaseEnum.DETAIL.value[0]),
                    'headers': self.case_data.get(TestCaseEnum.HEADERS.value[0]),
                    'requestType': super().get_request_type,
                    'data': self.case_data.get(TestCaseEnum.DATA.value[0]),
                    'dependence_case': self.case_data.get(TestCaseEnum.DE_CASE.value[0]),
                    'dependence_case_data': self.get_dependence_case_data,
                    "current_request_set_cache": self.case_data.get(TestCaseEnum.CURRENT_RE_SET_CACHE.value[0]),
                    "sql": self.get_sql,
                    "assert_data": self.get_assert,
                    "setup_sql": self.case_data.get(TestCaseEnum.SETUP_SQL.value[0]),
                    "teardown": self.case_data.get(TestCaseEnum.TEARDOWN.value[0]),
                    "teardown_sql": self.case_data.get(TestCaseEnum.TEARDOWN_SQL.value[0]),
                    "sleep": self.case_data.get(TestCaseEnum.SLEEP.value[0]),
                }
                if case_id_switch is True:
                    case_list.append({key: TestCase(**case_date).dict()})
                else:
                    case_list.append(TestCase(**case_date).dict())

        # print(case_list)
        return case_list


class GetTestCase:

    @staticmethod
    def case_data(case_id_lists: List):
        case_lists = []
        for i in case_id_lists:
            _data = CacheHandler.get_cache(i)
            case_lists.append(_data)

        return case_lists
