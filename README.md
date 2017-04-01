# wechat-tornado-sdk
   Based on the wechat-sdk,but part of the requests divide from the sdk, so tornado or other web frame work can make it async.
   Already got permissions from the Ace Kwok(doraemonext@gmail.com),my email is damonhowe2010@gmail.com.
   The doc can still be useful
   
why this?
-----------
   I got used to the style of the old one,cause Ace have no time to maintein it,I'd rather to do it

usage
-----------
   Basicaly I pack  most of the sync requests into a tornado HTTPRequest,so you should use the sdk like this:

.. code-block:: python
   
      from tornado import gen
      from tornado.httpclient import AsyncHTTPClient
      from tornado import escape
   
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
         #don't get the user_info directly ,just get the HTTPRequest
         rqt_user_info=wechat.get_user_info(user_openid, lang='zh_CN')
         #async requests
         http_client = AsyncHTTPClient()
         response    = yield http_client.fetch(rqt_user_info)
         if response.error:
             print "Error:", response.error
         else:
             print response.body
             result =escape.json_decode(response.body)
..           
    
    
    
update 2017-3-9:
------------
  full package from the wechat-sdk,but fix some update bugs
  1.upload_media now can take png,bmp,gif
