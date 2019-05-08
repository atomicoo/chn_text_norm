# -*- coding: utf-8 -*-
"""
TEXT类
"""

__author__ = 'Zhiyang Zhou <zyzhou@stu.xmu.edu.cn>'
__data__ = '2019-05-03'

import re

from chn_text_norm.cardinal import Cardinal
from chn_text_norm.digit import Digit
from chn_text_norm.telephone import TelePhone
from chn_text_norm.fraction import Fraction
from chn_text_norm.date import Date
from chn_text_norm.money import Money
from chn_text_norm.percentage import Percentage

CURRENCY_NAMES = '(人民币|美元|日元|英镑|欧元|马克|法郎|加拿大元|澳元|港币|先令|芬兰马克|爱尔兰镑|' \
                 '里拉|荷兰盾|埃斯库多|比塞塔|印尼盾|林吉特|新西兰元|比索|卢布|新加坡元|韩元|泰铢)'
CURRENCY_UNITS = '((亿|千万|百万|万|千|百)|(亿|千万|百万|万|千|百|)元|(亿|千万|百万|万|千|百|)块|角|毛|分)'


class Text:
    """
    Text类
    """

    def __init__(self, raw_text, norm_text=None):
        self.raw_text = raw_text
        self.norm_text = norm_text

    def _particular(self):
        text = self.norm_text
        pattern = re.compile(r"(([a-zA-Z]+)二([a-zA-Z]*))")
        matchers = pattern.findall(text)
        if matchers:
            # print('particular')
            for matcher in matchers:
                text = text.replace(matcher[0], matcher[1]+'2'+matcher[2])
        self.norm_text = text
        return self.norm_text

    def normalize(self):
        text = self.raw_text

        # 规范化日期
        pattern = re.compile(r"((\d{1,4}年)(\d{1,2}月(\d{1,2}[日号])?)?)")
        matchers = pattern.findall(text)
        if matchers:
            # print('date')
            for matcher in matchers:
                text = text.replace(matcher[0], Date(date=matcher[0]).date2chntext())

        # 规范化金钱
        pattern = re.compile(r'((\d+(\.\d+)?)' + CURRENCY_UNITS + '(\d' + CURRENCY_UNITS + '?)?)')
        matchers = pattern.findall(text)
        if matchers:
            # print('money')
            for matcher in matchers:
                text = text.replace(matcher[0], Money(money=matcher[0]).money2chntext())

        # 规范化固话/手机号码
        # 手机
        # http://www.jihaoba.com/news/show/13680
        # 移动：139、138、137、136、135、134、159、158、157、150、151、152、188、187、182、183、184、178、198
        # 联通：130、131、132、156、155、186、185、176
        # 电信：133、153、189、180、181、177
        pattern = re.compile(r"((\+?86 ?)?1([38]\d|5[0-35-9]|7[678]|9[89])\d{8})")
        matchers = pattern.findall(text)
        if matchers:
            # print('telephone')
            for matcher in matchers:
                text = text.replace(matcher[0], TelePhone(telephone=matcher[0]).telephone2chntext())
        # 固话
        pattern = re.compile(r"((0(10|2[1-3]|[3-9]\d{2})-?)?[1-9]\d{6,7})")
        matchers = pattern.findall(text)
        if matchers:
            # print('fixed telephone')
            for matcher in matchers:
                text = text.replace(matcher[0], TelePhone(telephone=matcher[0]).telephone2chntext(fixed=True))

        # 规范化分数
        pattern = re.compile(r"(\d+/\d+)")
        matchers = pattern.findall(text)
        if matchers:
            # print('fraction')
            for matcher in matchers:
                text = text.replace(matcher, Fraction(fraction=matcher).fraction2chntext())

        # 规范化百分数
        pattern = re.compile(r"(\d+(\.\d+)?%)")
        matchers = pattern.findall(text)
        if matchers:
            # print('percentage')
            for matcher in matchers:
                text = text.replace(matcher[0], Percentage(percentage=matcher[0]).percentage2chntext())

        # 规范化数字编号
        pattern = re.compile(r"(\d{11,32})")
        matchers = pattern.findall(text)
        if matchers:
            # print('digit')
            for matcher in matchers:
                text = text.replace(matcher, Digit(digit=matcher).digit2chntext())

        # 规范化纯数
        pattern = re.compile(r"(\d+(\.\d+)?)")
        matchers = pattern.findall(text)
        if matchers:
            # print('cardinal')
            for matcher in matchers:
                text = text.replace(matcher[0], Cardinal(cardinal=matcher[0]).cardinal2chntext())

        self.norm_text = text
        self._particular()

        return self.norm_text


if __name__ == '__main__':

    # 测试程序
    print(Text(raw_text='固话：0595-23865596或23880880').normalize())
    print(Text(raw_text='手机：+86 19859213959。').normalize())
    print(Text(raw_text='分数：32477/76391。').normalize())
    print(Text(raw_text='百分数：80%。').normalize())
    print(Text(raw_text='编号：31520181154418。').normalize())
    print(Text(raw_text='纯数：2983.07或12345.60。').normalize())
    print(Text(raw_text='日期：1999年2月20日或09年3月15号。').normalize())
    print(Text(raw_text='金钱：12块5，34.5元，20.1万').normalize())
    print(Text(raw_text='特殊：O2O或B2C。').normalize())

