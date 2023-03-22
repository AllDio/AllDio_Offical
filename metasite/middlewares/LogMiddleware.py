
import time
import json
from django.utils.deprecation import MiddlewareMixin
from metasite.models import  AccessTimeOutLogs,OpLogs

class OpLog(MiddlewareMixin):
    __exclude_urls = ['signin/','signup/','signout/']  # 无需记录日志的url名单,如:('index/')

    def __init__(self, *args):
        super(OpLog, self).__init__(*args)
        self.start_time = None  
        self.end_time = None    
        self.data = {}
        
    def process_request(self, request):
        self.start_time = time.time()
        re_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

        # 请求IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            re_ip = x_forwarded_for.split(",")[0]  # 如果有代理，获取真实IP 
        else:
            re_ip = request.META.get('REMOTE_ADDR')

        # 请求方法
        re_method = request.method

        # 请求参数
        re_content = request.GET if re_method == 'GET' else request.POST
        if re_content:
            re_content = json.dumps(re_content)               # 筛选空参数
        else:
            re_content = None
        # 请求记录

        self.data.update(
            {
                're_time'   : re_time,                        # 请求时间
                're_url'    : request.path,                   # 请求url
                're_method' : re_method,                      # 请求方法
                're_ip'     : re_ip,                          # 请求IP
                're_content': re_content,                      # 请求参数
                're_user'   : request.user.username,          # 操作人(需修改),网站登录用户
                # 're_user' : 'AnonymousUser'                 # 匿名用户测试
            }
        )

    def process_response(self, request, response):
        for url in self.__exclude_urls:                       # 无需记录页面不记录
            if url in self.data.get('re_url'):
                return response
        # 响应内容
        rp_content = response.content.decode()                # 获取响应数据字符串(JSON字符串)
        self.data['rp_content'] = 'rp_content'

        # 响应耗时
        self.end_time = time.time()  
        access_time = self.end_time - self.start_time
        self.data['access_time'] = round(access_time * 1000)  # 耗时毫秒/ms

        # 单独记录>3s的请求(可在settings中设置"时间阈值")
        if self.data.get('access_time') > 3 * 1000:
            AccessTimeOutLogs.objects.create(**self.data)     # 超时操作日志入库
        OpLogs.objects.create(**self.data)                    # 操作日志入库

        return response