# wechat-async-sdk
   Based on the wechat-sdk,but part of the requests divide from the sdk, so tornado or other web frame work can make it async.
   Already got permissions from the Ace Kwok(doraemonext@gmail.com),my email is damonhowe2010@gmail.com.
   The doc can still be useful https://wechat-sdk.doraemonext.com/
   
why this?
-----------
   wechat-sdk in most of the situations need async,but since there is no async version of wechat,so I create this project

usage
-----------
   The fuctions have been packed into a list [method,url,params],you can use it for your async style.
   Tornado examples like this, I pack  most of the sync requests into a tornado HTTPRequest,easy:

.. code-block:: python
   
      from tornado import gen
      from tornado.httpclient import AsyncHTTPClient
      from tornado.httpclient import HTTPRequest
      from tornado import escape
      from tornado.httputil import url_concat
      import urllib
      
      @gen.coroutine
      def wechat_test(wechat_xml):
          conf = WechatConf(
            token='yourtoken', 
            appid='yourappid',   
            appsecret='yourappsecret', 
            encrypt_mode=encrypt_mode,  # normal/compatible/safe
            encoding_aes_key='yourencoding_aes_key',
            access_token=None,
            access_token_expires_at=None,            
                           )
         wechat = WechatBasic(conf)
         wechat.parse_data(wechat_xml)
         wechat.response_none()
         #don't get the user_info directly ,just get the method,url,params
         method,url,params=wechat.get_user_info(user_openid, lang='zh_CN')
         #async requests
         http_client = AsyncHTTPClient()
         rqt=pack_rqt(method,url,params)
         response    = yield http_client.fetch(rqt_user_info)
         if response.error:
             print "Error:", response.error
         else:
             print response.body
             result =escape.json_decode(response.body)
             
     def pack_rqt(method,url,params)
         if method=='get':
             url=url_concat(url,params)
             body=None
         elif method=='post':
             body =urllib.urlencode(params)
         return HTTPRequest(url=url, method=method.upper(), body=body,)
..           
    
    
    
update 2017-3-9:
------------
  full package from the wechat-sdk,but fix some update bugs
  1.upload_media now can take png,bmp,gif
