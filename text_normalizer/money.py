import re
from text_normalizer.basic_util import *


currency_name = r'(人民币|美元|日元|英镑|欧元|马克|法郎|加拿大元|澳元|港币|先令|芬兰马克|爱尔兰镑|' \
                r'里拉|荷兰盾|埃斯库多|比塞塔|印尼盾|林吉特|新西兰元|比索|卢布|新加坡元|韩元|泰铢)'
currency_sla = r'(亿|千万|百万|万|千|百|元|块|角|毛|分)'
currency_sla2 = r'((花(了)?)|(用(了)?)|(借(了)?)|(还(了)?)|(欠(了)?)|还款|借款)'


def money2chn(money_text):

    pattern = re.compile(r'(\d+\.*\d*)' + currency_sla + r'(\d*\.*\d*)')
    while True:
        matcher = re.search(pattern, money_text)
        if matcher:
            st, ed = matcher.span()
            pattern_j = re.compile(currency_sla)
            matcher_j = re.search(pattern_j, money_text[st:ed] )
            st_j, ed_j = matcher_j.span()
            st_j += st
            ed_j += st
            if ed_j < ed:
                money_text = money_text[:st] + num2chn(money_text[st:st_j]) + money_text[st_j:ed_j] + num2chn(money_text[ed_j:ed]) + money_text[ed:]
            else:
                money_text = money_text[:st] + num2chn(money_text[st:st_j]) + money_text[st_j:]
        else:
            break

    pattern = re.compile(currency_sla2 + r'(\d+\.?\d*)')
    while True:
        matcher = re.search(pattern, money_text)
        if matcher:
            st, ed = matcher.span()
            pattern_j = re.compile(currency_sla2)
            matcher_j = re.search(pattern_j, money_text[st:ed])
            st_j, ed_j = matcher_j.span()
            st_j += st
            ed_j += st
            money_text = money_text[:ed_j] + num2chn(money_text[ed_j:ed]).replace('点','块') + money_text[ed:]
        else:
            break

    pattern = re.compile(r'(\d+\.*\d*)' + currency_name)
    while True:
        matcher = re.search(pattern, money_text)
        if matcher:
            st, ed = matcher.span()
            pattern_j = re.compile(currency_name)
            matcher_j = re.search(pattern_j, money_text[st:ed])
            st_j, ed_j = matcher_j.span()
            st_j += st
            ed_j += st
            money_text = money_text[:st] + num2chn(money_text[st:st_j]) + money_text[st_j:]
        else:
            break
    return money_text


if __name__ == '__main__':
    # 测试程序
    print(money2chn(money_text='小花有20000.5澳元，小明借了50.5元花了30.5剩下20块,非常的高兴,那就给小花12块5吧,那我就剩下17块5，小明还欠34.5，小草欠小花20.1万'))