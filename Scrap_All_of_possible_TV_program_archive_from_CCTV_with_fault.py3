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
2018-07-30：由于2016年8月22日，央视网对网页结构进行了调整，我们决定将搜索时间起点挪至2016年8月22日。
	网页结构调整前后对比
		调整前
		<ul>
	<li><a href="http://tv.cctv.com/2016/08/05/VIDEvw4RyzMQS6NGuA4SKt2x160805.shtml" target="_blank">
《新闻联播》 20160805 21:00
</a></li>
</ul>
		调整后
		<ul>
	<li>
		<a href="http://tv.cctv.com/2016/08/23/VIDEcwEt6Sw0iDnv3XhTSvRC160823.shtml" target="_blank">
			<div class="imgbox" style="display:none;"> <img src="http://p4.img.cctvpic.com/fmspic/2016/08/23/34a1b814d32c43b5a0192525fe76c3f8-19.jpg"><i class="player"></i> </div>
			<div class="text">
				<div class="title">《新闻联播》 20160823 19:00</div>
				<div class="bottom" style="display:none;">00:29:55</div>
			</div>
		</a>
		<div style="clear:both"></div>
	</li>
</ul>
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
end = datetime.date(2016, 8, 23).today()

'''
获取节目日期（仅适用于新闻联播）
功能描述：
'''


class Xwlb():
    """专门用于处理新闻联播的类"""
    '''
新闻联播的处理函数
处理步骤：新闻联播的处理分为两步：第一步是从返回的网页中提取链接，并且尝试从文本中筛选出时间，不行就执行第二步；
第二步是从链接获取的网页中提取时间。如果是19:00，则认为没有问题；如果只有21:00，则认为出现失误，其他则为异常，记录下来分析原因。
新闻联播由于对存在口误的节目直接重制，很可能不存在重播（偶尔有漏网之鱼存在两期19:00和21:00），决定分三种情况处理：1.存在一种分析发布时间，如果为21:00左右发布则为不可考证，19:00发布则认为没有问题；2.如果两个都有，则记录下来，方便后期查阅。
'''

    def __init__(self):
        __xwlbProgramAddress = 'http://tv.cctv.com/lm/xwlb/day/{}.shtml'
        __programNameRegex = "\u65b0\u95fb\u8054\u64ad"

    def getProgramDateForXwlb(self, scrapAddressFormat, programNameRegex):
            # 遍历从上面描述的时间点开始，到昨天结束
        searchDoubleResult = set()
        globalRegex = "\d{8}"
        for i in range((end - begin).days):
            day = begin + datetime.timedelta(days=i)
            dayStr = day.strftime('%Y%m%d')
            scrapAddress = scrapAddressFormat.format(dayStr)
            response = requests.get(scrapAddress, headers=header)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            soupRes = soup.find_all(text=re.compile(globalRegex))
            # 如果找出存在两项的，放到集合里
            searchDoubleResult.add(soupRes)
            # 如果没找到相应的元素，就跳过
            if len(soupRes) == 0:
                continue
            print(soupRes)

    def xwlbProc(self):
            # 新闻联播节目地址格式（括号里为节目日期）
        getProgramDateForXwlb(__xwlbProgramAddress, __programNameRegex)


'''
新闻直播间：
'''
'''
主函数
'''


def main():
    xwlbObj = Xwlb()
    xwlbObj.xwlbProc()


'''
执行主函数
'''

main()
