from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import pymysql
import time
options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images":2}

options.add_experimental_option("prefs",prefs)
options.add_argument("--window-size=1000,768")#--start-maximized
driver = webdriver.Chrome("S:/Career/merukali_price/chromedriver.exe",options=options)
link = "https://www.mercari.com/jp/search/?page=1"+"&keyword=ストッキング"

driver.get(link)
box = driver.find_elements_by_tag_name('section')
for i in range(1,len(box)):
    try:
        titles = driver.find_element_by_xpath("//div[@class='items-box-content clearfix']//section["+str(i)+"]//figure[@class='items-box-photo']//img[1]").get_attribute("alt")
        print(str(i))
        imgs = driver.find_element_by_xpath("//div[@class='items-box-content clearfix']//section["+str(i)+"]//figure[1]//img[1]").get_attribute("data-src")
        print("no: "+str(i)+"img: "+str(imgs))

    except NoSuchElementException:
        likess = "0"
