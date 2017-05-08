# coding:utf-8
from selenium import webdriver
from bs4 import BeautifulSoup
import urllib
import re
import time
import os
import sys
import json


# driver = webdriver.PhantomJS()
driver = webdriver.Chrome()
AllChaptUrlAndName = []
allFirstImgUrl = []


def get_pic():
    url = "http://www.77mh.com/colist_183657.html"
    # 请求页面
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, "lxml")

    get_AllChaptUrls(soup)

    for item in AllChaptUrlAndName:

        # FirstImgUrlAndCount = []
        driver.get(item[0][0])

        img_id = driver.find_element_by_id("dracga")
        if img_id.is_displayed() is True:
            # driver.implicitly_wait(10)
            # img_id = driver.find_element_by_id("dracga")
            # print img_id.is_displayed()
            # while img_id.is_displayed() is False:
            #     print "刷新页面"
            #     driver.get(item[0][0])
            #     driver.implicitly_wait(10)
            #     img_id = driver.find_element_by_id("dracga")
            #     if img_id.is_displayed():
            #         break
            #     time.sleep(5)

            print("打开 " + item[0][1])
            # soupnew = BeautifulSoup(driver.page_source, "lxml")
            # page_tip = soupnew.find_all(class_="top page_tip")
            # allpagecount = get_AllPageCount(page_tip)

            # FirstImgUrlAndCount.append(item[0][1])
            # FirstImgUrlAndCount.append(allpagecount)
            # FirstImgUrlAndCount.append(item[0][0])
            # # FirstImgUrlAndCount内容:[第X话，总页数，地址]
            # allFirstImgUrl.append(FirstImgUrlAndCount)
            time.sleep(5)
            # save_img_url(allFirstImgUrl)

    driver.quit()


def save_allChaptUrls(chapturls):
    urlfile = 'manhua/AllChaptUrlAndName.json'
    with open(urlfile, 'w') as f:
        json.dump(chapturls, f, ensure_ascii=False)


def save_img_url(imgurl):
    urlfile = 'manhua/firstimgurl.json'
    with open(urlfile, 'w') as f:
        json.dump(imgurl, f, ensure_ascii=False)


def get_AllPageCount(page_tip):
    ''' 获取每一话的总页数'''
    pattern = re.compile('<strong>(\d*)</strong>')
    # print list.type()
    pagesnum = pattern.findall(str(page_tip))
    # 每一话的总页数
    allpage_count = pagesnum[1]
    print("共" + allpage_count + "页")
    return allpage_count


def get_AllChaptUrls(soup):
    ''' 获取每一话的 url 和名称 '''
    all = soup.find
    allurls = soup.find_all(
        target="_blank",
        href=re.compile("http://www.77mh.com/"),
        title=re.compile(u"请叫我英雄"))

    print("获取到每一话的地址")

    for url in allurls:
        urlAndNameItem = re.findall(r'href=\"(.*?)\".*?\>(.*?)\<', str(url))
        AllChaptUrlAndName.append(urlAndNameItem)
    save_allChaptUrls(AllChaptUrlAndName)
    print("保存每一话的地址")


# def save_pic(img_url, chapt_folder, img_num, page_count):
#     req = urllib.request.Request(img_url
#     req.add_header(
#         'User-Agent',
#         'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
#     )

#     req.add_header('GET', img_url)

#     try:
#         # print "save pic url: " + pic_url
#         resp = urllib.request.urlopen(req, timeout=20)
#         data = resp.read()
#         # print data.encode('utf-8')
#         # print data
#         img_savePath = chapt_folder + "/" + "%.5d.jpg" % img_num
#         fp = open(img_savePath, "wb")
#         fp.write(data)
#         fp.close
#         print("save pic finished.")
#     except Exception:
#         # print(e)
#         print("save pic: " + img_url + " failed.")


def save_img(img_savePath, img_num, page_count):
    ''' 下载每一页漫画 '''
    savenotice = img_savePath[6:-10] + ": " + str(img_num) + "/" + str(
        page_count) + "页"
    # 下载图片并命名
    try:
        pic_id = "dracga"
        img_url = driver.find_element_by_id(
            pic_id).get_attribute("src")    # 定位图片元素，并获取图片的地址
        print("开始下载第" + str(img_num) + "页...")
        urllib.request.urlretrieve(img_url, img_savePath)  # 下载图片
        imgsize = os.path.getsize(img_savePath) / 1024    # kb
        print("图片大小：%.0f kb" % (imgsize))  # 图片大小：262 kb
        print(savenotice + ",下载完成")  # 请叫我英雄/第4卷: 205/228页,下载完成
    except urllib.error.HTTPError as e:
        print(e.code)
        print(savenotice + ",下载失败")
        driver.save_screenshot(img_savePath)  # 若下载失败，则改为网页截图
        print("截图")


def save_chapt_img(chapt_home_url, chapt_folder, page_count):
    ''' 下载每一话漫画 '''
    driver.get(chapt_home_url)  # 问题1
    img_num = 1
    pic_id = "dracga"
    for i in range(page_count):  # 循环次数为总页数
        # img_savePath: manhua/请叫我英雄/第70话18页/00001.jpg
        img_savePath = chapt_folder + "/" + "%.5d.jpg" % img_num
        if os.path.exists(img_savePath):
            print("图片已存在")
        else:
            # TODO: 下载当前页图片
            save_img(img_savePath, img_num, page_count)
            driver.find_element_by_class_name("nextPage").click()  # 点击下一页
            next_page_url = driver.current_url
            time.sleep(5)
            driver.get(next_page_url)   # 打开下一页
        img_num += 1
        # 进入下一页
    print(chapt_folder + "下载完成")


def save_all_img():
    ''' 下载全部章节漫画 '''
    allurlfile = "firstimgurl.json"
    with open(allurlfile, 'r') as f:
        all_chapt_home_urls = json.load(f)
    title = all_chapt_home_urls
    comic_folder = "请叫我英雄"
    create_dir_path(comic_folder)
    for item in all_chapt_home_urls[30:]:
        chaptname = item[0]
        page_count = int(item[1])
        chapt_home_url = item[2]
        chapt_folder = comic_folder + "/" + chaptname + str(
            page_count) + "页"
        create_dir_path(chapt_folder)
        save_chapt_img(chapt_home_url, chapt_folder, page_count)

    print("全部漫画下载完成.")
    driver.quit()


def create_dir_path(path):
    # 以漫画名创建文件夹
    isexists = os.path.exists(path)
    if not isexists:
        print("创建文件夹")
        os.makedirs(path)
    else:
        print("文件夹已存在")


if __name__ == "__main__":
    # get_pic()
    save_all_img()
