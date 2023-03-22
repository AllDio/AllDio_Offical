import json
import random

from django.shortcuts import render, HttpResponse
from ratelimit.decorators import ratelimit, timelimit
from metasite.decorator import already_login, validate_codemail
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from metasite.models import *

giftcards = [
    {
        'title': 'CardSets',
        'icon': 'https://cdn-icons-png.flaticon.com/128/1692/1692226.png',
        'price': '25',
    },
    {
        'title': 'Instruments',
        'icon': 'https://cdn-icons-png.flaticon.com/128/1692/1692226.png',
        'price': '5',
    },
    {
        'title': 'Structures',
        'icon': 'https://cdn-icons-png.flaticon.com/128/1692/1692226.png',
        'price': '5',
    },
    {
        'title': 'Chords',
        'icon': 'https://cdn-icons-png.flaticon.com/128/1692/1692226.png',
        'price': '5',
    },
]
buycoins = [
    {
        'price': '5',
        'icon': 'https://cdn-icons-png.flaticon.com/128/1027/1027917.png',
        'quantity': '15',
    },
    {
        'price': '15',
        'icon': 'https://cdn-icons-png.flaticon.com/128/1027/1027950.png',
        'quantity': '50',
    },
    {
        'price': '35',
        'icon': 'https://cdn-icons-png.flaticon.com/128/1027/1027961.png',
        'quantity': '150',
    }
]

paypal_client_id = 'Ada9UP46XCR6D1H8nYMc2Jz4c81xsGddcKnWGTUY-QpETBDF2_kS_vETgidW4s58qF3-ECwbtnumxKpQ'
paypal_client_secret = 'ELUkvSR-t9ztslZUzF0A5WidwMshUtQN4kC_EniDvuumr4mfjlOqfMTpjicupf0Md2lvqJOqY56LIdee'


def time_controller(days, hour=0, minute=0, second=0, day=datetime.now()):
    '''
    # 获得某天的x天、y小时、t分钟、z秒后的日期, day为空默认为当前时间开始
    # 所有参数默认都为0，只需要调你需要的时间即可
    # arg = 1: 获得hour小时,minute分钟,second秒后的具体时间
    # arg = -1: 获得hour小时,minute分钟,second秒前的具体时间
    '''
    global value
    import time
    import datetime
    arg = 1
    # day = datetime.datetime.now()
    now = day
    if type(day) == str:
        try:
            now = datetime.datetime.strptime(day, '%Y-%m-%d %H:%M:%S')
        except:
            now = datetime.datetime.strptime(day, '%Y.%m.%d %H:%M:%S')
    if arg == 1:
        value = now + datetime.timedelta(days=days, hours=hour, minutes=minute, seconds=second)
    elif arg == -1:
        value = now - datetime.timedelta(days=days, hours=hour, minutes=minute, seconds=second)
    return value


def reload_page(request):
    if request_POST(request):
        add_nowtab_nowsubtab(request)
        return HttpResponse('')
    else:
        return HttpResponse('')


@already_login
def wallet_connect(request):
    if request_POST(request):
        wallet_address = POST_get(request, 'wallet_address')
        wallet_balance = POST_get(request, 'wallet_balance')
        wallet_network = POST_get(request, 'wallet_network')
        try:
            add_session_value(request, 'wallet_address', wallet_address)
            add_session_value(request, 'wallet_balance', wallet_balance)
            add_session_value(request, 'wallet_network', wallet_network)
            add_nowtab_nowsubtab(request)
            return HttpResponse(True)
        except:
            return HttpResponse(False)


@already_login
def web3_dapps(request):
    # if request_POST(request):
    import os
    from alldio.settings import STATIC_METASITE
    # account = POST_get(request, 'account')
    # user_wallet = request.POST.get('user_wallet')

    # 调取智能合约并写入更新信息
    from web3 import Web3
    Dapp_address = Web3.toChecksumAddress("0x7f331fcb6a314400686abbc40c51db200535dc79")
    Dapp = Web3(Web3)

    def get_abi():
        abi_path = os.path.join(STATIC_METASITE, 'abi.json')
        f = open(abi_path, 'r')
        abi = ''
        for i in f.readlines():
            abi += i
        abi = abi
        return abi

    abi = get_abi()

    contract = Dapp.eth.contract(address=Dapp_address, abi=abi)

    from eth_account import Account
    import json
    key = '77599fb2f4f22ec02ac80798a27843c05ec283372e919e570182ef955976027a'
    account = Account.from_key(key)
    # balance = contract.functions.balanceOf(account).call()
    # print(balance)
    return HttpResponse('')


@already_login
def buy_coins(request):
    if request_POST(request):
        try:
            pay_result = get_session_value(request, 'pay_result')
        except:
            pay_result = False
        if pay_result:
            coin_select = POST_get(request, 'coin_select')
            userid = request.user.id
            quantity = buycoins[int(coin_select) - 1]['quantity']
            memberwallet = MemberWallet.objects.get(user_id=userid)
            memberwallet.coin = int(get_obj_value('coin', MemberWallet.objects.filter(user_id=userid), 'id')[0]) + int(
                quantity)
            memberwallet.save()

            add_nowtab_nowsubtab(request)
            delete_reqeust(request, 'pay_result')
            return HttpResponse('coinpay success')
        else:
            delete_reqeust(request, 'pay_result')
            return HttpResponse('coinpay failed')

    else:
        return HttpResponse('')


def dapps_return(request):
    try:
        nft_title = get_session_value(request, 'nft_title')
        nft_description = get_session_value(request, 'nft_description')
        nft_image = get_session_value(request, 'nft_image')

        result = {
            "name": nft_title,
            "description": nft_description,
            "image": nft_image,
        }

        delete_reqeust(request, nft_title)
        delete_reqeust(request, nft_description)
        delete_reqeust(request, nft_image)

        return HttpResponse(json.dumps(result))
    except:
        return HttpResponse('')


@already_login
def song_info(request):
    private_key = request.POST.get('private_key')
    if private_key == '77599fb2f4f22ec02ac80798a27843c05ec283372e919e570182ef955976027a':
        result = {
            'name': 'Justin',
            # 'song' : 'http://www.alldio.xyz/hello_music.mp3',
            'description': 'a pop song',
            'image': 'https://goerli.ethersacn.io/images/favicon3.ico',
            # 可添加其他信息？
        }
        return result
    else:
        return 'error'


@already_login
def paypal_refund(requset):
    # 退款
    from paypalrestsdk import Sale

    sale = Sale.find("流水号")

    # Make Refund API call
    # Set amount only if the refund is partial
    refund = sale.refund({
        "amount": {
            "total": "5.00",
            "currency": "USD"}})

    # Check refund status
    if refund.success():
        print("Refund[%s] Success" % (refund.id))
    else:
        print("Unable to Refund")
        print(refund.error)


@already_login
def paypal_execute(request):
    if request.method == 'GET':
        import paypalrestsdk
        add_nowtab_nowsubtab(request)
        try:
            paymentid = get_session_value(request, 'paymentid')  # 订单id
            payerid = get_session_value(request, 'payerId')  # 支付者id

            if paymentid != None:
                payment = paypalrestsdk.Payment.find(paymentid)

                if payment.execute({"payer_id": payerid}):
                    print("Payment execute successfully")
                    return HttpResponse("success")
                else:
                    print(payment.error)  # Error Hash
                    return HttpResponse("falied")
            else:
                return HttpResponse('falied')
        except:
            return HttpResponse('falied')


@already_login
def paypal_payment(request):
    if request_POST(request):
        import paypalrestsdk

        add_nowtab_nowsubtab(request)

        item = POST_get(request, 'item')
        value = POST_get(request, 'value')

        try:
            if item == 'subscription':
                title = value
                payprice = str(get_obj_value('price', Subscription.objects.filter(title=title), 'id')[0])
            elif item == 'buycoin':
                title = item
                payprice = value

            paypalrestsdk.configure({
                "mode": "sandbox",
                "client_id": paypal_client_id,
                "client_secret": paypal_client_secret,
            })

            payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {"payment_method": "paypal"},
                "redirect_urls": {
                    "return_url": "http://34.125.254.98/paypal_backurl/",  # 支付成功跳转页面
                    "cancel_url": "http://34.125.254.98/paypal/cancel/"},  # 取消支付页面
                "transactions": [{
                    "amount": {
                        "total": payprice,
                        "currency": "USD"},
                    "description": f"Payment about {title}"}]})
            if payment.create():
                print("Payment created successfully")
                for link in payment.links:
                    if link.rel == "approval_url":
                        approval_url = str(link.href)
                        print("Redirect for approval: %s" % (approval_url))
                        return HttpResponse(approval_url)
            else:
                print(payment.error)
                return HttpResponse("Pay failed")
        except:
            return HttpResponse('Pay failed')
    else:
        HttpResponse('')


def get_nowtime():
    import time
    nowtime = time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time()))
    return nowtime


def date_fix(date):
    fix_date = date.split('.')[0].replace('-', '.')
    return fix_date


def dict_object_create(query_keys, handle_keys, updt_dict, objects):
    try:
        new_dict = {}
        new_dict.update(updt_dict)
        for key in query_keys:
            if key not in handle_keys:
                new_dict.update({key: '-'})
        objects.create(**new_dict)
        return True
    except:
        import traceback
        print(traceback.format_exc())
        return False


def get_time_delta(date1, date2):
    date1 = datetime.strptime(date1, "%Y.%m.%d %H:%M:%S")
    date2 = datetime.strptime(date2, "%Y.%m.%d %H:%M:%S")
    resttime = str(date2 - date1)
    if ' day' in resttime:
        resttime = int(resttime.split(' day')[0])
    else:
        resttime = 0
    return resttime


def request_POST(request):
    if request.method == 'POST':
        return True
    else:
        return False


def POST_get(request, kywrd):
    result = request.POST.get(kywrd)
    return result


def get_session_value(request, tag):
    try:
        value = request.session[tag]
    except:
        value = None
    return value


def delete_reqeust(request, tag):
    try:
        del request.session[tag]
        return True
    except:
        return False


def add_session_value(request, tag, value):
    if tag in list(request.session.keys()):
        request.session[tag] = value
    else:
        request.session.update({tag: value})


def get_obj_value(tag, obj, order):
    value = [i[tag] for i in obj.order_by(order).values().order_by(order)]
    return value


def digi_add_zero(digi):
    if digi <= 9:
        str_digi = '00' + str(digi)
    elif digi <= 99:
        str_digi = '0' + str(digi)
    elif digi <= 999:
        str_digi = str(digi)
    else:
        str_digi = str(digi)
    return str_digi


def add_nowtab_nowsubtab(request):
    nowdark = POST_get(request, 'nowdark')
    nowtab = POST_get(request, 'nowtab')
    nowsubtab = POST_get(request, 'nowsubtab')
    add_session_value(request, 'nowdark', nowdark)
    add_session_value(request, 'nowtab', nowtab)
    add_session_value(request, 'nowsubtab', nowsubtab)


# [ Core Runtime ] ---------------------------
@already_login
def become_contributor(request):
    if request_POST(request):
        def get_info():
            userid = request.user.id
            about = POST_get(request, 'about')
            role = POST_get(request, 'role')
            return userid, about, role

        (userid, about, role) = get_info()  # ♻️

        def send_admincheck_contributor(about, role, userid):
            pass

        send_admincheck_contributor(about, role, userid)  # ♻️

        def user_apply_status_change():
            userinfo_obj = Userinfo.objects.get(user_id_id=userid)
            userinfo_obj.apply_status = 1
            userinfo_obj.save()
            return True

        user_apply_status_change()  # ♻️

        return HttpResponse('')
    else:
        return HttpResponse('')


@already_login
def get_generatesong(request):
    if request_POST(request):
        def get_info():
            userid = request.user.id
            prompt = POST_get(request, 'prompt')
            return userid, prompt

        (userid, prompt) = get_info()  # ♻️

        def reduce_rights():
            user_right = get_obj_value('right', Member.objects.filter(user_id=userid), 'id')[0]
            memebr = Member.objects.get(user_id=userid)
            memebr.right = int(user_right) - 1
            memebr.save()

        reduce_rights()  # ♻️

        def get_music_token():
            from metasite.dailytools.tools.random_code import get_random_code
            music_token = get_random_code()
            already_token = get_obj_value('mstoken', Music.objects, 'id')
            while music_token in already_token:
                already_token = get_obj_value('mstoken', Music.objects, 'id')
                music_token = get_random_code()
            return music_token

        music_token = get_music_token()  # ♻️
        add_session_value(request, 'music_token', music_token)

        def connect_universe(prompt):
            from metasite.dailytools.tools.string_number import get_str_number
            str_idx = get_str_number(intnumber=random.choice(range(1, 10)), intmax=10)

            song_url = f'https://storage.googleapis.com/acoustic-gizmo-377310.appspot.com/public_music/%20song_{str_idx}.mp3'
            return song_url

        song_url = connect_universe(prompt)  # ♻️

        add_session_value(request, 'song_url', song_url)
        add_session_value(request, 'prompt', prompt)

        def get_return_result():
            result = {
                'song_url': song_url,
                'music_title': 'new song',
                'music_token': music_token,
            }
            result = json.dumps(result)
            return result

        result = get_return_result()  # ♻️

        return HttpResponse(result, content_type="application/json")
    else:
        return HttpResponse('')


@already_login
def stored_song(request):
    if request_POST(request):
        def get_info():
            userid = request.user.id
            mstoken = POST_get(request, 'mstoken')
            add_nowtab_nowsubtab(request)
            return userid, mstoken

        userid, mstoken = get_info()  # ♻️

        def get_music_token():
            from metasite.dailytools.tools.random_code import get_random_code
            music_token = get_random_code()
            already_token = get_obj_value('mstoken', Music.objects, 'id')
            while music_token in already_token:
                already_token = get_obj_value('mstoken', Music.objects, 'id')
                music_token = get_random_code()
            return music_token

        try:
            session_mstoken = get_session_value(request, '')
            if mstoken == session_mstoken:
                music_token = mstoken
            else:
                music_token = get_music_token()
                print('not same token')
        except:
            music_token = get_music_token()  # ♻
            print('not same token')

        def auto_newsong_title():
            musictitle_abbreviations = [i for i in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']
            musicsubtitles = []

            for i in range(1, 100):
                str_digi = digi_add_zero(i)
                musicsubtitles.append(str_digi)
            library_titles = get_obj_value('title', Music.objects, 'id')
            first_letters = [i.split('-')[0] for i in library_titles]
            second_digis = [i.split('-')[1] for i in library_titles]
            if len(second_digis) > 0:
                if second_digis[-1] < '999':
                    abv = first_letters[-1]
                    str_digi = digi_add_zero(int(second_digis[-1]) + 1)
                else:
                    abv = musictitle_abbreviations[musictitle_abbreviations.index(first_letters[-1]) + 1]
                    str_digi = '001'
                music_title = f'{abv}-{str_digi}'
            else:
                str_digi = '001'
                music_title = f'A-{str_digi}'

            return music_title

        music_title = auto_newsong_title()  # ♻️

        nft_images = [
            'https://i.seadn.io/gcs/files/d22dad6ad96518d5eda31fb0ffd0a31d.png?auto=format&w=1000',
            'https://i.seadn.io/gcs/files/77c413cc1cc31c193a7f46794b198810.png?auto=format&w=1000',
            'https://i.seadn.io/gcs/files/0ac8a32a07c0a39264dddb66cd092d4f.png?auto=format&w=1000',
        ]

        song_url = get_session_value(request, 'song_url')
        prompt = get_session_value(request, 'prompt')

        add_session_value(request, 'nft_title', music_title)
        add_session_value(request, 'nft_description', prompt)
        add_session_value(request, 'nft_image', nft_images[random.choice(range(len(nft_images)))])

        def add_new_song():
            song_id = len(Music.objects.values()) + 1
            add_keys = ['mstoken', 'founder', 'prompt', 'title', 'id', 'status', 'owner', 'url', 'createdate']
            if len(Music.objects.values()) > 0:
                query_keys = list(dict(Music.objects.values()[0]).keys())
            else:
                query_keys = ['songnm', 'value', 'price', 'tag', 'genre', 'emo', 'inst', 'tempo', 'length', 'beat',
                              'scale', 'cover', 'wavform', 'label', 'minter', 'share', 'lyrics', 'melody', 'arrange',
                              'artist', 'mixing', 'record', 'unit', 'cue', 'intro', 'saleif', 'more1', 'more2', 'more3',
                              'more4', 'more5', 'more6', 'more7', 'more8', 'more9', 'more10']
            newsong_dict = {}
            newsong_dict.update({
                'mstoken': music_token,
                'founder': userid,
                'prompt': prompt,
                'title': music_title,
                'owner': userid,
                'status': 'offline',
                'url': song_url,
                'id': song_id,
            })
            for key in query_keys:
                if key not in add_keys:
                    newsong_dict.update({key: '-'})

            Music.objects.create(**newsong_dict)
            return True

        add_new_song()  # ♻️

    return HttpResponse('')


@already_login
def edit_usrprofile(request):
    if request_POST(request):
        def get_info():
            userid = request.user.id
            nickname = POST_get(request, 'nickname')
            icon_idx = POST_get(request, 'icon_idx')
            return userid, nickname, icon_idx

        (userid, nickname, icon_idx) = get_info()  # ♻️

        def save_usrprofile_eidt():
            userinfo_obj = Userinfo.objects.filter(user_id_id=userid)
            usrinfo = Userinfo.objects.get(user_id_id=userid)
            userinfodate = str(get_obj_value('userinfodate', userinfo_obj, 'id')[0]).split('.')[0].replace('-', '.')

            def get_usr_edit_rights():
                limit_edit_duration_day = 30
                try:
                    rights = int(get_obj_value('edit_rights', userinfo_obj, 'id')[0])
                except:
                    rights = 0

                if rights > 0:
                    has_EditRights = True
                else:
                    if get_time_delta(userinfodate, get_nowtime()) >= limit_edit_duration_day:
                        has_EditRights = True
                        rights = 10
                    else:
                        has_EditRights = False
                return has_EditRights, rights

            (has_EditRights, rights) = get_usr_edit_rights()

            if has_EditRights:
                if len(icon_idx) > 0:
                    usrinfo.icon = icon_idx
                usrinfo.edit_rights = int(rights) - 1
                usrinfo.nick = nickname
                usrinfo.save()
                return True
            else:
                return False

        result = save_usrprofile_eidt()  # ♻️

        add_nowtab_nowsubtab(request)  # ♻️

        return HttpResponse(result)
    else:
        return HttpResponse('')


@already_login
def get_luckycard(request):
    if request_POST(request):
        userid = request.user.id
        cardbox_idx = POST_get(request, 'cardbox_idx')

        add_nowtab_nowsubtab(request)
        try:
            cardbox_title = giftcards[int(cardbox_idx) - 1]['title']
            coin_pay = giftcards[int(cardbox_idx) - 1]['price']
        except:
            cardbox_title = 'None'
            coin_pay = 0

        def get_cards(cardbox_title):
            cards_infos = []
            if cardbox_title == 'CardSets':
                card_sets = ['instrument', 'structure', 'chord', 'effect']
                try:
                    for i in range(len(card_sets)):
                        cards_obj = Cards.objects.filter(user_id=0, type=card_sets[i])
                        random_idx = random.choice(range(len(get_obj_value('title', cards_obj, 'id'))))
                        cards_info = {
                            'card_title': get_obj_value('title', cards_obj, 'id')[random_idx],
                            'card_icon': get_obj_value('icon', cards_obj, 'id')[random_idx],
                            'card_type': get_obj_value('type', cards_obj, 'id')[random_idx],
                            'card_level': get_obj_value('level', cards_obj, 'id')[random_idx],
                            'card_intro': get_obj_value('intro', cards_obj, 'id')[random_idx],
                            'card_token': get_obj_value('cdtoken', cards_obj, 'id')[random_idx],
                        }
                        cards_infos.append(cards_info)
                    cdtokens = [i['card_token'] for i in cards_infos]
                except:
                    cards_infos = None
                    cdtokens = None
            else:
                try:
                    if cardbox_title == 'Instruments':
                        cards_obj = Cards.objects.filter(user_id='0', type='instrument')
                    elif cardbox_title == 'Structures':
                        cards_obj = Cards.objects.filter(user_id='0', type='structure')
                    elif cardbox_title == 'Chords':
                        cards_obj = Cards.objects.filter(user_id='0', type='chord')
                    elif cardbox_title == 'Effects':
                        cards_obj = Cards.objects.filter(user_id='0', type='effect')
                    else:
                        cards_obj = ''
                        breakpoint()
                    random_idx = random.choice(range(len(get_obj_value('title', cards_obj, 'id'))))
                    cards_info = {
                        'card_title': get_obj_value('title', cards_obj, 'id')[random_idx],
                        'card_icon': get_obj_value('icon', cards_obj, 'id')[random_idx],
                        'card_type': get_obj_value('type', cards_obj, 'id')[random_idx],
                        'card_level': get_obj_value('level', cards_obj, 'id')[random_idx],
                        'card_intro': get_obj_value('intro', cards_obj, 'id')[random_idx],
                        'card_token': get_obj_value('cdtoken', cards_obj, 'id')[random_idx],
                    }
                    cards_infos.append(cards_info)
                    cdtokens = [i['card_token'] for i in cards_infos]
                except:
                    cards_infos = None
                    cdtokens = None

            if cards_infos != None:
                def coin_cost(coin_pay):
                    member_wallet = MemberWallet.objects.get(user_id=userid)
                    user_rest_coin = get_obj_value('coin', MemberWallet.objects.filter(user_id=userid), 'id')[0]
                    member_wallet.coin = int(user_rest_coin) - int(coin_pay)
                    member_wallet.save()

                coin_cost(coin_pay)  # ♻️
            return cards_infos, cdtokens

        (cards_infos, cdtokens) = get_cards(cardbox_title)  # ♻️

        if cdtokens:
            def belong_user(cdtokens):
                for ti in range(len(cdtokens)):
                    card = Cards.objects.get(cdtoken=cdtokens[ti])
                    card.user_id = userid
                    card.save()
                return cards_infos

            belong_user(cdtokens)  # ♻️
            cards_infos = json.dumps(cards_infos)
        else:
            cards_infos = [{}]
        return HttpResponse(cards_infos, content_type="application/json")
    else:
        return HttpResponse('')


@already_login
def pay_royalty(request):
    if request_POST(request):
        def get_info():
            userid = request.user.id
            usersong_objs = Music.objects.filter(owner=userid)
            user_songids = get_obj_value('id', usersong_objs, 'id')
            royalty_objs = Royalty.objects.filter(song_id__in=user_songids)
            royalty_songprices = get_obj_value('price', royalty_objs, 'song_id')
            royalty_incomes = round(sum(float(i) for i in royalty_songprices), 2)
            return royalty_incomes

        royalty_incomes = get_info()

        def user_royalty_payment():
            pay_result = True
            return pay_result

        pay_result = user_royalty_payment()

        if pay_result:
            result = True
        else:
            result = False

        add_nowtab_nowsubtab(request)

        return HttpResponse(result)
    else:
        return HttpResponse('')


@already_login
def admincheck_contributor(request):
    pass


def songmint_status(request):
    if request_POST(request):
        def get_info():
            token = POST_get(request, 'token')
            result = POST_get(request, 'result')
            add_nowtab_nowsubtab(request)
            return token, result

        token, result = get_info()  # ♻️

        def send_dapps_api(result):
            if result == 'true':
                result = True
            else:
                result = False
            return result

        result = send_dapps_api(result)  # ♻️

        if result:
            song = Music.objects.get(mstoken=token)
            song.status = 'online'
            song.save()
        return HttpResponse('')
    else:
        return HttpResponse('')


@already_login
def mint_song(request):
    if request_POST(request):
        def get_info():
            userid = request.user.id
            username = request.user.username
            token = POST_get(request, 'token')
            return userid, username, token

        (userid, username, token) = get_info()  # ♻️

        def get_mintsong_info():
            song_objs = Music.objects.filter(mstoken=token)
            user_objs = Userinfo.objects.filter(user_id_id=userid)
            mintsong_infos = {
                'song_url': get_obj_value('url', song_objs, 'id')[0],
                'song_token': token,
                'song_ownertoken': get_obj_value('ustoken', user_objs, 'id')[0],
                'song_username': username,
            }
            return mintsong_infos

        mintsong_infos = get_mintsong_info()  # ♻️

        def get_result():
            from metasite.dailytools.tools.contract_abi import get_contract_abi
            contract_abi = get_contract_abi(abi_json='abi.json')
            contract_privatekey = '77599fb2f4f22ec02ac80798a27843c05ec283372e919e570182ef955976027a'
            contract_address = '0x7f331fcb6a314400686abbc40c51db200535dc79'
            nft_return = 'http://www.alldio.xyz/dapps_return'
            return (contract_abi, contract_privatekey, contract_address, nft_return)

        (contract_abi, contract_privatekey, contract_address, nft_return) = get_result()

        result = {
            'contract_abi': contract_abi,
            'contract_address': contract_address,
            'contract_privatekey': contract_privatekey,
            'nft_return': nft_return,
            'mintsong_infos': mintsong_infos,
        }
        return HttpResponse(json.dumps(result))
    else:
        return HttpResponse('')


@already_login
def sell_card(request):
    if request_POST(request):
        def get_info():
            userid = request.user.id
            token = POST_get(request, 'token')
            saleif = POST_get(request, 'saleif')
            return token, userid, saleif

        (token, user_id, saleif) = get_info()  # ♻️

        def change_card_sell_status():
            try:
                card = Cards.objects.get(cdtoken=token)
                if saleif == 'sell':
                    card.saleif = 'store'
                else:
                    card.saleif = 'sell'
                card.save()
                return True
            except:
                return False

        change_result = change_card_sell_status()

        if change_result:
            result = True
        else:
            result = False

        add_nowtab_nowsubtab(request)  # ♻️

        return HttpResponse(result)
    else:
        return HttpResponse('')


@already_login
def buysongs(request):
    return HttpResponse('')


@already_login
def buycards(request):
    return HttpResponse('')


@already_login
def userprofile_edit(request):
    return HttpResponse('')


@already_login
def change_subscription(request):
    if request_POST(request):
        def get_info():
            title = POST_get(request, 'plan')
            userid = request.user.id
            return userid, title

        (userid, title) = get_info()

        def pay_subscription():
            pay_result = get_session_value(request, 'pay_result')
            return pay_result

        pay_result = pay_subscription()

        if pay_result:
            def change_user_subscription():
                member = Member.objects.get(user_id=userid)
                member_obj = Member.objects.filter(user_id=userid)
                subscription_obj = Subscription.objects.filter(title=title)
                subscription_type = get_obj_value('type', subscription_obj, 'id')[0]
                member.type = subscription_type
                right = get_obj_value('limit1', subscription_obj, 'id')[0]
                try:
                    member.right = int(member.right) + int(right)
                except:
                    member.right = int(right)

                member.buydate = get_nowtime()
                day = get_obj_value('outdate', member_obj, 'id')[0]
                if len(day) == 0:
                    day = get_nowtime()
                print(day)

                member.outdate = time_controller(days=30, day=day)
                member.save()

            change_user_subscription()
            result = True
        else:
            result = False

        add_nowtab_nowsubtab(request)
        delete_reqeust(request, 'pay_result')

        return HttpResponse(result)
    else:
        return HttpResponse('')


@already_login
def cancel_subscription(request):
    if request_POST(request):
        def get_info():
            userid = request.user.id
            return userid

        (userid) = get_info()

        def cancel_user_subscription():
            cancel_result = True
            return cancel_result

        cancel_result = cancel_user_subscription()

        if cancel_result:
            def change_user_subscription():
                member = Member.objects.get(user_id=userid)
                member.type = 0
                member.save()

            change_user_subscription()
            result = True
        else:
            result = False

        add_nowtab_nowsubtab(request)

        return HttpResponse(result)
    else:
        return HttpResponse('')


@already_login
def send_suggestion(request):
    if request_POST(request):
        userid = request.user.id
        suggestion = POST_get(request, 'suggestion')
        result = dict_object_create(
            query_keys=list(dict(Messagebox.objects.values()[0]).keys()),
            handle_keys=['user_id', 'id', 'type', 'content', 'touserid', 'status', 'messageboxdate'],
            updt_dict={
                'user_id': userid,
                'id': len(Messagebox.objects.values()) + 1,
                'type': 'suggestion',
                'content': suggestion,
                'touserid': 0,
                'status': 0,
            },
            objects=Messagebox.objects,
        )
        return HttpResponse(result)
    else:
        return HttpResponse('')


@already_login
def save_payinfo(request):
    if request_POST(request):
        def get_info():
            userid = request.user.id
            card_number = POST_get(request, 'card_number')
            exp_month = POST_get(request, 'exp_month')
            exp_year = POST_get(request, 'exp_year')
            exp_code = POST_get(request, 'exp_code')
            add_nowtab_nowsubtab(request)
            return userid, card_number, exp_month, exp_year, exp_code

        (userid, card_number, exp_month, exp_year, exp_code) = get_info()

        def save_payinfo():
            payinfo = Payinfo.objects.get(user_id=userid)
            payinfo.expmonth = exp_month
            payinfo.expyear = exp_year
            payinfo.secucode = exp_code
            payinfo.cardnum = card_number
            payinfo.save()

        save_payinfo()

        passPayinfo = True

        if passPayinfo:
            result = True
        else:
            result = False

        return HttpResponse(result)
    else:
        return HttpResponse('')


@already_login
def upload_contribution(request):
    return HttpResponse('')


@already_login
def read_message(request):
    return HttpResponse('')


@already_login
def search_pannel(request):
    return HttpResponse('')


# ------------------------------------------------
@already_login
def paypal_backurl(request):
    back_url = request.get_full_path()
    if 'paymentId=' and 'token=' and 'PayerID=' in back_url:
        payerid = back_url.split('PayerID=')[1]
        paymentid = back_url.split('paymentId=')[1].split('&token=')[0]
        # token = back_url.split('&token=')[1].split('&PayerID=')[0]

        if paymentid != None:
            import paypalrestsdk
            payment = paypalrestsdk.Payment.find(paymentid)
            if payment.execute({"payer_id": payerid}):
                add_session_value(request, 'pay_result', True)
                print('payment excute success')
                return render(request, 'payback.html')
            else:
                add_session_value(request, 'pay_result', False)
                print(payment.error)
                return HttpResponse("falied")
        else:
            add_session_value(request, 'pay_result', False)
            return render(request, 'payback.html')

    else:
        add_session_value(request, 'pay_result', False)
        return HttpResponse('')


# 登录注册 =====================
@timelimit(key='ip', rate='10/10m', block=True)
def invitecode(request):
    from metasite.models import InviteCode
    if request.method == 'POST':
        code = request.POST.get('invite_code')
        invite_checks = [i['code'] for i in InviteCode.objects.all().values()]
        if code in invite_checks:
            return HttpResponse('success')
        else:
            return HttpResponse('⚠️ The invitation code is incorrectly entered')
    else:
        return HttpResponse('')


@timelimit(key='ip', rate='10/10m', block=True)
def create_user(request):
    if request.method == "GET":
        print('1' * 100)
        # username = request.GET.get('username')  # 用户名查重
        password = request.GET.get('password')
        # confirm = request.GET.get("confirm_password")  # 密码确认
        # phone = request.GET.get('phone')  # 手机验证
        email = request.GET.get('email')  # 邮箱验证
        username = email
        emailcode = request.GET.get('emailcode')  # 邮箱验证
        invitecode = request.GET.get('invitecode')
        # print(username,password,confirm,phone,email,emailcode,'.......')
        # phone_checked, msg = phone_check.phoneVertificate().verificate(phone)
        if len(email) > 0:
            if 'email_code' in request.session.keys():
                if emailcode == request.session['email_code']:
                    email_checked = True
                else:
                    email_checked = False
            else:
                email_checked = False
        else:
            email_checked = False

        if email_checked:
            # 用户体系
            User.objects.create_user(username=username, email=email, password=password, invite=invitecode)
            userid = [i['id'] for i in User.objects.filter(username=username).values()][0]
            print(userid, '..........')
            # 获取ustoken
            from metasite.dailytools.tools.random_code import get_random_code

            ustoken = get_random_code()
            all_ustoken = Userinfo.objects.filter(ustoken=ustoken).values()

            exit_num = 0
            while len(all_ustoken) > 0:
                exit_num += 1
                ustoken = get_random_code()
                if exit_num > 100000:
                    ustoken = 'None'
                    break
            print(ustoken, '........')

            if ustoken != 'None':
                # 会员体系
                member = Member()
                member.id = len(Member.objects.values()) + 1
                member.user_id = userid
                member.right = 10
                member.type = 0
                member.note = username
                member.level = 0
                member.honor = 'pp'
                member.ustoken = ustoken
                member.memberdate = datetime.now()
                member.save()
                # 货币
                memberwallet = MemberWallet()
                memberwallet.coin = 5
                memberwallet.id = len(MemberWallet.objects.values()) + 1
                memberwallet.user_id = userid
                memberwallet.ustoken = ustoken
                memberwallet.walletdate = datetime.now()
                memberwallet.expdate = time_controller(days=30, day=datetime.now())
                memberwallet.save()
                # 用户信息
                userinfo = Userinfo()
                userinfo.invite = invitecode
                userinfo.nick = username.split('@')[0]
                userinfo.icon = 1
                userinfo.id = len(Userinfo.objects.values()) + 1
                userinfo.email = email
                userinfo.ustoken = ustoken
                userinfo.user_id_id = userid
                userinfo.apply_status = 0
                userinfo.iscontributor = 0
                userinfo.edit_rights = 10
                userinfo.userinfodate = datetime.now()
                userinfo.save()
                # 付款信息
                payinfo = Payinfo()
                payinfo.id = len(Payinfo.objects.values()) + 1
                payinfo.user_id = userid
                payinfo.paymentdate = datetime.now()
                payinfo.save()
                return HttpResponse("success")
            else:
                return HttpResponse("error")
        else:
            return HttpResponse("⚠️ Refresh the page and re-register")
    else:
        return HttpResponse("")


@ratelimit(key='ip', rate='30/30m', block=True)
def email_check(request):
    if request.method == "GET":
        email = request.GET.get("email")
        type = request.GET.get('type')
        allemail = [i['email'] for i in User.objects.all().values()]
        if email in allemail:
            hasaccount = True
        else:
            hasaccount = False

        if '@' in email and len(email) > 6 and not hasaccount:
            hasemail = True
        else:
            hasemail = False

        def random_str(randomlength=4):
            import random
            codekey = ''
            chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
            length = len(chars) - 1
            for i in range(randomlength):
                codekey += chars[random.randint(0, length)]
            return codekey

        def email_format():
            subject = 'Alldio_Code'
            text_content = 'Regist'
            code = random_str()
            request.session["email_code"] = code
            request.session["email"] = email
            html_content = f'<h3>Your Regist Code,' \
                           f'Do not share anyone</h3><h1>' \
                           f'<font style="background-color:darkgray;color: #3F3F3F" >{code}</font></h1>'
            from_email = settings.DEFAULT_FROM_EMAIL
            receive_email_addr = [email]
            msg = EmailMultiAlternatives(subject, text_content, from_email, receive_email_addr)
            return (msg, html_content)

        if hasemail:
            (msg, html_content) = email_format()
            msg.attach_alternative(html_content, 'text/html')
            try:
                msg.send()
                return HttpResponse("success")
            except:
                return HttpResponse("⚠️ Please check whether your email is working properly")
        else:
            if not hasaccount:
                return HttpResponse("⚠️ The account was not found")
            else:
                if type == 'reset':
                    (msg, html_content) = email_format()
                    msg.attach_alternative(html_content, 'text/html')
                    try:
                        msg.send()
                        return HttpResponse("success")
                    except:
                        return HttpResponse("⚠️ Please check whether your email is working properly")
                else:
                    return HttpResponse("⚠️ The email address has been registered")
    else:
        return HttpResponse('')


@ratelimit(key='ip', rate='10/10m', block=True)
def email_codecheck(request):
    if request.method == 'GET':
        code = request.GET.get('code')
        if request.session['email_code'] == code:
            return HttpResponse('success')
        else:
            return HttpResponse('⚠️ The email verification code is incorrect')
    else:
        return HttpResponse('')


@validate_codemail
def pswrd_reset(request):
    if request.method == "GET":
        code = request.GET.get('code')
        email = request.GET.get('email')
        password = request.GET.get('password')
        username = User.objects.filter(email=email)[0]
        user = User.objects.get(username=username)
        if 'email_code' in request.session.keys():
            if code == request.session['email_code']:
                user.set_password(password)
                user.save()
                request.session.flush()
                return HttpResponse('success')
            else:
                return HttpResponse('⚠️ Verification code error')
        else:
            return HttpResponse('⚠️ Verification code out of date')
    else:
        return HttpResponse('')


@already_login
def signout(request):
    logout(request)
    return render(request, 'signup.html')


@ratelimit(key='ip', rate='10/10m', block=True)
def login_check(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse('success')
        else:
            return HttpResponse('⚠️ The user name or password is incorrect')
    else:
        return HttpResponse('API Method Error')


def get_main_infos():
    main_infos = {
        'jobs': ['Create', 'Publish', 'Invest'],
        'titles': [
            {
                'name': 'Welcome',
                'href': 'http://www.alldio.xyz',
            },
            {
                'name': '|',
                'href': '#',
            },
            {
                'name': 'WhitePaper',
                'href': 'https://docs.alldio.xyz',
            },
            {
                'name': '|',
                'href': '#',
            },
            {
                'name': 'EarlyBird',
                'href': 'http://www.alldio.xyz/signup',
            },
            {
                'name': '|',
                'href': '#',
            },
            {
                'name': 'Help',
                'href': '#',
            },
        ]
    }
    return main_infos


def loggin(print_input):
    import logging
    logger = logging.getLogger('django')
    logger.error(print_input)


# [ Main Window ] ---------------------------------
def signup(request):
    jobs = get_main_infos()['jobs']
    titles = get_main_infos()['titles']
    msg = {
        'jobs': jobs,
        'titles': titles,
    }
    return render(request, 'signup.html', msg)


def universe(request):
    jobs = get_main_infos()['jobs']
    titles = get_main_infos()['titles']
    msg = {
        'jobs': jobs,
        'titles': titles,
    }
    return render(request, 'universe.html', msg)


@already_login
def usrpanel(request):
    from metasite.dailytools.tools.thounds_split import thousands_split
    userid = request.user.id
    avatar_icons = [
        'https://cdn-icons-png.flaticon.com/128/2436/2436683.png',
        'https://cdn-icons-png.flaticon.com/128/3667/3667290.png',
        'https://cdn-icons-png.flaticon.com/512/3667/3667820.png',
        'https://cdn-icons-png.flaticon.com/128/3667/3667740.png',
        'https://cdn-icons-png.flaticon.com/128/3284/3284037.png',
        'https://cdn-icons-png.flaticon.com/128/2945/2945408.png',
        'https://cdn-icons-png.flaticon.com/128/2945/2945303.png',
        'https://cdn-icons-png.flaticon.com/128/5976/5976179.png',
        'https://cdn-icons-png.flaticon.com/128/4092/4092655.png',
    ]
    userinfo_objs = Userinfo.objects.filter(user_id_id=userid)
    # [ market cards ] ---------------------------------
    marketcard_objs = Cards.objects.filter(saleif='store')
    new_marketcard_titles = get_obj_value('title', marketcard_objs, '-carddate')
    new_marketcard_types = get_obj_value('type', marketcard_objs, '-carddate')
    new_marketcard_tokens = get_obj_value('cdtoken', marketcard_objs, '-carddate')
    new_marketcard_prices = get_obj_value('price', marketcard_objs, '-carddate')
    new_marketcard_intro = get_obj_value('intro', marketcard_objs, '-carddate')
    new_marketcards = [
        ({
            'title': new_marketcard_titles[i],
            'type': new_marketcard_types[i],
            'code': new_marketcard_tokens[i],
            'price': thousands_split(new_marketcard_prices[i]),
            'detail': new_marketcard_intro[i],
        }) for i in range(len(new_marketcard_titles))]
    # [ top cards ] ---------------------------------
    top_marketcard_titles = get_obj_value('title', marketcard_objs, 'value')
    top_marketcard_types = get_obj_value('type', marketcard_objs, 'value')
    top_marketcard_tokens = get_obj_value('cdtoken', marketcard_objs, 'value')
    top_marketcard_prices = get_obj_value('price', marketcard_objs, 'value')
    top_marketcard_intro = get_obj_value('intro', marketcard_objs, 'value')
    top_marketcards = [
        ({
            'title': top_marketcard_titles[i],
            'type': top_marketcard_types[i],
            'code': top_marketcard_tokens[i],
            'price': thousands_split(top_marketcard_prices[i]),
            'detail': top_marketcard_intro[i],
        }) for i in range(len(top_marketcard_titles))]
    # [ market songs ] ----------------------------------
    marketsong_objs = Music.objects.filter(status='online')
    new_marketsong_songnms = get_obj_value('songnm', marketsong_objs, '-createdate')
    new_marketsong_covers = get_obj_value('cover', marketsong_objs, '-createdate')
    new_marketsong_price = get_obj_value('price', marketsong_objs, '-createdate')
    new_marketsong_value = get_obj_value('value', marketsong_objs, '-createdate')
    new_marketsong_genre = get_obj_value('genre', marketsong_objs, '-createdate')
    new_marketsong_url = get_obj_value('url', marketsong_objs, '-createdate')
    new_marketsong_intro = get_obj_value('intro', marketsong_objs, 'createdate')
    new_marketsong_token = get_obj_value('mstoken', marketsong_objs, 'createdate')
    new_marketsongs = [
        ({
            'title': new_marketsong_songnms[i],
            'covers': new_marketsong_covers[i],
            'genre': new_marketsong_genre[i],
            'value': new_marketsong_value[i],
            'price': thousands_split(new_marketsong_price[i]),
            'url': new_marketsong_url[i],
            'code': new_marketsong_token[i],
            'detail': new_marketsong_intro[i],
        }) for i in range(len(new_marketsong_songnms))]
    # [ top songs ] ----------------------------------
    top_marketsong_songnms = get_obj_value('songnm', marketsong_objs, '-value')
    top_marketsong_covers = get_obj_value('cover', marketsong_objs, '-value')
    top_marketsong_url = get_obj_value('url', marketsong_objs, '-value')
    top_marketsong_price = get_obj_value('price', marketsong_objs, '-value')
    top_marketsong_genre = get_obj_value('genre', marketsong_objs, '-value')
    top_marketsong_value = get_obj_value('value', marketsong_objs, '-value')
    top_marketsong_intro = get_obj_value('intro', marketsong_objs, '-value')
    top_marketsong_token = get_obj_value('mstoken', marketsong_objs, '-value')
    top_marketsongs = [
        ({
            'title': top_marketsong_songnms[i],
            'covers': top_marketsong_covers[i],
            'genre': top_marketsong_genre[i],
            'value': top_marketsong_value[i],
            'price': thousands_split(top_marketsong_price[i]),
            'url': top_marketsong_url[i],
            'code': top_marketsong_token[i],
            'detail': top_marketsong_intro[i],
        }) for i in range(len(top_marketsong_songnms))]
    # [ songs ] ----------------------------------
    usersong_objs = Music.objects.filter(owner=userid)
    song_titles = get_obj_value('title', usersong_objs, 'id')
    song_status = get_obj_value('status', usersong_objs, 'id')

    # song_minters = get_obj_value('minter', usersong_objs, 'id')

    def get_song_founder_icons():
        song_founder_ids = [i.split(',') for i in get_obj_value('founder', usersong_objs, 'id')]

        song_founder_icons = []
        for i in range(len(song_founder_ids)):
            founders = song_founder_ids[i]
            icons = []
            for a in range(len(founders)):
                icon_id = get_obj_value('icon', Userinfo.objects.filter(user_id_id=founders[a]), 'id')[0]
                icons.append(avatar_icons[int(icon_id) - 1])
            song_founder_icons.append(icons)
        return song_founder_icons

    song_founder_icons = get_song_founder_icons()  # ♻️
    song_tokens = get_obj_value('mstoken', usersong_objs, 'id')
    song_urls = get_obj_value('url', usersong_objs, 'id')
    song_createdates = get_obj_value('createdate', usersong_objs, 'id')
    song_dates = [str(i).split(' ')[0] for i in song_createdates]
    try:
        web_songs = [
            ({'token': song_tokens[i],
              'title': song_titles[i],
              'status': song_status[i],
              'url': song_urls[i],
              'date': song_dates[i],
              'founders': song_founder_icons[i],
              }) for i in range(len(song_titles))]
    except:
        web_songs = []

    # [ cards ] ----------------------------------
    usercard_objs = Cards.objects.filter(user_id=userid)
    card_titles = get_obj_value('title', usercard_objs, 'id')
    card_ids = get_obj_value('cdtoken', usercard_objs, 'id')
    card_icons = get_obj_value('icon', usercard_objs, 'id')
    card_types = get_obj_value('type', usercard_objs, 'id')
    card_levels = get_obj_value('level', usercard_objs, 'id')
    card_details = get_obj_value('intro', usercard_objs, 'id')
    card_tokens = get_obj_value('cdtoken', usercard_objs, 'id')
    card_saleif = get_obj_value('saleif', usercard_objs, 'id')
    try:
        web_cards = [
            ({
                'title': card_titles[i],
                'id': card_ids[i],
                'icon': card_icons[i],
                'type': card_types[i],
                'level': card_levels[i],
                'detail': card_details[i],
                'saleif': card_saleif[i],
                'token': card_tokens[i],
            }) for i in range(len(card_titles))
        ]
    except:
        web_cards = []
    webcards_count = len(web_cards)
    # [ royalties ] --------------------------------------------
    user_songids = get_obj_value('id', usersong_objs, 'id')
    royalty_objs = Royalty.objects.filter(song_id__in=user_songids)
    royalty_songids = get_obj_value('song_id', royalty_objs, 'song_id')
    usersong_royalty_objs = Music.objects.filter(id__in=royalty_songids)
    royalty_songtitles = get_obj_value('title', usersong_royalty_objs, 'id')
    royalty_songprices = get_obj_value('price', royalty_objs, 'song_id')
    royalty_songdate = get_obj_value('date', royalty_objs, 'song_id')
    royalty_songstreams = get_obj_value('quantity', royalty_objs, 'song_id')
    web_royalties = [
        ({
            'title': royalty_songtitles[i],
            'price': thousands_split(royalty_songprices[i]),
            'date': royalty_songdate[i],
            'stream': thousands_split(royalty_songstreams[i]),
        }) for i in range(len(royalty_songtitles))]
    royalty_songscount = len(web_royalties)
    # --------------------------------------------
    news_allow = ['all', str(userid)]
    notification_objs = Notification.objects.filter(allow__in=news_allow)
    notification_dates = get_obj_value('notificationdate', notification_objs, 'notificationdate')
    notification_types = get_obj_value('type', notification_objs, 'notificationdate')
    notification_contents = get_obj_value('content', notification_objs, 'notificationdate')
    news_icons = {
        'news': 'https://cdn-icons-png.flaticon.com/128/3315/3315547.png',
        'mint': 'https://cdn-icons-png.flaticon.com/128/9421/9421230.png',
        'compose': 'https://cdn-icons-png.flaticon.com/128/9431/9431347.png',
    }
    try:
        notification_icons = [news_icons[notification_types[i]] for i in range(len(notification_types))]
    except:
        notification_icons = ['https://cdn-icons-png.flaticon.com/128/3315/3315547.png' for _ in
                              range(len(notification_types))]
    newses = [({
        'icon': notification_icons[i],
        'date': str(notification_dates[i]).split(' ')[0].replace('-', '/'),
        'type': notification_types[i],
        'content': notification_contents[i],
    }) for i in range(len(notification_icons))]
    # [ messagebox ] --------------------------------------------
    message_objs = Messagebox.objects.filter(touserid=userid)
    message_sender_ids = get_obj_value('user_id', message_objs, 'id')
    message_contents = get_obj_value('content', message_objs, 'id')
    message_dates = get_obj_value('messageboxdate', message_objs, 'id')
    try:
        message_sender_usernames = [];
        message_sender_icons = []
        for i in range(len(message_sender_ids)):
            if str(message_sender_ids[i]) != '999999999':
                message_sender_icon = avatar_icons[int(i)]
                message_sender_username = \
                    get_obj_value('nick', Userinfo.objects.filter(user_id_id=message_sender_ids[i]), 'id')
            else:
                message_sender_icon = 'https://cdn-icons-png.flaticon.com/128/2797/2797403.png'
                message_sender_username = ['Dio']
            message_sender_usernames.append(message_sender_username)
            message_sender_icons.append(message_sender_icon)
    except:
        message_sender_usernames = ['****']
        message_sender_icons = ['https://cdn-icons-png.flaticon.com/128/2797/2797403.png']

    try:
        messages = [(
            {
                'messageuser': message_sender_usernames[i][0],
                'message': message_contents[i],
                'messdate': str(message_dates[i]).split(' ')[0].replace('-', '/'),
                'iconlink': message_sender_icons[i],
            }) for i in range(len(message_contents))
        ]
    except:
        messages = []
    # [ royalties ] ----------------------------------
    titles = get_main_infos()['titles']

    websong_count = len(web_songs)

    try:
        coins = get_obj_value(tag='coin', obj=MemberWallet.objects.filter(user_id=userid), order='id')[0]
    except:
        coins = 0

    current_wallet = 0

    try:
        member_outdate_a = get_obj_value('outdate', Member.objects.filter(user_id=userid), 'id')[0].split('.')[0]
        member_outdate = member_outdate_a.replace('-', '.')
        if len(member_outdate) == 0:
            member_outdate = get_nowtime()
    except:
        member_outdate = get_nowtime()
    # [ rest time ] ----------------------------------
    resttime = get_time_delta(get_nowtime(), member_outdate)  # ♻️

    # [ one data ] ----------------------------------
    try:
        nickname = get_obj_value('nick', Userinfo.objects.filter(user_id_id=userid), 'id')[0]
        userbrand = get_obj_value('group', Userinfo.objects.filter(user_id_id=userid), 'id')[0]
    except:
        nickname = ''
        userbrand = 'Alldio'
    salesongs = Music.objects.filter(saleif='stored').values()
    salecards = Cards.objects.filter(saleif='stored').values()
    salesong_count = thousands_split(len(salesongs))
    salecard_count = thousands_split(len(salecards))
    try:
        useremail = request.user.email
    except:
        useremail = ''

    try:
        userlevel = get_obj_value('level', Member.objects.filter(user_id=userid), 'id')[0]
    except:
        userlevel = 0

    subscriptions = Subscription.objects.values()
    try:
        current_subscription = int(get_obj_value('type', Member.objects.filter(user_id=userid), 'id')[0])
    except:
        current_subscription = 1
    current_subscription_name = get_obj_value('title', Subscription.objects.filter(type=current_subscription), 'id')[0]
    current_subscription_icon = get_obj_value('icon', Subscription.objects.filter(type=current_subscription), 'id')[0]
    try:
        current_avatar_id = int(get_obj_value('icon', Userinfo.objects.filter(user_id=userid), 'id')[0])
    except:
        current_avatar_id = 99

    if current_avatar_id != 9999:
        try:
            current_avataricon = avatar_icons[current_avatar_id - 1]
        except:
            current_avataricon = 'https://cdn-icons-png.flaticon.com/128/4092/4092655.png'
    else:
        current_avataricon = 'https://cdn-icons-png.flaticon.com/128/924/924915.png'
    try:
        royaltypaydate = get_obj_value('royaltypayday', Userinfo.objects.filter(user_id_id=userid), 'id')[-1]
    except:
        royaltypaydate = 'No Royalty Yet'
    try:
        royalty_incomes = round(sum(float(i) for i in royalty_songprices), 2)
    except:
        royalty_incomes = 0

    invoice = royalty_incomes
    userinfos = {
        'useremail': useremail,
        'nickname': nickname,
    }
    wallets = [
        {
            'icon': 'https://static.opensea.io/logos/walletconnect-alternative.png',
            'title': 'WalletConnect',
            'href': '',
        },
        {
            'icon': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/MetaMask_Fox.svg/800px-MetaMask_Fox.svg.png',
            'title': 'MetaMask',
            'href': '',
        },
        {
            'icon': 'https://lh3.googleusercontent.com/uBaatYG20TOMFFUCTEgwtaI9Q6l_Nqr0qKUGQPJHjKnlLDqhwQaQbAvQku4nyH8TVxZKx96RsiFduLrcw2vqqjrr=s48',
            'title': 'BitKeep',
            'href': '',
        },
    ]
    payments = [
        {
            'icon': 'https://cdn-icons-png.flaticon.com/128/5968/5968299.png',
            'title': 'Creidt Card',
            'href': '',
        },
        {
            'icon': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOEAAADhCAMAAAAJbSJIAAAA6lBMVEX///8DL4YUnN4BIWkAI4KAirMAIIICJXEVoOKVosMAlNwALYUAE2AAmuAAKoQNcrQAKIMAHIEAG2WCwOkAFn8AGmQAJYICKHYDLYEAF2MMaKrn9Pvl6fGd1PEAF4Hs8PYAD38hR5S1wtsANY7M1eYHR4pVtegRiswAEF/c4u10vuna7/mq2fKAx+4QgcbQ6feHmb9VbafDz+IyU5oQQZVsgLGquNMjRpRqf7J3h7NKZKOSosZCWpugrcw7g7o6rOcEMXcGO38JV5kENHkLYKIKWqQOcroLYqyo1/C74vVhuOgIT52OzvBdcadTS3TIAAAHJElEQVR4nO2cAVvaSBCGYUVMWTZCrlBD8dCKorZFi9TqtR5qvbtq7f//O5dARZTATJLd2W2feX+Aj++zybezkx0KBYZhGIZhGIZhGIZhGIZhGIZhGIZhGCY1nYvVbByfdrudju1/H+a4WS9lpP7ny7K//WH1YuCy50ldFnMgpV+LTYcfT9u2VZL5UM7j94jfrG8Nj7u2deYZbOkRHCNL5e0Xrq3keUmjYeTol4vnB7alnnDiazWMJUs75w7lTsfPFTMLHMufTm2LTTl4qV8wwq+fubKMb+pGDIvF8okjb+NnTXvFPDXfjZ1Dc5TO4m85sYp/1YwZRoHjwNbYGRqI0im1bftx0zb3kMaUz2wLFgZmNosHZN36vnhhLEon+EPbr6LBKJ1Q/mjZ8IfBKB0ja3Z3xY7+uvs5Jbth094xuVmMkTtW9/2uqap0hvJnm4anBIb+iU3DY8ObRYyUNh/TH03zhsWyzV3/i+nNIqZ0bk+wbbTufqBm8UU8oFjCohzaMxwQRGncYLR3hjLXwnhC016YnlFEaRQ19kpTkiiNtgtrhp1t43W3ZcMD83X3GHtP6aBMZGgtaXAtjI1Xa3heRWxsPPsLNWu7BaqFsbaShUh16imlLUFUNziT31RzbOlvWzP8BEfpqzyGY8noIf1iSxDTwsgpOJZsrtoy7MIVzYYGw5X9v48sGZ7CUarFsNFX7+0YHoNRKvO+hhMqQo2sLOMH+CnNtlU8JbgUQijv1oIhIko1CK4Eu56IeUcuiLmFocMwbE0MFfkqHiAqGh2GQX9iKLy3xIZviKL0UvxEjYgNES0MHVH68BrGisSbBqKFoSNKw/WpoVC0zynigK9BcCXozRjekRoiDoc6BK/EDKSL2EbcK9VgGN54s4aUb+LgT1BQR5Q2erOGwiM0vID73Rqi9OlDKkSFsD6F624dhtXWkyUU6p7OENHC0LFZqKdrKPboDBEf1vL7Na69Z4Z0L2IHMWSR33C/99xQvaYy7FJE6UzFNjUkO2EgbmHkN9zvPRcUapPKEHELI3eUJiyhUH9QGVLU3fNvIaUh4kJbXsP5ICU1pGhhPN8LSQ0RgyR5g6a6nrCEdIaIQZKcho2EmKE0NN7CCC6TnlHCwhTx6TBf0DT6iUsoFFXb1HTdHbaSBYUiOj51PpmN0vA62Y+uLm2b/bAW7i4SJDtbdI1uFuGVWPCMCkHVFUbcwsgepcsE1SGRISJKMxtWkzfCn4ZURwvEIEnWKN2/WSJIdjzEDJJk8wuCxFrt0ZAqSuFbGNmCpnqVcGCyETRduEmTxbARtBZnzGQJqXreRloYQXUXWEDCLo2BFkYQfu0DCxgbEgnqb2FEfuuwH+FXYMTt5zSGYWO378F+hLshYpAE/RoG4f5lq4fyI/x8iBgkQRlGduEVWi8SJPtogRgkWW4YBI2wWl3bvYnCBe1HePrFtjBiiwTClbWvu9etfi+VXYxH9s3iDNPCCC+vW+tz9Pu9XtyA8dLaCdJP3IgWxkpwo7wFpDWbLiHZNQXEIIlsLC+gs0B2NEQNkvhLj0DZILzWBg+SyA3tfpRLiGhh+P8YWEKyIMW0MGr/ajeskH0ZLWCitLmgYZ0dunImBo7SZkWzoBCkF9rAKJVStx9dvRYDD5LIoeaHlDJHC5jbz7qjlPr6M3yhTXOUqhHhRhEDD5LojVJyQUSUlsCemdOCiEGSmj4/4o1wDDxIInf0LSFxio6Bo1R+12WoLAw7FQov4M3iP02Gao96DmgM3A329WwWyqMstmf4DkZpTcdmobz31Bn6ANxn8/PX3ZGflQc0BjFIspNXT402ba1fATNIkqvuVqoyurc1uj0BHiTJWneriNHhN2tP5wOruupu9UilorzR3uHmrcVn8xG4heH3MX7i7n5zzLd3t7dHr+3/XvAU+MOanL9gPy9oZy/HgBgkQUSphXIaDTxIgolS8qnsFMC3MHy47rZxYEADfzqswXU3/W8HpACuuxFVqcsPKWKQRMItDPK+RBrgFsYOXHc7nKSIQRI5BAWFy0EDD5IgWhiUs7yp+f2jVM+nQ5ejVEvdTfk1Ny0dxA8ngXU3+c/MpAEeJEFEKfEPlKQDHiTBVKWWfnwNhZZbGLTfc1OipYVBNX2WCXiQBFN3uxylYN0tES0Ml6MUMd4MtzCcjtIDsN8tt2FDl6O0XYTOTpgotfRFCccx1IfCRKnLdXehcLZVXspLOErpfmAmG4MXS/kMvoakv9ZlgNfw0cnlFgaCI1DQ6V4pgtvkn3qYNXQ6SmHuYUO3oxTkDjZ0uYWBYAS+h8L2v5gPRJS6XHcjOIL3e5frbgSIKHW5G4xgEzZ0uYWB4BA2dLmFgQCOUrJxc0P89lFagJfwF6/ZCiPgPXS6oY/iSC1TVC5fo8Hydq+yEHX3ixfdDMMwDMMwDMMwDMMwDMMwDMMwDMMwDGOQ/wH+YuDLDiZk8wAAAABJRU5ErkJggg==',
            'title': 'Paypal',
            'href': '',
        },
        {
            'icon': 'https://www.apistack.io/_next/image?url=https%3A%2F%2Fres.cloudinary.com%2Fapideck%2Fimage%2Fupload%2Fw_auto%2Cf_auto%2Fv1619319113%2Ficons%2Fstripe-billing.svg&w=3840&q=75',
            'title': 'Stripe',
            'href': '',
        },
    ]
    awards = [
        {
            'title': 'Project',
            'price': '15',
            'icon': 'https://cdn-icons-png.flaticon.com/128/1705/1705317.png',
        },
        {
            'title': 'Clip',
            'price': '10',
            'icon': 'https://cdn-icons-png.flaticon.com/128/2611/2611288.png',
        },
        {
            'title': 'Model',
            'price': '8',
            'icon': 'https://cdn-icons-png.flaticon.com/128/9417/9417817.png',
        },
        {
            'title': 'Shot',
            'price': '6',
            'icon': 'https://cdn-icons-png.flaticon.com/128/4098/4098328.png',
        },
    ]
    contributors = [
        {
            'title': 'Arrangementor',
            'icon': 'https://cdn-icons-png.flaticon.com/128/3271/3271164.png ',
        },
        {
            'title': 'Composer',
            'icon': 'https://cdn-icons-png.flaticon.com/128/9087/9087110.png',
        },
        {
            'title': 'SoundDesigner',
            'icon': 'https://cdn-icons-png.flaticon.com/128/6653/6653609.png',
        },
    ]

    try:
        wallet_address = get_session_value(request, 'wallet_address')
        wallet_balance = get_session_value(request, 'wallet_balance')
        wallet_network = get_session_value(request, 'wallet_network')
        wallet_address_abv = wallet_address[0:5] + ' ... ' + wallet_address[-5:-1]
    except:
        wallet_balance = []
        wallet_network = []
        wallet_address = []
        wallet_address_abv = []
    user_rights = get_obj_value('right', Member.objects.filter(user_id=userid), 'id')[0]
    rest_chances = thousands_split(int(user_rights))
    artmodel_count = 10
    isPlayer = False
    hasCard = True
    apply_status = get_obj_value('apply_status', userinfo_objs, 'id')[0]
    if int(apply_status) >= 1:
        isApplingContributor = True
    else:
        isApplingContributor = False
    user_streams = sum([int(i) for i in get_obj_value('quantity', royalty_objs, 'id')])
    if user_streams > 999:
        user_streams = thousands_split(int(user_streams / 1000)) + 'k'
    else:
        if user_streams > 1000000:
            user_streams = thousands_split(int(user_streams / 1000000, 1)) + 'm'
    fastviews = [
        {
            'title': 'Cards',
            'icon': '',
            'href': '',
            'value': webcards_count,
        },
        {
            'title': 'Songs',
            'icon': '',
            'href': '',
            'value': websong_count,
        },
        {
            'title': 'Stream',
            'icon': '',
            'href': '',
            'value': user_streams,
        },
        {
            'title': current_subscription_name,
            'icon': current_subscription_icon,
            'href': '',
            'value': '',
        },
    ]
    games = [
        {
            'title': 'CardBox',
            'icon': 'https://cdn-icons-png.flaticon.com/128/6545/6545501.png',
            'href': 'luckybox',
            'hint': '',
        },
        {
            'title': 'Compose',
            'icon': 'https://cdn-icons-png.flaticon.com/128/9465/9465132.png',
            'href': 'generate',
            'hint': '',
        },
        {
            'title': 'Museum',
            'icon': 'https://cdn-icons-png.flaticon.com/128/2400/2400568.png',
            'href': 'cardtrade',
            'hint': '',
        },
        {
            'title': 'Discord',
            'icon': 'https://cdn-icons-png.flaticon.com/128/2111/2111370.png',
            'href': 'https://discord.gg/BRqb9bqzwW',
            'hint': 'limit 100 person',
        },
    ]
    paymethods = {
        'credit': 1,
        'paypal': 2,
        'stripe': 3,
    }
    usertoken = get_obj_value('ustoken', Member.objects.filter(user_id=userid), 'id')[0]
    current_paymethod = get_obj_value('paymethod', Userinfo.objects.filter(user_id_id=userid), 'id')[0]
    try:
        current_payment = paymethods[current_paymethod]
    except:
        current_payment = 1

    nowpath = request.get_full_path()
    nowtab = 1
    nowsubtab = 2
    nowdark = 'day'

    payinfo_obj = Payinfo.objects.filter(user_id=userid)
    expmonth = get_obj_value('expmonth', payinfo_obj, 'id')[0]
    expyear = get_obj_value('expyear', payinfo_obj, 'id')[0]
    cardnumbers = get_obj_value('cardnum', payinfo_obj, 'id')[0].split(' ')
    if len(cardnumbers) > 4:
        cardnumber = f'{cardnumbers[0]} **** **** {cardnumbers[3]}'
    else:
        cardnumber = '**** **** **** ****'

    print('nowtab', get_session_value(request, 'nowtab'))
    print('nowsubtab', get_session_value(request, 'nowsubtab'))
    try:
        if get_session_value(request, 'nowtab'):
            nowtab = get_session_value(request, 'nowtab')
        if get_session_value(request, 'nowsubtab'):
            nowsubtab = get_session_value(request, 'nowsubtab')
        if get_session_value(request, 'nowdark'):
            nowdark = get_session_value(request, 'nowdark')
    except:
        pass
    print(new_marketsongs)
    # [ msg ] ---------------------------------------
    msg = {
        # [ global ] ----------------------------
        'titles': titles,
        'nowtab': nowtab,
        'nowsubtab': nowsubtab,
        'nowdark': nowdark,
        # [ Home ] ------------------------------
        'userinfos': userinfos,
        'fastviews': fastviews,
        'messages': messages,
        'newses': newses,
        'games': games,
        # [ Tube ] ---------------------------
        'giftcards': giftcards,
        'rest_chances': rest_chances,
        'artmodel_count': artmodel_count,
        'awards': awards,
        'contributors': contributors,
        'isPlayer': isPlayer,
        'isApplingContributor': isApplingContributor,
        # [ library ] ---------------------------
        'card_count': webcards_count,
        'song_count': websong_count,
        'userbrand': userbrand,
        'cards': web_cards,
        'songs': web_songs,
        # [ market ] ----------------------------
        'salesong_count': salesong_count,
        'salecard_count': salecard_count,
        'new_marketsongs': new_marketsongs,
        'top_marketsongs': top_marketsongs,
        'new_marketcards': new_marketcards,
        'top_marketcards': top_marketcards,
        # [ royalty ] ---------------------------
        'web_royalties': web_royalties,
        'royaltypaydate': royaltypaydate,
        'royalty_songscount': royalty_songscount,
        # [ payment ] ---------------------------
        'payments': payments,
        'coins': coins,
        'invoice': invoice,
        'wallets': wallets,
        'wallet_address': wallet_address,
        'wallet_balance': wallet_balance,
        'wallet_network': wallet_network,
        'wallet_address_abv': wallet_address_abv,
        'hasCard': hasCard,
        'expmonth': expmonth,
        'expyear': expyear,
        'cardnumber': cardnumber,
        # [ user ] ------------------------------
        'usercode': usertoken,
        'avatars': avatar_icons[0:8],
        # [ subscription ] ----------------------
        'resttime': resttime,
        'subscriptions': subscriptions,
        'buycoins': buycoins,
        # [ current ] ---------------------------
        'current_subscription': current_subscription + 1,
        'current_payment': current_payment,
        'current_wallet': current_wallet,
        'current_avataricon': current_avataricon,
        'current_subscription_name': current_subscription_name,
    }
    delete_reqeust(request, 'nowtab')
    delete_reqeust(request, 'nowsubtab')
    delete_reqeust(request, 'nowdark')
    return render(request, 'usrpanel.html', msg)


def error404(request, exception):
    return render(request, 'error404.html')
