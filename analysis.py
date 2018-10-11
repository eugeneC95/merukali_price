#!/usr/bin/env python
# coding: utf8
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import pymysql
import time
#Get all info from link;

options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images":2}

options.add_experimental_option("prefs",prefs)
options.add_argument("--window-size=300,300")#--start-maximized
driver = webdriver.Chrome("S:/Career/merukali_price/chromedriver.exe",options=options)
#https://www.mercari.com/jp/brand/1620/
keyword = ''
db = pymysql.connect(host='206.189.90.203',user='zun95',passwd='Hotdilvin95',db='merucali')
cursor = db.cursor()
def insert(hre,tit,lik,sto,pri,tim):
    try:
        cursor.execute("INSERT into post (href,title,likes,stock,price,time_update) VALUES(%s, %s, %s, %s, %s, %s)",(hre,tit,lik,sto,pri,tim))
        db.commit()
    except:
        print("error")
        db.rollback()
def gethref(x):
    try:
        cursor.execute("SELECT * FROM post WHERE href LIKE %s",(x))
        datas = cursor.fetchall()
        if datas != ():
            for data in datas:
                price = data[5]
            return "true",price
        elif datas == ():
            return "false","0"
    except:
        print ("Error: unable to fetch data")
def updatetime(tim,hre,pri):
    try:
        cursor.execute("UPDATE post SET time_update =%s WHERE href = %s && price =%s",(tim,hre,pri))
        db.commit()
    except:
        print ("Error: unable to fetch data")
def research(j):
    link = "https://www.mercari.com/jp/search/?page="+str(j)+"&keyword=supreme"
    driver.get(link);
    #get all link
    time.sleep(1)
    box = driver.find_elements_by_tag_name('section')
    for i in range(1,len(box)):
        try:
            titles = driver.find_element_by_xpath("//div[@class='items-box-content clearfix']//section["+str(i)+"]//figure[@class='items-box-photo']//img[1]").get_attribute("alt")
            hrefs = driver.find_element_by_xpath("//div[@class='items-box-content clearfix']//section["+str(i)+"]//a[1]").get_attribute("href")
            prices = driver.find_element_by_xpath("//div[@class='items-box-content clearfix']//section["+str(i)+"]//div[@class='items-box-price font-5']").text
            prices = prices.replace("¥ ","")
            prices = prices.replace(",","")
            likess = driver.find_element_by_xpath("//div[@class='items-box-content clearfix']//section["+str(i)+"]//span").text
            eptime = time.process_time()
        except NoSuchElementException:
            likess = "0"
        try:
            stock = driver.find_element_by_xpath("//div[@class='items-box-content clearfix']//section["+str(i)+"]//figcaption//div[1]//div[1]").text
        except NoSuchElementException:
            stock = "YES"
        time_updates = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(hrefs)
        status = gethref(hrefs)[0]
        price = str(gethref(hrefs)[1])
        print(status)
        if status == "true":
            if price == prices:
                #update time
                updatetime(time_updates,hrefs,price)
                print("time updated\n")
            else:
                #insert post with new price
                insert(hrefs,titles,likess,stock,prices,time_updates)
                print("New Uploaded\n")
        else:
            insert(hrefs,titles,likess,stock,prices,time_updates)
            print("Uploaded\n")
    driver.refresh()
    time.sleep(1)
    print("lopped\n")
    if j >= 15:
        j=1
    else:
        j += 1
    research(j)
research(1)
db.close()
# driver.quit()
# quit()
