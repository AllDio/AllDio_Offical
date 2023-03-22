from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin    # 1.10.x
from alldio.settings import IPDIA_ROOT
import os
class TestMiddleware(MiddlewareMixin):
    def process_view(self,request,view_func,*view_args,**view_kwargs):
        def get_ip_location():
            '''
            -获得ip位置信息
            :param request:
            :param datapath:
            :return: country(string)
            '''
            import geoip2.database
            datapath = os.path.join(IPDIA_ROOT,'GeoLite2-City.mmdb')
            reader = geoip2.database.Reader(datapath)
            try:
                response = reader.city(ip)
                country = response.country.iso_code
                cityname = response.city.name
                data = {'country': country, 'city': cityname}
                return data['country']
            except:
                local_ips = ['127.0.0.1']
                if ip in local_ips:
                    return 'LOCAL'
                else:
                    return 'Unkown IP'

        if 'HTTP_X_FORWARDED_FOR' in  request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']

        id_country = get_ip_location()
        print(f'[{id_country}] -> {ip} ')

        countries = ['CN','TW','HK','LOCAL']
        if id_country not in countries:
            return HttpResponse('<h1 style="opacity:0.2">no permission</h1>')

