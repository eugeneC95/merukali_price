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
options.add_argument("--window-size=100,100")#--start-maximized
driver = webdriver.Chrome("D:/Documents/Career/merukali_price/chromedriver.exe",options=options)
#https://www.mercari.com/jp/brand/1620/
keyword = 'ジャケット'
db = pymysql.connect(host='206.189.90.203',user='zun95',passwd='Hotdilvin95',db='merucali')
cursor = db.cursor()
def insertpost(hre,imges,tit,lik,sto,pri,tim):
    try:
        cursor.execute("INSERT into list (href,img,title,likes,stock,price,time_update) VALUES(%s ,%s ,%s, %s, %s, %s, %s)",(hre,imges,tit,lik,sto,pri,tim))
        db.commit()
    except:
        print('error')
        db.rollback()
def insertchange(hre,imges,tit,lik,sto,pri,tim):
    try:
        cursor.execute("INSERT into changes (href,img,title,likes,stock,price,time_update) VALUES(%s ,%s ,%s, %s, %s, %s, %s)",(hre,imges,tit,lik,sto,pri,tim))
        db.commit()
    except:
        print("errorChanges")
        db.rollback()
def gethref(x):
    try:
        cursor.execute("SELECT * FROM list WHERE href LIKE %s",(x))
        datas = cursor.fetchall()
        if datas != ():
            for data in datas:
                price = data[6]
            return "true",price
        elif datas == ():
            return "false","0"
    except:
        print ("Error: unable to fetch data")
def get(x,h):
    try:
        cursor.execute("SELECT * FROM list WHERE href LIKE %s ORDER BY time_update ASC",(x))
        datas = cursor.fetchall()
        if len(datas) > 1:
            #main reinput
            for data in datas:
                link = data[1]
                imgs = data[2]
                title = data[3]
                likes = data[4]
                stock = data[5]
                prices = data[6]
                time = data[7]
                #print(link,title,likes,stock,prices,time)
                cursor.execute("SELECT * FROM changes WHERE href LIKE %s AND img LIKE %s AND title LIKE %s AND likes LIKE %s AND stock LIKE %s AND price LIKE %s",(link,imgs,title,likes,stock,prices))
                datos = cursor.fetchall()
                if len(datos) >= 1:
                    print("data alaready haved")
                    break
                else:
                    insertchange(link,imgs,title,likes,stock,prices,time)
                    print("insert new data to table")
        else:
            #donothings
            print(str(h),"none duplicate")
    except:
        print ("Errorget: unable to fetch data")
def updatetime(tim,hre,pri):
    try:
        cursor.execute("UPDATE list SET time_update =%s WHERE href = %s && price =%s",(tim,hre,pri))
        db.commit()
    except:
        print ("Error: unable to fetch data")
def index():
    prices =[]
    da = ""
    cursor.execute("SELECT href,time_update FROM changes LIMIT 0,5")
    datas = cursor.fetchall()
    for data in datas:
        if da == "":
            cursor.execute("SELECT * FROM changes WHERE href LIKE %s",data[0])
        else:
            cursor.execute("SELECT * FROM changes WHERE href LIKE %s AND time_update NOT LIKE (SELECT time_update FROM changes WHERE time_update LIKE %s)",(data[0],da))
        da = data[1]
        datos = cursor.fetchall()
        for dato in datos:
            prices.append(int(dato[6]))
            print(str(dato[6]) + str(dato[3]))
        # price = prices[1] - prices[0]
        # prices = []
        # print(price)

def rearrange():
    try:
        cursor.execute("SELECT * FROM list ")
        datas = cursor.fetchall()
        h = 0
        for data in datas:
            link = data[1]
            h += 1
            get(link,h)
    except:
        print ("Errormain: unable to fetch data")
def research(j):
    link = "https://www.mercari.com/jp/search/?page="+str(j)+"&keyword="+keyword
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
            imgs = driver.find_element_by_xpath("//div[@class='items-box-content clearfix']//section["+str(i)+"]//img[1]").get_attribute("data-src")
            print("img: "+str(imgs))
            likess = driver.find_element_by_xpath("//div[@class='items-box-content clearfix']//section["+str(i)+"]//span").text
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
                insertpost(hrefs,imgs,titles,likess,stock,prices,time_updates)
                print("New Uploaded\n")
        else:
            imgs = str(imgs)
            insertpost(hrefs,imgs,titles,likess,stock,prices,time_updates)
            print("Uploaded\n")
    driver.refresh()
    time.sleep(1)

    if j >= 3:
        j=1
    else:
        j += 1
    print("lopped\n" + str(j))
    rearrange()
    research(j)
#research(1)
index()
db.close()
# driver.quit()
# quit()
