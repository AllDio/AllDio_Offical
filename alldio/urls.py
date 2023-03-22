from django.contrib import admin
from django.urls import path
from metasite.views import *

handler404 = error404

urlpatterns = [
    path('reload_page/', reload_page, name='reload_page'),
    path('songmint_status/', songmint_status, name='songmint_status'),
    path('buy_coins/', buy_coins, name='buy_coins'),
    path('wallet_connect/', wallet_connect, name='wallet_connect'),
    path('dapps_return/', dapps_return, name='dapps_return'),
    path('web3_dapps/', web3_dapps, name='web3_dapps'),
    path('paypal_payment/', paypal_payment, name='paypal_payment'),
    path('paypal_execute/', paypal_execute, name='paypal_execute'),
    path('paypal_backurl/', paypal_backurl, name='paypal_backurl'),
    # -------------------------------------
    path('pay_royalty/', pay_royalty, name='pay_royalty'),
    path('cancel_subscription/', cancel_subscription, name='cancel_subscription'),
    path('become_contributor/', become_contributor, name='become_contributor'),
    path('change_subscription/', change_subscription, name='change_subscription'),
    path('get_luckycard/', get_luckycard, name='get_luckycard'),
    path('get_generatesong/', get_generatesong, name='get_generatesong'),
    path('save_payinfo/', save_payinfo, name='save_payinfo'),
    path('stored_song/', stored_song, name='stored_song'),
    path('send_suggestion/', send_suggestion, name='send_suggestion'),
    path('edit_usrprofile/', edit_usrprofile, name='edit_usrprofile'),
    path('mint_song/', mint_song, name='mint_song'),
    path('sell_card/', sell_card, name='sell_card'),

    # ------------------------------------------
    path('', universe),
    path('admin/', admin.site.urls),
    path('signup/', signup, name='signup'),
    path('universe/', universe, name='universe'),
    path('error404/', error404, name='erro404'),
    path('usrpanel/', usrpanel, name='usrpanel'),
    # ------------------------------------------
    path('invitecode/', invitecode, name='invitecode'),
    path('create_user/', create_user, name='create_user'),
    path('email_check/', email_check, name='email_check'),
    path('email_codecheck/', email_codecheck, name='email_codecheck'),
    path('pswrd_reset/', pswrd_reset, name='pswrd_reset'),
    path('login_check/', login_check, name='login_check'),
    path('signout/', signout, name='signout'),
]
