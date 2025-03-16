"""
====================
@Time:  2023/7/1214:21
@Author: test_007
@File:  handle_parameterize.py
====================
"""
import re
import string
import random
from utils.mysql_tool.mysql_control import MysqlDB
import csv


class Parameterize:
    """
    参数化类
    """
    ont_existed_user_pattern = r'{ont_existed_user}'
    ont_existed_tel_pattern = r'{ont_existed_tel}'
    ont_existed_user_id_pattern = r'{ont_existed_user_id}'
    ont_existed_dependence_pattern = r'$cache'

    @staticmethod
    def creat_user():
        """
        随机生成用户
        """
        return ''.join(random.choices(string.ascii_letters, k=9))

    @staticmethod
    def creat_tel():
        """
        随机生成手机号
        """
        return '130' + ''.join(random.sample('012345679', 8))


    @classmethod
    def to_param(cls, data):
        data_control = str(data)
        if re.search(cls.ont_existed_user_pattern, data_control):
            data = re.sub(cls.ont_existed_user_pattern, cls.creat_user(), data_control)

        if re.search(cls.ont_existed_tel_pattern, data_control):
            data = re.sub(cls.ont_existed_tel_pattern, cls.creat_tel(), data_control)

        # if re.search(cls.ont_existed_user_id_pattern, data_control):
        #     """获取user_id"""
        #     do_mysql = MysqlDB()
        #     sql = 'SELECT user_id  FROM sys_user WHERE FULL_NAME LIKE "%boo%" and del_flag = 0 and user_id != 1692006676799799297 LIMIT 1;'
        #     # ont_existed_user_id = do_mysql.query(sql)[0]['user_id']
        #     ont_existed_user_id = do_mysql.query(sql)[0]['user_id']
        #     data = re.sub(cls.ont_existed_user_id_pattern,str(ont_existed_user_id), data_control)

        return data


if __name__ == '__main__':
    res = Parameterize()
    # # res1 = res.creat_user()
    # # print(res1, type(res1))
    # # res2 = res.creat_tel()
    # # print(res2, type(res2))
    res1 = res.to_param('{ont_existed_user}')
    print(res1)
