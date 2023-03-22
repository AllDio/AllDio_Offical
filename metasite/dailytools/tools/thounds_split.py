def thousands_split(digi):
    '''
     - 千位分隔
    '''
    # 字符串化 
    digi = str(digi)

    # 小数点与整数区分
    if '.' in digi:
        int_digi   = digi.split('.')[0]
        float_digi = '.' + digi.split('.')[1]
    else:
        int_digi   = digi
        float_digi = ''

    # 反转数字
    reverse_digi     = int_digi[::-1]

    # 千位分隔
    new_reverse_digi = ''
    for i in range(len(str(reverse_digi))):
        if i>0 and i%2 == 0 and i<len(reverse_digi)-1:
            new_reverse_digi += reverse_digi[i] + ','
        else:
            new_reverse_digi += reverse_digi[i]

    # 数字归位
    new_digi = new_reverse_digi[::-1] + float_digi

    return new_digi