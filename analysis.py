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
options.add_argument("--start-maximized")

driver = webdriver.Chrome("S:/Career/merukali_price/chromedriver.exe",options=options)
link = 'https://www.mercari.com/jp/search/?keyword=%E3%83%91%E3%83%B3%E3%82%B9%E3%83%88' #https://www.mercari.com/jp/brand/1620/
keyword = ''
def insert(hre,tit,lik,pri,tim):
    db = pymysql.connect('206.189.90.203','zun95','Hotdilvin95','merucali')
    try:
        with db.cursor() as cursor:
            sql = "INSERT into post (href,title,likes,price,time_update) VALUES(%s, %s, %s, %s, %s)"
            cursor.execute(sql,(hre,tit,lik,pri,tim))
            db.commit()
    except:
        print("error")
        db.rollback()
    db.close()
def gethref(x):
    db = pymysql.connect('206.189.90.203','zun95','Hotdilvin95','merucali')
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM post")
        datas = cursor.fetchall()
        for data in datas:
            href = data[1]
            if href == x:
                #print("trues",x,href)
                return "true"
                break
            else:
                #print("falses",x,href)
                return "false"
    except:
       print ("Error: unable to fetch data")
    db.close()
def research():
    driver.get(link);
    time.sleep(0.3)
    #get all link
    box = driver.find_elements_by_tag_name('section')
    for i in range(1,20):#len(box)):
        sptime = time.process_time()
        try:
            titles = driver.find_element_by_xpath("//div[@class='items-box-content clearfix']//section["+str(i)+"]//figure[@class='items-box-photo']//img[1]").get_attribute("alt")
            hrefs = driver.find_element_by_xpath("//div[@class='items-box-content clearfix']//section["+str(i)+"]//a[1]").get_attribute("href")
            prices = driver.find_element_by_xpath("//div[@class='items-box-content clearfix']//section["+str(i)+"]//div[@class='items-box-price font-5']").text
            likess = driver.find_element_by_xpath("//div[@class='items-box-content clearfix']//section["+str(i)+"]//span").text
            eptime = time.process_time()
        except NoSuchElementException:
            likess = "0"
            eptime = time.process_time()
        time_updates = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print("Time: "+str(eptime-sptime))
        if gethref(hrefs) == "true":
            print(hrefs,"true")
            # if getprice("SELECT * FROM post") == prices:
            #     #update time
            # else:
            #     #insert post with new price
        elif gethref(hrefs) == "false":
            print(hrefs,"false")
            insert(hrefs,titles,likess,prices,time_updates)
    # if success:
    #     print ('success')
    # if failure:
    #     print ('failure')
    # else:
    #     driver.refresh()
    #     time.sleep(10)
    #     research()

research()

# driver.quit()
# quit()
