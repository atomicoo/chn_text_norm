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
from chn_text_norm.date import date2chn
from chn_text_norm.money import money2chn


class Text:
    """
    Text类
    """

    def __init__(self, raw_text, norm_text=None):
        self.raw_text = raw_text
        self.norm_text = norm_text

    def normalize(self):
        text = self.raw_text

        # 规范化日期
        text = date2chn(text)

        # 规范化金钱
        text = money2chn(text)

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
            # m0 = matcher[0][0]
            # m1 = TelePhone(telephone=matcher[0][1]).telephone2chntext()
            # m2 = matcher[0][-1]
            # text = ''.join([m0, m1, m2])
        # 固话
        pattern = re.compile(r"((0(10|2[1-3]|[3-9]\d{2})-?)?[1-9]\d{6,7})")
        matchers = pattern.findall(text)
        if matchers:
            # print('fixed telephone')
            for matcher in matchers:
                text = text.replace(matcher[0], TelePhone(telephone=matcher[0]).telephone2chntext(fixed=True))
                # m0 = matcher[0][0]
                # m1 = TelePhone(telephone=matcher[0][1]).telephone2chntext(fixed=True)
                # m2 = matcher[0][-1]
                # text = ''.join([m0, m1, m2])

        # 规范化分数
        pattern = re.compile(r"(\d+/\d+)")
        matchers = pattern.findall(text)
        if matchers:
            # print('fraction')
            for matcher in matchers:
                text = text.replace(matcher, Fraction(fraction=matcher).fraction2chntext())
            # m0 = matcher[0][0]
            # m1 = Fraction(fraction=matcher[0][1]).fraction2chntext()
            # m2 = matcher[0][-1]
            # text = ''.join([m0, m1, m2])

        # 规范化数字编号
        pattern = re.compile(r"(\d{11,32})")
        matchers = pattern.findall(text)
        if matchers:
            # print('digit')
            for matcher in matchers:
                text = text.replace(matcher, Digit(digit=matcher).digit2chntext())
            # m0 = matcher[0][0]
            # m1 = Digit(digit=matcher[0][1]).digit2chntext()
            # m2 = matcher[0][-1]
            # text = ''.join([m0, m1, m2])

        # 规范化纯数
        pattern = re.compile(r"(\d+\.?\d*)")
        matchers = pattern.findall(text)
        if matchers:
            # print('cardinal')
            for matcher in matchers:
                text = text.replace(matcher, Cardinal(cardinal=matcher).cardinal2chntext())
            # m0 = matcher[0][0]
            # m1 = Cardinal(cardinal=matcher[0][1]).cardinal2chntext()
            # m2 = matcher[0][-1]
            # text = ''.join([m0, m1, m2])

        return text


if __name__ == '__main__':

    # 测试程序
    print(Text(raw_text='固话：0595-23865596或0595-23880880').normalize())
    print(Text(raw_text='手机：+86 19859213959。').normalize())
    print(Text(raw_text='分数：32477/76391。').normalize())
    print(Text(raw_text='编号：31520181154418。').normalize())
    print(Text(raw_text='纯数：2983.07和12345.67890。').normalize())
    print(Text(raw_text='日期：今天是9012年12月15日,天气很好').normalize())
    print(Text(raw_text='金钱：小花有20000澳元，小明借了50.5元花了30.5剩下20块,非常的高兴,那就给小花12块5吧,那我就剩下17块5，小明还欠34.5，小草欠小花20.1万').normalize())
