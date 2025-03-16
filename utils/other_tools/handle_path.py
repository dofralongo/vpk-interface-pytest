"""
====================
@Time:  2023/7/515:02
@Author: test_007
@File:  handle_path.py
====================
"""
import os

# 获取根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# print(BASE_DIR)

# Files路径
CONFIG_FILES = os.path.join(BASE_DIR, 'Files')
# print(CONFIG_FILES)
# 测试案例参数化数据存放文件路径
CONFIG_TEST_CASE_PARAMETER = os.path.join(CONFIG_FILES, 'parameter')
# CONFIG_FILES_PARAMETER_FILE = os.path.join(CONFIG_FILES, 'login.xlsx')
# 配置文件路径
CONFIG_CONFIG = os.path.join(BASE_DIR,'common')
CONFIG_YAML_FILE = os.path.join(CONFIG_CONFIG, 'config.yaml')

# print(CONFIG_YAML_FILE)
# 测试案例文件存放路径
CONFIG_TEST_CASES = os.path.join(BASE_DIR, 'data')
CONFIG_TEST_CASES_LOGIN = os.path.join(CONFIG_TEST_CASES,'Login')
CONFIG_TEST_CASES_LOGIN_YAML = os.path.join(CONFIG_TEST_CASES_LOGIN,'Login.yaml')
