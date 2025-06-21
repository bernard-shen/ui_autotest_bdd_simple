#!/usr/bin/python
# -*- coding: UTF-8 -*-
# --Author: Bernard--

import pymysql
import cx_Oracle
# from pyhive import hive
import psycopg2
import time
from pymysql import err as error
from loguru import logger

# from sqlalchemy import *
# from sqlalchemy.engine import create_engine
# from sqlalchemy.schema import *

# from pyhive import presto


class MySql:
    def __init__(self, host, sql_type, port=None, user=None, passwd=None, dbname=None, sample=None, catalog=None):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.dbname = dbname
        self.sample = sample
        self.nowTime = time.strftime('%Y-%m-%d', time.localtime())
        self.sql_type = sql_type
        self.catalog = catalog
        # 连接mysql
        if self.sql_type == 'mysql':
            self.connect = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.passwd, db=self.dbname, charset='utf8', autocommit=True)
            self.cursor = self.connect.cursor()
        # 连接oracle
        elif self.sql_type == 'oracle':
            self.connect = cx_Oracle.connect('{user}/{passwd}@{host}:{port}/{sample}'.format(user=self.user, passwd=self.passwd, host=self.host, port=self.port, sample=self.sample))
            self.cursor = self.connect.cursor()
        # 连接hive
        elif self.sql_type == 'hive':
            self.connect = hive.Connection(host=self.host, port=self.port, username=self.user, database=self.dbname)
            self.cursor = self.connect.cursor()
        # 连接pg
        elif self.sql_type == 'pg':
            self.connect = psycopg2.connect(host=self.host, port=self.port, user=self.user, password=self.passwd, database=self.dbname)
            self.cursor = self.connect.cursor()

        # elif self.sql_type == 'presto':
        #     self.engine = create_engine('presto://{}:{}/{}/{}'.format(self.host,self.port,self.catalog,self.sample))
        #     self.cursor = self.engine.connect()
        elif self.sql_type == 'presto':
            self.connect = presto.connect(host=self.host)
            self.cursor = self.connect.cursor()

        # 预留其他sql连接
        else:
            pass
        logger.add('../logs/db_connect/file_{}.log'.format(self.nowTime))

    def add_many(self, sql, data):
        try:
            if self.sql_type == 'mysql':
                self.cursor.executemany(sql, data)
            else:
                pass
        except error.DatabaseError as err:
            logger.error("db error:{}".format(err.args))

    def get_data(self, sql):
        try:
            list_data = []
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            for i in data:
                list_data.append(i[0])
            return list_data
        except error.DatabaseError as err:
            logger.error("db error: {}".format(err.args))

    #### 可以用来向hive插入数据
    def get_data_hive(self, sql):
        try:
            list_data = []
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            for i in data:
                list_data.append(i)
            return list_data
        except error.DatabaseError as err:
            logger.error("db error: {}".format(err.args))

    def execute_sql(self, sql):
        try:
            self.cursor.execute(sql)
        except error.DatabaseError as err:
            logger.error("db error:{}".format(err.args))

    def commit(self):
        try:
            if self.sql_type == "oracle":
                self.cursor.execute("COMMIT")
        except error.DatabaseError as err:
            logger.error("db error:{}".format(err.args))

    def close(self):
        self.cursor.close()
        self.connect.close()



if __name__ == '__main__':
    # new_conn = MySql(host='192.168.7.240', port=8080, user='hive', sample='hive', sql_type='presto', catalog='hive')
    # # res = new_conn.get_data('select * from table_shen1 where ID = 111;')
    # try:
    #     res = new_conn.get_data('SELECT * FROM autotest1.test_shen_connect_parameters1')
    #     print(res)
    # except ConnectionRefusedError as e:
    #     logger.error("数据连接执行报错：{}".format(e.args))

    # cursor = presto.connect('localhost').cursor()
    conn = presto.connect(host='192.168.7.240')
    cursor = conn.cursor()
    cursor.execute('select * from memory.information_schema.columns limit 10')
    print(cursor.fetchone())


