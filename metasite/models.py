from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import smart_str
from django.contrib.auth.models import AbstractUser


# 注册信息 -----------------------------------------------------------------------------------------------------------
class User(AbstractUser):
    phone = models.CharField(max_length=50, null=True, verbose_name="phone")
    invite = models.CharField(max_length=50, null=True, verbose_name="invite")
from django.contrib.auth import get_user_model

User = get_user_model()


# 邀请信息 -----------------------------------------------------------------------------------------------------------
class InviteCode(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(_(u'邀请码'), max_length=250)
    note = models.CharField(_(u'备注'), max_length=250)
    status = models.CharField(_(u'状态'), max_length=250)
    codedate = models.DateTimeField(u'创建时间', auto_now=True)

    class Meta:
        verbose_name = _(u'InviteCode')
        verbose_name_plural = _(u'InviteCode')
        ordering = ['-codedate']


# 行为日志 ----------------------------------------------------------------------------------------------------------
class OpLogs(models.Model):
    id = models.AutoField(primary_key=True)
    re_time = models.CharField(max_length=32, verbose_name='请求时间')
    re_user = models.CharField(max_length=32, verbose_name='操作人')
    re_ip = models.CharField(max_length=32, verbose_name='请求IP')
    re_url = models.CharField(max_length=255, verbose_name='请求url')
    re_method = models.CharField(max_length=11, verbose_name='请求方法')
    re_content = models.TextField(null=True, verbose_name='请求参数')
    rp_content = models.TextField(null=True, verbose_name='响应参数')
    access_time = models.IntegerField(verbose_name='响应耗时/ms')

    class Meta:
        db_table = 'op_logs'


class AccessTimeOutLogs(models.Model):
    id = models.AutoField(primary_key=True)
    re_time = models.CharField(max_length=32, verbose_name='请求时间')
    re_user = models.CharField(max_length=32, verbose_name='操作人')
    re_ip = models.CharField(max_length=32, verbose_name='请求IP')
    re_url = models.CharField(max_length=255, verbose_name='请求url')
    re_method = models.CharField(max_length=11, verbose_name='请求方法')
    re_content = models.TextField(null=True, verbose_name='请求参数')
    rp_content = models.TextField(null=True, verbose_name='响应参数')
    access_time = models.IntegerField(verbose_name='响应耗时/ms')

    class Meta:
        db_table = 'access_timeout_logs'


# 内容信息 ----------------------------------------------------------------------------------------------------------
class Music(models.Model):
    title = models.CharField(_(u'标题'), max_length=250)
    prompt = models.CharField(_(u'设想'), max_length=250)
    songnm = models.CharField(_(u'歌名'), max_length=250)
    value = models.CharField(_(u'指数'), max_length=250)
    price = models.CharField(_(u'价值'), max_length=250)
    tag = models.CharField(_(u'标签'), max_length=250)
    genre = models.CharField(_(u'风格'), max_length=250)
    emo = models.CharField(_(u'情绪'), max_length=250)
    inst = models.CharField(_(u'乐器'), max_length=250)
    tempo = models.CharField(_(u'速度'), max_length=250)
    length = models.CharField(_(u'时长'), max_length=250)
    beat = models.CharField(_(u'拍号'), max_length=250)
    scale = models.CharField(_(u'调性'), max_length=250)
    cover = models.CharField(_(u'封面'), max_length=250)
    url = models.CharField(_(u'链接'), max_length=250)
    wavform = models.CharField(_(u'波形'), max_length=250)
    label = models.CharField(_(u'厂牌'), max_length=250)
    founder = models.CharField(_(u'发现'), max_length=250)
    owner = models.CharField(_(u'拥有'), max_length=250)
    minter = models.CharField(_(u'铸造'), max_length=250)
    share = models.CharField(_(u'分配'), max_length=250)
    lyrics = models.CharField(_(u'作词'), max_length=250)
    melody = models.CharField(_(u'作曲'), max_length=250)
    arrange = models.CharField(_(u'编曲'), max_length=250)
    artist = models.CharField(_(u'艺人'), max_length=250)
    mixing = models.CharField(_(u'混音'), max_length=250)
    record = models.CharField(_(u'录音'), max_length=250)
    unit = models.CharField(_(u'元件'), max_length=250)
    cue = models.CharField(_(u'卡点'), max_length=250)
    mstoken = models.CharField(_(u'乐码'), max_length=250)
    intro = models.CharField(_(u'介绍'), max_length=250)
    status = models.CharField(_(u'状态'), max_length=250)
    saleif = models.CharField(_(u'售况'), max_length=250)
    more1 = models.CharField(_(u'更多1'), max_length=250)
    more2 = models.CharField(_(u'更多2'), max_length=250)
    more3 = models.CharField(_(u'更多3'), max_length=250)
    more4 = models.CharField(_(u'更多4'), max_length=250)
    more5 = models.CharField(_(u'更多5'), max_length=250)
    more6 = models.CharField(_(u'更多6'), max_length=250)
    more7 = models.CharField(_(u'更多7'), max_length=250)
    more8 = models.CharField(_(u'更多8'), max_length=250)
    more9 = models.CharField(_(u'更多9'), max_length=250)
    more10 = models.CharField(_(u'更多10'), max_length=250)
    createdate = models.DateTimeField(_(u'日期'), auto_now_add=True)

    def __unicode__(self):
        return smart_str(self.title)

    class Meta:
        verbose_name = _(u'MusicLibrary')
        verbose_name_plural = _(u'MusicLibrary')
        ordering = ['-createdate', 'value', 'price']


class Royalty(models.Model):
    id = models.AutoField(primary_key=True)
    song_id = models.CharField(_(u'结算歌曲'), max_length=250)
    platform = models.CharField(_(u'结算平台'), max_length=250)
    type = models.CharField(_(u'结算类型'), max_length=250)  # 流媒体 / 演出 / 短视频授权使用
    quantity = models.CharField(_(u'结算数量'), max_length=250)  # 流媒体 / 演出 / 短视频授权使用
    price = models.CharField(_(u'结算金额'), max_length=250)
    cointype = models.CharField(_(u'结算币种'), max_length=250)
    source = models.CharField(_(u'报表来源'), max_length=250)
    date = models.CharField(_(u'结算日期'), max_length=250)
    detail = models.CharField(_(u'报表介绍'), max_length=250)
    note = models.CharField(_(u'其它备注'), max_length=250)
    paydate = models.CharField(_(u'结算日'), max_length=250)
    more1 = models.CharField(_(u'更多1'), max_length=250)
    more2 = models.CharField(_(u'更多2'), max_length=250)
    more3 = models.CharField(_(u'更多3'), max_length=250)
    more4 = models.CharField(_(u'更多4'), max_length=250)
    more5 = models.CharField(_(u'更多5'), max_length=250)
    more6 = models.CharField(_(u'更多6'), max_length=250)
    more7 = models.CharField(_(u'更多7'), max_length=250)
    more8 = models.CharField(_(u'更多8'), max_length=250)
    more9 = models.CharField(_(u'更多9'), max_length=250)
    more10 = models.CharField(_(u'更多10'), max_length=250)
    royaltydate = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _(u'Royalty')
        verbose_name_plural = _(u'Royalty')
        ordering = ['-royaltydate']


# 用户操作信息 ----------------------------------------------------------------------------------------------------------
class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(_(u'用户'), max_length=250)
    good = models.CharField(_(u'商品内容'), max_length=250)
    goodtype = models.CharField(_(u'商品类型'), max_length=250)
    paytype = models.CharField(_(u'支付类型'), max_length=250)
    pay = models.CharField(_(u'支付金额'), max_length=250)
    cointype = models.CharField(_(u'支付币种'), max_length=250)
    date = models.CharField(_(u'支付日期'), max_length=250)
    bfrest = models.CharField(_(u'交前余额'), max_length=250)
    afrest = models.CharField(_(u'交后余额'), max_length=250)
    record = models.CharField(_(u'交易记录'), max_length=250)
    note = models.CharField(_(u'交易备注'), max_length=250)
    more1 = models.CharField(_(u'更多1'), max_length=250)
    more2 = models.CharField(_(u'更多2'), max_length=250)
    more3 = models.CharField(_(u'更多3'), max_length=250)
    more4 = models.CharField(_(u'更多4'), max_length=250)
    more5 = models.CharField(_(u'更多5'), max_length=250)
    more6 = models.CharField(_(u'更多6'), max_length=250)
    more7 = models.CharField(_(u'更多7'), max_length=250)
    more8 = models.CharField(_(u'更多8'), max_length=250)
    more9 = models.CharField(_(u'更多9'), max_length=250)
    more10 = models.CharField(_(u'更多10'), max_length=250)
    paymentdate = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _(u'Payment')
        verbose_name_plural = _(u'Payment')
        ordering = ['-paymentdate']


class Favorite(models.Model):
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE)
    song_id = models.ForeignKey(to=Music, on_delete=models.CASCADE)
    collectdate = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _(u'Favorite')
        verbose_name_plural = _(u'Favorite')
        ordering = ['-collectdate']


class Cart(models.Model):
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE)
    song_id = models.ForeignKey(to=Music, on_delete=models.CASCADE)
    cartdate = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _(u'Cart')
        verbose_name_plural = _(u'Cart')
        ordering = ['-cartdate']


class Generate(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(_(u'用户'), max_length=250)
    command = models.CharField(_(u'命令'), max_length=250)
    cards = models.CharField(_(u'卡片'), max_length=250)
    keyword = models.CharField(_(u'关键词'), max_length=1000)
    mstoken = models.CharField(_(u'乐码'), max_length=250)
    more1 = models.CharField(_(u'更多1'), max_length=250)
    more2 = models.CharField(_(u'更多2'), max_length=250)
    more3 = models.CharField(_(u'更多3'), max_length=250)
    more4 = models.CharField(_(u'更多4'), max_length=250)
    more5 = models.CharField(_(u'更多5'), max_length=250)
    more6 = models.CharField(_(u'更多6'), max_length=250)
    more7 = models.CharField(_(u'更多7'), max_length=250)
    more8 = models.CharField(_(u'更多8'), max_length=250)
    more9 = models.CharField(_(u'更多9'), max_length=250)
    more10 = models.CharField(_(u'更多10'), max_length=250)
    generatedate = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _(u'Generateinfo')
        verbose_name_plural = _(u'Generateinfo')
        ordering = ['-generatedate']


# 用户信息 ----------------------------------------------------------------------------------------------------------
class Userinfo(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE)
    invite = models.CharField(max_length=50, null=True, verbose_name="invite")
    nick = models.CharField(_(u'昵称'), max_length=250)
    icon = models.CharField(_(u'头像'), max_length=250)
    speak = models.CharField(_(u'签名'), max_length=250)
    favor = models.CharField(_(u'口味'), max_length=250)
    age = models.CharField(_(u'年龄'), max_length=250)
    sex = models.CharField(_(u'性别'), max_length=250)
    country = models.CharField(_(u'国家'), max_length=250)
    city = models.CharField(_(u'城市'), max_length=250)
    email = models.CharField(_(u'邮箱'), max_length=250)
    email2 = models.CharField(_(u'备邮'), max_length=250)
    phone = models.CharField(_(u'电话'), max_length=250)
    ustoken = models.CharField(_(u'唯码'), max_length=250)
    paymethod = models.CharField(_(u'支付'), max_length=250)
    paywallet = models.CharField(_(u'钱包'), max_length=250)
    royaltypayday = models.CharField(_(u'结算日'), max_length=250)
    discord = models.CharField(_(u'discord'), max_length=250)
    twitter = models.CharField(_(u'twitter'), max_length=250)
    facebook = models.CharField(_(u'facebook'), max_length=250)
    tiktok = models.CharField(_(u'tiktok'), max_length=250)
    social = models.CharField(_(u'账号'), max_length=250)
    language = models.CharField(_(u'语言'), max_length=250)
    friend = models.CharField(_(u'好友'), max_length=25)
    iscontributor = models.CharField(_(u'贡献者'), max_length=250)
    apply_status = models.CharField(_(u'申请状态'), max_length=250)
    edit_rights = models.CharField(_(u'修改次数'), max_length=250)
    ai = models.CharField(_(u'推荐'), max_length=1000)
    group = models.CharField(_(u'群组'), max_length=250)
    more1 = models.CharField(_(u'更多1'), max_length=250)
    more2 = models.CharField(_(u'更多2'), max_length=250)
    more3 = models.CharField(_(u'更多3'), max_length=250)
    more4 = models.CharField(_(u'更多4'), max_length=250)
    more5 = models.CharField(_(u'更多5'), max_length=250)
    more6 = models.CharField(_(u'更多6'), max_length=250)
    more7 = models.CharField(_(u'更多7'), max_length=250)
    more8 = models.CharField(_(u'更多8'), max_length=250)
    more9 = models.CharField(_(u'更多9'), max_length=250)
    more10 = models.CharField(_(u'更多10'), max_length=250)
    userinfodate = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _(u'Userinfo')
        verbose_name_plural = _(u'Userinfo')
        ordering = ['-userinfodate']


class Member(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(_(u'用户ID'), max_length=250)
    ustoken = models.CharField(_(u'用户唯码'), max_length=250)
    type = models.CharField(_(u'会员类型'), max_length=250)
    buydate = models.CharField(_(u'购买日期'), max_length=250)
    outdate = models.CharField(_(u'到期日期'), max_length=250)
    level = models.CharField(_(u'等级信息'), max_length=250)
    honor = models.CharField(_(u'荣誉称号'), max_length=250)
    viphonor = models.CharField(_(u'特殊荣誉'), max_length=250)
    score = models.CharField(_(u'会员积分'), max_length=250)
    musics = models.CharField(_(u'音乐资产'), max_length=250)
    cards = models.CharField(_(u'卡片资产'), max_length=250)
    right = models.CharField(_(u'权限信息'), max_length=250)
    note = models.CharField(_(u'备注信息'), max_length=250)
    more1 = models.CharField(_(u'更多1'), max_length=250)
    more2 = models.CharField(_(u'更多2'), max_length=250)
    more3 = models.CharField(_(u'更多3'), max_length=250)
    more4 = models.CharField(_(u'更多4'), max_length=250)
    more5 = models.CharField(_(u'更多5'), max_length=250)
    more6 = models.CharField(_(u'更多6'), max_length=250)
    more7 = models.CharField(_(u'更多7'), max_length=250)
    more8 = models.CharField(_(u'更多8'), max_length=250)
    more9 = models.CharField(_(u'更多9'), max_length=250)
    more10 = models.CharField(_(u'更多10'), max_length=250)
    memberdate = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _(u'Member')
        verbose_name_plural = _(u'Member')
        ordering = ['-memberdate']


class MemberWallet(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(_(u'用户'), max_length=250)
    number = models.CharField(_(u'卡号'), max_length=250)
    expdate = models.CharField(_(u'到期'), max_length=250)
    firstnm = models.CharField(_(u'首姓'), max_length=1000)
    midnm = models.CharField(_(u'中名'), max_length=250)
    lastnm = models.CharField(_(u'尾名'), max_length=250)
    code = models.CharField(_(u'验码'), max_length=250)
    coin = models.CharField(_(u'主币'), max_length=250)
    coinA = models.CharField(_(u'币A'), max_length=250)
    coinB = models.CharField(_(u'币B'), max_length=250)
    coinC = models.CharField(_(u'币C'), max_length=250)
    wallet = models.CharField(_(u'钱包'), max_length=250)
    ustoken = models.CharField(_(u'唯码'), max_length=250)
    more1 = models.CharField(_(u'更多1'), max_length=250)
    more2 = models.CharField(_(u'更多2'), max_length=250)
    more3 = models.CharField(_(u'更多3'), max_length=250)
    more4 = models.CharField(_(u'更多4'), max_length=250)
    more5 = models.CharField(_(u'更多5'), max_length=250)
    more6 = models.CharField(_(u'更多6'), max_length=250)
    more7 = models.CharField(_(u'更多7'), max_length=250)
    more8 = models.CharField(_(u'更多8'), max_length=250)
    more9 = models.CharField(_(u'更多9'), max_length=250)
    more10 = models.CharField(_(u'更多10'), max_length=250)
    walletdate = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _(u'MemberWalletinfo')
        verbose_name_plural = _(u'MemberWalletinfo')
        ordering = ['-walletdate']


class Subscription(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(_(u'标题'), max_length=250)
    type = models.CharField(_(u'类型'), max_length=250)
    icon = models.CharField(_(u'图标'), max_length=250)
    url = models.CharField(_(u'链接'), max_length=250)
    detail = models.CharField(_(u'详情'), max_length=250)
    price = models.CharField(_(u'价格'), max_length=250)
    limit1 = models.CharField(_(u'限制1'), max_length=250)
    limit2 = models.CharField(_(u'限制2'), max_length=250)
    limit3 = models.CharField(_(u'限制3'), max_length=250)
    limit4 = models.CharField(_(u'限制4'), max_length=250)
    limit5 = models.CharField(_(u'限制5'), max_length=250)
    limit6 = models.CharField(_(u'限制6'), max_length=250)
    duration = models.CharField(_(u'周期'), max_length=250)
    more1 = models.CharField(_(u'更多1'), max_length=250)
    more2 = models.CharField(_(u'更多2'), max_length=250)
    more3 = models.CharField(_(u'更多3'), max_length=250)
    more4 = models.CharField(_(u'更多4'), max_length=250)
    more5 = models.CharField(_(u'更多5'), max_length=250)
    more6 = models.CharField(_(u'更多6'), max_length=250)
    more7 = models.CharField(_(u'更多7'), max_length=250)
    more8 = models.CharField(_(u'更多8'), max_length=250)
    more9 = models.CharField(_(u'更多9'), max_length=250)
    more10 = models.CharField(_(u'更多10'), max_length=250)
    subsdate = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _(u'Subscriptioninfo')
        verbose_name_plural = _(u'Subscriptioninfo')
        ordering = ['-subsdate']


class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(_(u'标题'), max_length=250)
    type = models.CharField(_(u'类型'), max_length=250)
    allow = models.CharField(_(u'允许'), max_length=250)
    icon = models.CharField(_(u'图标'), max_length=250)
    url = models.CharField(_(u'链接'), max_length=250)
    content = models.CharField(_(u'内容'), max_length=250)
    more1 = models.CharField(_(u'更多1'), max_length=250)
    more2 = models.CharField(_(u'更多2'), max_length=250)
    more3 = models.CharField(_(u'更多3'), max_length=250)
    more4 = models.CharField(_(u'更多4'), max_length=250)
    more5 = models.CharField(_(u'更多5'), max_length=250)
    more6 = models.CharField(_(u'更多6'), max_length=250)
    more7 = models.CharField(_(u'更多7'), max_length=250)
    more8 = models.CharField(_(u'更多8'), max_length=250)
    more9 = models.CharField(_(u'更多9'), max_length=250)
    more10 = models.CharField(_(u'更多10'), max_length=250)
    notificationdate = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _(u'Notificationinfo')
        verbose_name_plural = _(u'Notificationinfo')
        ordering = ['-notificationdate']


class Payinfo(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(_(u'用户'), max_length=250)
    cardnum = models.CharField(_(u'信用卡'), max_length=250)
    expmonth = models.CharField(_(u'到期月'), max_length=250)
    expyear = models.CharField(_(u'到期年'), max_length=250)
    secucode = models.CharField(_(u'三位码'), max_length=250)
    paycode = models.CharField(_(u'网付码'), max_length=250)
    paypal = models.CharField(_(u'Paypal'), max_length=250)
    strip = models.CharField(_(u'Strip'), max_length=250)
    pay1 = models.CharField(_(u'支付1'), max_length=250)
    pay2 = models.CharField(_(u'支付2'), max_length=250)
    pay3 = models.CharField(_(u'支付3'), max_length=250)
    pay4 = models.CharField(_(u'支付4'), max_length=250)
    pay5 = models.CharField(_(u'支付5'), max_length=250)
    pay6 = models.CharField(_(u'支付6'), max_length=250)
    pay7 = models.CharField(_(u'支付7'), max_length=250)
    pay8 = models.CharField(_(u'支付8'), max_length=250)
    more1 = models.CharField(_(u'更多1'), max_length=250)
    more2 = models.CharField(_(u'更多2'), max_length=250)
    more3 = models.CharField(_(u'更多3'), max_length=250)
    more4 = models.CharField(_(u'更多4'), max_length=250)
    more5 = models.CharField(_(u'更多5'), max_length=250)
    more6 = models.CharField(_(u'更多6'), max_length=250)
    more7 = models.CharField(_(u'更多7'), max_length=250)
    more8 = models.CharField(_(u'更多8'), max_length=250)
    more9 = models.CharField(_(u'更多9'), max_length=250)
    more10 = models.CharField(_(u'更多10'), max_length=250)
    paymentdate = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _(u'Payment')
        verbose_name_plural = _(u'Payment')
        ordering = ['-paymentdate']


class Messagebox(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(_(u'用户ID'), max_length=250)
    type = models.CharField(_(u'评论类型'), max_length=250)
    touserid = models.CharField(_(u'评给用户'), max_length=250)
    tosongid = models.CharField(_(u'评给歌曲'), max_length=250)
    content = models.CharField(_(u'评论内容'), max_length=250)
    favor = models.CharField(_(u'收藏用户'), max_length=250)
    status = models.CharField(_(u'评论状态'), max_length=250)
    more1 = models.CharField(_(u'更多1'), max_length=250)
    more2 = models.CharField(_(u'更多2'), max_length=250)
    more3 = models.CharField(_(u'更多3'), max_length=250)
    more4 = models.CharField(_(u'更多4'), max_length=250)
    more5 = models.CharField(_(u'更多5'), max_length=250)
    more6 = models.CharField(_(u'更多6'), max_length=250)
    more7 = models.CharField(_(u'更多7'), max_length=250)
    more8 = models.CharField(_(u'更多8'), max_length=250)
    more9 = models.CharField(_(u'更多9'), max_length=250)
    more10 = models.CharField(_(u'更多10'), max_length=250)
    messageboxdate = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _(u'Messageboxinfo')
        verbose_name_plural = _(u'Messageboxinfo')
        ordering = ['-messageboxdate']


# 道具信息 ----------------------------------------------------------------------------------
class Cards(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(_(u'卡片归属'), max_length=250)
    type = models.CharField(_(u'卡片类型'), max_length=250)
    cdtoken = models.CharField(_(u'卡片唯码'), max_length=250)
    level = models.CharField(_(u'卡片等级'), max_length=250)
    rare = models.CharField(_(u'稀有指数'), max_length=250)
    honor = models.CharField(_(u'卡片荣誉'), max_length=250)
    intro = models.CharField(_(u'卡片介绍'), max_length=250)
    title = models.CharField(_(u'卡片标题'), max_length=250)
    image = models.CharField(_(u'卡片图标'), max_length=250)
    icon = models.CharField(_(u'卡片微图'), max_length=250)
    materail = models.CharField(_(u'卡片材料'), max_length=250)
    grade1 = models.CharField(_(u'卡参数1'), max_length=250)
    grade2 = models.CharField(_(u'卡参数2'), max_length=250)
    grade3 = models.CharField(_(u'卡参数3'), max_length=250)
    create = models.CharField(_(u'创建日期'), max_length=250)
    outdate = models.CharField(_(u'回归日期'), max_length=250)
    saleif = models.CharField(_(u'售卖状况'), max_length=250)
    value = models.CharField(_(u'卡片指数'), max_length=250)
    price = models.CharField(_(u'卡片价值'), max_length=250)
    group = models.CharField(_(u'卡片套组'), max_length=250)
    note = models.CharField(_(u'备注信息'), max_length=250)
    more1 = models.CharField(_(u'更多1'), max_length=250)
    more2 = models.CharField(_(u'更多2'), max_length=250)
    more3 = models.CharField(_(u'更多3'), max_length=250)
    more4 = models.CharField(_(u'更多4'), max_length=250)
    more5 = models.CharField(_(u'更多5'), max_length=250)
    more6 = models.CharField(_(u'更多6'), max_length=250)
    more7 = models.CharField(_(u'更多7'), max_length=250)
    more8 = models.CharField(_(u'更多8'), max_length=250)
    more9 = models.CharField(_(u'更多9'), max_length=250)
    more10 = models.CharField(_(u'更多10'), max_length=250)
    carddate = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _(u'Card')
        verbose_name_plural = _(u'Card')
        ordering = ['-carddate', 'value', 'price']
