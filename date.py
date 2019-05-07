import re
from chn_text_norm.basic_util import *
from chn_text_norm.cardinal import Cardinal


def date2chn(date_text):
    pattern = re.compile(r'\d{4}年')
    matcher = re.search(pattern, date_text)
    if matcher:
        result = ''
        st, ed = matcher.span()
        for i in date_text[st: ed-1]:
            result += CHINESE_DIGIS[int(i)]
        date_text = date_text[:st] + result + date_text[ed - 1:]

    pattern = re.compile(r'([09])\d年')
    matcher = re.search(pattern, date_text)
    if matcher:
        result = ''
        st, ed = matcher.span()
        for i in date_text[st: ed - 1]:
            result += CHINESE_DIGIS[int(i)]
        date_text = date_text[:st] + result + date_text[ed - 1:]

    pattern = re.compile(r'\d{1,2}月\d{0,2}')
    pattern_m = re.compile(r'\d{1,2}月')
    matcher = re.search(pattern, date_text)
    matcher_m = re.search(pattern_m, date_text)
    if matcher:
        st, ed = matcher.span()
        st_m, ed_m = matcher_m.span()
        # month
        result_m = Cardinal(cardinal=date_text[st_m:ed_m-1]).cardinal2chntext()
        # day
        result_d = ''
        if ed > ed_m:
            result_d = Cardinal(cardinal=date_text[ed_m:ed]).cardinal2chntext()
        if date_text[ed] not in ['日', '号']:
            date_text = date_text[:st_m] + result_m + '月' + result_d + '号' + date_text[ed:]
        else:
            date_text = date_text[:st_m] + result_m + '月' + result_d + date_text[ed:]
    return date_text


if __name__ == '__main__':
    # 测试程序
    print(date2chn(date_text='今天是9012年12月15日。'))
    print(date2chn(date_text='那是09年的春天。'))
