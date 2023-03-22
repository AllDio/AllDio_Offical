from django.shortcuts import render
from django.http import HttpResponse
from metasite.models import *

def already_invite(func):
    def alr_invite(request, *args, **kwargs):
        invite_code = request.session.get('invite_code')
        code_list = [i['code'] for i in InviteCode.objects.all().values()]
        if invite_code in code_list:
            if request.user.is_authenticated:
                sum_cart = len(Cart.objects.filter(user_id=request.user.id))
                msg = {
                    'username': request.user.username,
                    "invitecode": invite_code,
                    'sum_cart': sum_cart
                }
                return render(request, 'signup.html', msg)
            else:
                msg = {"invitecode": invite_code}
                return render(request, 'signup.html', msg)
        else:
            return render(request, 'signup.html')
    return alr_invite

def already_login(func):
    def alr_login(request, *args, **kwargs):
        outsec = 60*60*2*4
        print(request)
        request.session.set_expiry(outsec) # 超过秒数后失效
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            return render(request, 'signup.html')
    return alr_login

def validate_permission(func):
    def valid_per(request, *args, **kwargs):
        group_id = request.session.get('group_id')
        if group_id == 0:
            return func(request, *args, **kwargs)
        else:
            return HttpResponse("")
    return valid_per


def validate_codemail(func):
    def valid_codmail(request, *args, **kwargs):
        session = len(request.session.items()) # 判断是否有验证码请求记录
        if session > 0:
            return func(request, *args, **kwargs)
        else:
            return HttpResponse("out of date")
    return valid_codmail


