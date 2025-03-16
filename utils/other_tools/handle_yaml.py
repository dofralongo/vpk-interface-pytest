"""
====================
@Time:  2023/7/516:38
@Author: test_007
@File:  handle_yaml.py
====================
"""
import os.path

import yaml
from utils.other_tools.handle_path import CONFIG_TEST_CASES
from utils.other_tools.handle_path import CONFIG_TEST_CASES_LOGIN_YAML
from utils.other_tools.handle_path import CONFIG_YAML_FILE


class HandleYaml:

    # def __init__(self, dir_name, filename=None):
    def __init__(self, filename=None):
        # self.dir_name = dir_name
        if filename is not None:
            self.filename = filename
        else:
            self.filename = CONFIG_YAML_FILE
        with open(self.filename, 'r', encoding='utf-8') as file:
            self.data = yaml.load(file, Loader=yaml.FullLoader)

    def yaml_read(self, section, option):
        return self.data[section][option]

do_yaml = HandleYaml()

if __name__ == '__main__':
    do_yaml = HandleYaml()
    res = do_yaml.yaml_read('mysql_db','password')
    print(res)
