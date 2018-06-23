#!/usr/bin/python
'''
作者：Ak88
日期：2018-06-21
本脚本的作用是利用BeautifulSoup的解析功能，实现解析哔哩哔哩网站的某位UP主的所有视频并生成文本文件的功能
大致步骤：输入UP主的个人空间地址，例如https://space.bilibili.com/28152409/#/video?page=3（末尾为页面位置），脚本通过定位最后一页的数字来确定总页数，然后逐步翻页，获取每一页所有视频的具体地址
'''
import requests
import json
# HTTP头，伪装浏览器
header = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:36.0) Gecko/20100101 Firefox/36.0'}
# 哔哩哔哩视频地址格式
avvideo = 'https://www.bilibili.com/video/av{}'
# 获取UP主所有视频的地址格式
apt = 'https://space.bilibili.com/ajax/member/getSubmitVideos?mid={}&pagesize=30&page={}'
# 默认文件名
fileName = "avVideoList.txt"
newFileName = fileName
# 输入测试UP主的地址，检测是否管用


def main():
    spaceID = input(
        "请输入UP主的个人空间ID（例如，https://space.bilibili.com/28152409（就是这个）/#/video）：")
    # 输入要获取的页面数
    getPageNum = getTotalPage(spaceID)
    wantToGetInfo = "总共有{}页，想获取多少页呢？"
    wantToGetInfoNow = wantToGetInfo.format(getPageNum)
    wantToGet = input(wantToGetInfoNow)
    avURLArray = realGet(spaceID, int(wantToGet))
    # 将结果输出并写入文件
    fileInfo = "请输入要保存的文件名（默认avVideoList.txt）："
    newFileName = input(fileInfo)
    if newFileName == "":
        newFileName = fileName
    print(avURLArray)


# 检测页面总数
def getTotalPage(spaceID):
    getDataObject = getDataJSON(spaceID, 1)
    getPageNum = getDataObject['pages']
    return getPageNum
# 循环爬取页面范围内的所有地址


def realGet(spaceID, wantToGet):
    avURLArray = []
    getFile = open(newFileName, "a+")
    for x in range(1, wantToGet):
        getDataObject = getDataJSON(spaceID, x)
        getVListObjectArray = getDataObject['vlist']
        for getVListObject in getVListObjectArray:
            avNum = getVListObject['aid']
            avURL = avvideo.format(str(avNum))
            getFile.write(avURL+"\n")
            avURLArray.append(avURL)
    getFile.close()
    return avURLArray


# 获取页面JSON（包括av号和页面总数）
def getDataJSON(spaceID, locationNum):
    spaceURL = apt.format(spaceID, locationNum)
    response = requests.get(spaceURL)
    getResJSONstr = response.text
    getResJSON = json.loads(getResJSONstr)
    getDataObject = getResJSON['data']
    return getDataObject


main()
