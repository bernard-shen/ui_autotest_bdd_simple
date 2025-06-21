#!/usr/bin/python
# -*- coding: UTF-8 -*-
# --Author: Bernard--

import base64
import json
from loguru import logger
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pksc1_v1_5
from Crypto.PublicKey import RSA
from common.api_request import ReqClass
from common.get_location import get_locations
from config import api_parameters as pp

# key为前端提供的固定值，若有更新可咨询前端获取； key1用户登录时的密码加密key；key2为新建数据连接时，数据库用户密码加密的key;
key1 = 'MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAJbl+tq+s4IRCLsjkiGtlr+vkUBm/rqD2KUsAg/xEIsMeEZd/pkXAiYwl9wsoLc4Xp3Df8LK/EGllo2TfVjmSqkCAwEAAQ=='
key2 = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA7Zj/2o946Fh/ivl21WJdtEO1Hh3QjDrs54jCNuW5Arh+j3AL9vyRJ5LSj7bTNWpPc6h6O1aX8jxF+dDrdXNwkjhYnd3+I9szo5fC113lhvR4zIHXGX1joTCda0NrkKxf+XqtP3wMYsRAHavSGccWcvn2TK1j/zgFyYS/divS8ouda/f8CaPl271HFc+fxL4rDqxEv5t5ttWMvT82bGTbiRJr+gwwfxRmt3RVOr4nkgcNKUwcKf7l71+sK92XD9wEME2oa/Y6WuXXRk068OHxgTyNFdKGJ0y5ZZHrORLmlgfYc1TXvFlbWKFjfZDMEjkLiD7fDRK7RkNQuI3BUvPZmwIDAQAB"
public_key1 = '-----BEGIN PUBLIC KEY-----\n' + key1 + '\n-----END PUBLIC KEY-----'
public_key2 = '-----BEGIN PUBLIC KEY-----\n' + key2 + '\n-----END PUBLIC KEY-----'
new_req = ReqClass()
header1 = {
    "Content-Type": 'multipart/form-data; boundary=----WebKitFormBoundarycJZ4TMUVW8qPgZT8'
}


# 1、对密码进行加密
def login_passwd(passwd, my_key):
    rsa_key = RSA.importKey(my_key)
    cipher = Cipher_pksc1_v1_5.new(rsa_key)
    cipher_text = base64.b64encode(cipher.encrypt(passwd.encode()))
    return cipher_text.decode()


# 获取登录后的token
def get_login_token(url, user, passwd):
    new_passwd = login_passwd(passwd=passwd, my_key=public_key1)
    data001 = {
        "username": user,
        "password": new_passwd,
        "realmFlag": "0"
    }
    res = new_req.post(url=url, params=data001, header=header1)
    response = json.loads(res.content)
    logger.info("接口返回内容为：{}".format(response))
    token = response["token"]
    return token


def get_db_user_passwd(passwd):
    rsa_key = RSA.importKey(public_key2)
    cipher = Cipher_pksc1_v1_5.new(rsa_key)
    cipher_text = base64.b64encode(cipher.encrypt(passwd.encode()))
    return cipher_text.decode()


# 将库表字段--文字参数--转化为接口自动化的接口参数；
def get_find_score(true=None, false=None, null=None):
    pass
    # 场景1：
    "db:autotes1,table:test001,column:id_no;"
    # 场景2：
    "db:autotes1;db:autotes2,table:test001,test002,column:id_no,name,phone;"
    #
    a = {    "selectedRange": [
            {
                "checked": true,
                "indeterminate": false,
                "children": [],
                "label": "autotest1",
                "type": null
            },
            {
                "checked": true,
                "indeterminate": true,
                "children": [
                    {
                        "checked": true,
                        "indeterminate": true,
                        "children": [
                            {
                                "checked": true,
                                "indeterminate": false,
                                "children": [],
                                "label": "uid",
                                "type": null
                            },
                            {
                                "checked": true,
                                "indeterminate": false,
                                "children": [],
                                "label": "name",
                                "type": null
                            },
                            {
                                "checked": true,
                                "indeterminate": false,
                                "children": [],
                                "label": "phone_number",
                                "type": null
                            }
                        ],
                        "label": "shen_static001",
                        "type": null
                    },
                    {
                        "checked": true,
                        "indeterminate": false,
                        "children": [],
                        "label": "shen_static002",
                        "type": null
                    }
                ],
                "label": "autotest_static",
                "type": null
            }
        ]}









