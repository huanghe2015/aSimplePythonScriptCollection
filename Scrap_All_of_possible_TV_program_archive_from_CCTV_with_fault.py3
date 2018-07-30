#!/usr/bin/python3
'''
作者：Ak88
日期：2018-07-30
类别：爬虫类
功能描述：本脚本的作用是爬取所有央视主持人存在口误的节目及其日期列表，为后续口误集锦素材的搜集准备资料。
判断依据：一般在出现口误后，对于不重要的节目（如共同关注），央视会将节目录像从节目的日历中删除，但通过近期正常的节目录像的网页仍然可以访问存在失误的节目录像；对于重要的节目（目前只发现新闻联播，如果有谁发现了同等重要的节目，欢迎更新），则进行重制，放出来的节目录像则为重播。
本脚本的作用就是通过以上的逻辑分析将那些可能存在失误的节目时间挖出来。
备注：鉴于央视网改版，为了方便起见，我们的搜索的节目时间段控制在2016年7月3日至今（新闻联播为2016年2月3日至今，暂时不设置）。
'''
'''
更新日志
'''
import requests
import datetime
import re
from bs4 import BeautifulSoup
'''
初始化设置
'''
# HTTP头，伪装浏览器
header = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:36.0) Gecko/20100101 Firefox/36.0'}

'''
划定时间范围
'''
begin = datetime.date(2016, 7, 3)
end = datetime.date(2017, 9, 20).today()

'''
处理公用函数
'''


def getProgramText(scrapAddressFormat):
        # 遍历从上面描述的时间点开始，到昨天结束
    for i in range((end - begin).days):
        day = begin + datetime.timedelta(days=i)
        dayStr = day.strftime('%Y%m%d')
        scrapAddress = scrapAddressFormat.format(dayStr)
        response = requests.get(scrapAddress)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        soupRes = soup.find_all(text=re.compile("\u65b0\u95fb\u8054\u64ad"))
        # 如果没找到相应的元素，就跳过
        if len(soupRes) == 0:
            continue
        print(soupRes)


'''
新闻联播的处理函数
处理步骤：新闻联播的处理分为两步：第一步是从返回的网页中提取链接，并且尝试从文本中筛选出时间，不行就执行第二步；
第二步是从链接获取的网页中提取时间。如果是19:00，则认为没有问题；如果是21:00，则认为出现失误，其他则为异常，记录下来分析原因。
'''


def xwlb():
    # 新闻联播节目地址格式（括号里为节目日期）
    xwlbProgramAddress = 'http://tv.cctv.com/lm/xwlb/day/{}.shtml'
    getProgramText(xwlbProgramAddress)


'''
判断时间是否为异常（目前仅供新闻联播使用）
'''
'''
主函数
'''


def main():
    xwlb()


'''
执行主函数
'''

main()
