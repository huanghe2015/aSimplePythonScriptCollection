#!/usr/bin/python
'''
作者：Ak88
日期：2018-06-21
本脚本的功能是利用requests获取哔哩哔哩网站的某位UP主的所有视频，然后调用命令行的you-get模块下载视频
大致步骤：输入UP主的个人空间地址，例如https://space.bilibili.com/28152409/#/video?page=3（末尾为页面位置），脚本通过定位最后一页的数字来确定总页数，然后逐步翻页，获取每一页所有视频的具体地址
'''
'''
更新日志
2018-07-30：试图添加多线程支持
'''
import requests
import json
import os
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
    # 执行完成之后，自动关机（因为需要消耗的时间）
    os.system("shutdown /s")  # Windows使用，其他操作系统自行参考

# 检测页面总数


def getTotalPage(spaceID):
    getDataObject = getDataJSON(spaceID, 1)
    getPageNum = getDataObject['pages']
    return getPageNum
# 循环爬取页面范围内的所有地址


def realGet(spaceID, wantToGet):
    avURLArray = []
    downloadingIndex = 0
    for x in range(1, wantToGet):
        getDataObject = getDataJSON(spaceID, x)
        getVListObjectArray = getDataObject['vlist']
        # 怎么样在多线程中实现每个线程下载一个资源？
        for getVListObject in getVListObjectArray:
            avNum = getVListObject['aid']
            # 创建两个线程
            try:
                _thread.start_new_thread(download, ("Thread-1", avNum, ))
                downloadingIndex++
                _thread.start_new_thread(download, ("Thread-2", avNum, ))
                downloadingIndex++
            except:
                print("Error: 无法启动线程")

    return avURLArray

# 单独包装的下载函数


def download(avNum):
    avURL = avvideo.format(str(avNum))
    # 使用命令行调用you-get进行下载
    os.system("you-get -d -o . "+avURL)

# 获取页面JSON（包括av号和页面总数）


def getDataJSON(spaceID, locationNum):
    spaceURL = apt.format(spaceID, locationNum)
    response = requests.get(spaceURL)
    getResJSONstr = response.text
    getResJSON = json.loads(getResJSONstr)
    getDataObject = getResJSON['data']
    return getDataObject


main()
