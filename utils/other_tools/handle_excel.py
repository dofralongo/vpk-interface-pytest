"""
====================
@Time:  2023/7/516:24
@Author: test_007
@File:  handle_excel_01.py
====================
"""
import os
import openpyxl
from utils.other_tools.handle_yaml import do_yaml
from utils.other_tools.handle_path import CONFIG_FILES
from utils.other_tools.handle_path import CONFIG_TEST_CASE_PARAMETER


class CaseDate:
    pass


class HandleExcel(object):
    """封装excel读写的类"""

    def __init__(self, sheet_name, filename=None):
        self.sheet_name = sheet_name
        if filename is not None:
            self.filename = os.path.join(CONFIG_TEST_CASE_PARAMETER, filename)
            # print(self.filename)
        else:
            self.filename = os.path.join(CONFIG_TEST_CASE_PARAMETER,
                                         do_yaml.yaml_read('case_common', 'excel_file_name'))

    def open(self):
        self.wb = openpyxl.load_workbook(self.filename)
        self.sh = self.wb[self.sheet_name]

    def read_excel_obj(self):
        self.open()
        case_datas = []
        rows = list(self.sh.rows)
        datas_title = ['case_name', 'headers', 'data', 'assert_data', 'sql']
        # datas_title = ['case_name', 'headers', 'data', 'assert_data']
        titles = [title_datas.value for title_datas in rows[1]]

        # 获取headers分割点session_id的下标
        try:
            headers_keyword_index = titles.index('session_id')
        except Exception as E:
            print(f'excel格式错误，缺少session_id字段,报错信息：{E}')

        # 获取assert分割点status_code的下标
        try:
            assert_keyword_index = titles.index('status_code')
        except Exception as E:
            print(f'excel格式错误，缺少status_code字段,报错信息：{E}')

        # 获取最大最大下标
        max_index = titles.index('sql')

        # 获取header键名
        header_key_name = titles[2:headers_keyword_index + 1]

        # 获取data键名
        if assert_keyword_index - headers_keyword_index > 1:
            data_key_name = titles[headers_keyword_index + 1:assert_keyword_index]
        else:
            data_key_name = None

        # 获取status_title键名
        status_key_name = titles[assert_keyword_index]

        # 获取assert键名
        # assert_key_names = []
        # num = 0
        #
        # while assert_keyword_index + num + 6 <= max_index:
        #     try:
        #             assert_key_name = titles[assert_keyword_index+num+1:assert_keyword_index+num+6]
        #     except Exception as E:
        #         break
        #     finally:
        #         assert_key_names.append(assert_key_name)
        #         num += 5

        # 获取sql
        sql_key_name = titles[-1]


        for datas in rows[2:]:
            case_params = [data.value for data in datas]
            if case_params[0] is None:
                break
            # 测试数据列表
            cases_datas_list = []
            cases_datas_list.append(case_params[1])

            # 处理headers
            case_headers_data = [data for data in case_params[2:headers_keyword_index + 1]]
            case_headers_data_dict = dict(zip(header_key_name, case_headers_data))
            cases_datas_list.append(case_headers_data_dict)

            # 处理data
            if assert_keyword_index - headers_keyword_index > 1:
                case_data_data = [data for data in case_params[headers_keyword_index + 1:assert_keyword_index]]
                case_data_data_dict = dict(zip(data_key_name, case_data_data))
            else:
                case_data_data_dict = None
            cases_datas_list.append(case_data_data_dict)

            # 处理sql
            # case_sql_data = []
            # case_sql_data.append(case_params[-1])
            # case_sql_data_dict = dict(zip(list(sql_key_name), case_sql_data))
            # cases_datas_list.append(case_sql_data_dict)

            # 处理status_code
            case_assert_dict = {}
            case_assert_dict[status_key_name] = case_params[assert_keyword_index]

            num = 0
            while assert_keyword_index + num + 6 <= max_index:
                data_ele = case_params[assert_keyword_index + num + 1]
                if data_ele is None:  # @ldj
                    break
                else:
                    try:
                        titles[assert_keyword_index + num + 2:assert_keyword_index + num + 6]
                    except Exception as E:
                        break
                    else:
                        assert_data = titles[assert_keyword_index + num + 2:assert_keyword_index + num + 6]
                        datas_data = case_params[assert_keyword_index + num + 2:assert_keyword_index + num + 6]
                        datas_data[2] = str(datas_data[2])
                        assert_datas = dict(zip(assert_data, datas_data))
                        case_assert_dict[data_ele] = assert_datas
                        num += 5
            cases_datas_list.append(case_assert_dict)

            if case_params[-1] is not None:
                cases_datas_list.append(case_params[-1])
            else:
                cases_datas_list.append(None)
            case_data_object = CaseDate()
            for data_object in zip(datas_title, cases_datas_list):
                setattr(case_data_object, data_object[0], data_object[1])
            case_datas.append(case_data_object)

        return case_datas


if __name__ == '__main__':
    excel = HandleExcel('login', 'login_test.xlsx')
    # excel = HandleExcel('login')
    res = excel.read_excel_obj()
    print(res)