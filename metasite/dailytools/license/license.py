
def enlarge_fontdistance(text_word):
    enlarged_word = ''
    for word_i in range(len(text_word)):
        enlarged_word += text_word[word_i] + ''
    return enlarged_word


def draw_image(bocfldpath,buyer,idcard,song,author,proxy,link,code,usage,item,timenow,timelimit):
    import os.path
    from PIL import Image, ImageDraw, ImageFont
    from django.conf import settings
    width,height = 794,1123  # A4大小
    album_title  = "       音 乐 授 权 书"
    album_title  = enlarge_fontdistance(album_title)
    year         = timenow[0:4]
    month        = timenow[4:6]
    day          = timenow[6:8]
    lmt_year     = timelimit[0:4]
    lmt_month    = timelimit[4:6]
    lmt_day      = timelimit[6:8]

    location     = '全球'
    auth_time    = '随项目永久'
    limit        = f'{lmt_year} 年 {lmt_month} 月 {lmt_day} 日'
    atten        = '被授权的音乐作品不得以任何形式进行转授权或应用于非约定的项目属性'
                   # '                   音乐可随项目永久免费使用，\n\n'\

    line_1       = f'此证书证明您可以在以下约定中使用指定音乐作品，授权期限: {auth_time},'
    line_2       = f'您本次使用音乐作品的项目为《{item}》。'
    line_3       = f'被授权者:   {buyer}'
    line_4       = f'身份证号:   {idcard}'
    line_5       = f'音乐作品:  《{song}》'
    # line_6       = f'版权作者:   {author}'
    # line_7       = f'版权代理:   {proxy}'
    line_8       = f'授权代码:   {code}'
    # line_9       = f'作品链接:   {link}'
    line_11      = f'项目名称:   《{item}》'
    line_12      = f'项目属性:   {usage}'
    line_14      = f'发行地域:   {location}'
    line_10      = f'发表期限:   {limit} (被授权项目应不晚于该日期发表)'
    line_13      = f'授权申明:   {atten}'

    company      = '上海链声网络科技有限公司'
    timedate     = f'{year} 年 {month} 月 {day} 日'
                 
    line_list    = [line_1 ,line_2 ,line_3 ,line_4 ,line_5 ,line_8 , line_11 ,line_12,line_14,line_10 ,line_13]

    # 样式设置 (⚠️ 字体在服务器上需要预先安装)
    fontstyle   = ["Alibaba-PuHuiTi-Light.ttf" ,"Alibaba-PuHuiTi-Regular.ttf" ,"Alibaba-PuHuiTi-Medium.ttf"]
    # fontstyle = ["Alibaba-PuHuiTi-Light.otf", "Alibaba-PuHuiTi-Regular.ttf", "Alibaba-PuHuiTi-Medium.otf"]
    bg_color    = '#F5F5F5'                                                          # 背景色
    fontsize    = [32 ,17 ,17] +[15 for _ in range(len(line_list) - 2)] + [20, 18]   # 字体大小
    fontcolor   = ["#000000" for _ in range(len(fontsize))]                          # 字体颜色
    fontname    = [fontstyle[2], fontstyle[1], fontstyle[1]] + \
                  [fontstyle[0] for _ in range(len(line_list) - 2)] + \
                  [fontstyle[1], fontstyle[1]]                                       # 字体样式
    words       = [album_title] + line_list + [company, timedate]                    # 文字内容


    bocname     = f"{timenow}_{song}_音乐作品授权证明.png"
    bocpath     = os.path.join(bocfldpath, bocname)                                  # 图片路径
    # img       = Image.new("RGB", (width, height), bg_color)                        # 图片初始化
    bgimg_path  = 'MusicLab/dailytools/license/blank/signwhite.png'                # 背景图片
    img_path    = os.path.join(settings.BASE_DIR,bgimg_path)
    img = Image.open(img_path)

    for t in range(len(words)):
        # 文字内容
        word = words[t]

        # 样式应用
        font = ImageFont.truetype(fontname[t], fontsize[t])
        if t == 0:
            text_coordinate = (250, int(width / 2 - width / 2.5) + t)
        elif t == 1:
            text_coordinate = (140, int(width / 2 - width / 2.5) + t * 100 + 30)
        elif t == 2:
            text_coordinate = (105, int(width / 2 - width / 2.5) + t * 75 + 20)
        elif t < len(line_list) + 1:
            text_coordinate = (105, int(width / 2 - width / 2.5) + t * 47 + 120)
        elif t == len(line_list) + 1:
            text_coordinate = (430, int(width / 2 - width / 2.5) + t * 47 + 230)
        else:
            text_coordinate = (550, int(width / 2 - width / 2.5) + t * 47 + 240)
            
        # 合成图片
        img_draw = ImageDraw.Draw(img)
        img.save(bocpath, quality=1000)

        # 合成文字 (文字一层层覆盖图片)
        img_draw.text(text_coordinate, word, font=font, fill=fontcolor[t])
        img.save(bocpath, quality=1000)
    return bocpath




