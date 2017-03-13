# -*- coding: utf-8 -*-

import json
import requests
import six
from tornado import gen
from wechat_sdk.exceptions import OfficialAPIError

#tornado version
from tornado.httpclient import AsyncHTTPClient
from tornado.httpclient import HTTPRequest
# def handle_response(response):
#     if response.error:
#         print "Error:", response.error
#     else:
#         print 'the rr',response.body


# @gen.coroutine
# def request_asyn(method,url,**kwargs):
#     print 'the request_asyn is method',method
#     print 'the request_asyn is url',url
#     print 'the request_asyn is kwargs',kwargs
#     http_client = AsyncHTTPClient()
#     rec=yield http_client.fetch('http://www.baidu.com')
#     print 'the  rec.body is',rec.body

class WechatRequest(object):
    """ WechatRequest 请求类

    对微信服务器的请求响应处理进行封装
    """

    def __init__(self, conf=None):
        """
        :param conf: WechatConf 配置类实例
        """
        self.__conf = conf

    # @gen.coroutine
    def request(self, method, url, access_token=None, **kwargs):
        """
        向微信服务器发送请求
        :param method: 请求方法
        :param url: 请求地址
        :param access_token: access token 值, 如果初始化时传入 conf 会自动获取, 如果没有传入则请提供此值
        :param kwargs: 附加数据
        :return: 微信服务器响应的 JSON 数据
        """
        access_token = self.__conf.access_token if self.__conf is not None else access_token
        if "params" not in kwargs:
            kwargs["params"] = {
                "access_token": access_token
            }
        else:
            kwargs["params"]["access_token"] = access_token

        if isinstance(kwargs.get("data", ""), dict):
            body = json.dumps(kwargs["data"], ensure_ascii=False)
            if isinstance(body, six.text_type):
                body = body.encode('utf8')
            kwargs["data"] = body
        r = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        r.raise_for_status()
        try:
            response_json = r.json()
        except ValueError:  # 非 JSON 数据
            return r

        headimgurl = response_json.get('headimgurl')
        if headimgurl:
            response_json['headimgurl'] = headimgurl.replace('\\', '')
        self._check_official_error(response_json)
        return response_json
        ###########################async##############################
        # method=method.upper()
        # # print 'the request_asyn is method',method
        # # print 'the request_asyn is url',url
        # # print 'the request_asyn is kwargs',kwargs
        # # # method='GET'
        # # # url='http://www.baidu.com'
        # response=yield AsyncHTTPClient().fetch(HTTPRequest( 
        #             url=url, 
        #             #follow_redirects=False
        #             method=method, 
        #             body=kwargs['params']
        #             ))
        #             # body=download_file.body, 
        #             # headers=headers_dict, 
        # print 'the response body is',response.body
        # if response.error:
        #     print "Error:", response.error
        # else:
        #     print 'the rr',response.body
        ############################sync################################

    def get(self, url, access_token=None, **kwargs):
        """
        使用 GET 方法向微信服务器发出请求
        :param url: 请求地址
        :param access_token: access token 值, 如果初始化时传入 conf 会自动获取, 如果没有传入则请提供此值
        :param kwargs: 附加数据
        :return: 微信服务器响应的 JSON 数据
        """
        return self.request(
            method="get",
            url=url,
            access_token=access_token,
            **kwargs
        )

    def post(self, url, access_token=None, **kwargs):
        """
        使用 POST 方法向微信服务器发出请求
        :param url: 请求地址
        :param access_token: access token 值, 如果初始化时传入 conf 会自动获取, 如果没有传入则请提供此值
        :param kwargs: 附加数据
        :return: 微信服务器响应的 JSON 数据
        """
        return self.request(
            method="post",
            url=url,
            access_token=access_token,
            **kwargs
        )

    def _check_official_error(self, json_data):
        """
        检测微信公众平台返回值中是否包含错误的返回码
        :raises OfficialAPIError: 如果返回码提示有错误，抛出异常；否则返回 True
        """
        if 'errcode' in json_data and json_data['errcode'] != 0:
            raise OfficialAPIError(errcode=json_data.get('errcode'), errmsg=json_data.get('errmsg', ''))
