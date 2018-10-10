
from selenium import webdriver

#Get all info from link;

options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images":2}

options.add_experimental_option("prefs",prefs)
options.add_argument("--start-maximized")

driver = webdriver.Chrome("S:/Career/merukali_price/chromedriver.exe",options=options)
link = 'https://www.mercari.com/jp/brand/1620/'
keyword = ''


def research():
    driver.get(link);
    #get all link
    box = driver.find_elements_by_tag_name('section')
    titles=[]
    hrefs=[]
    for i in range(1,5):#len(box)):
        titles.append(driver.find_element_by_xpath("//div[@class='items-box-content clearfix category-brand-list']//section["+str(i)+"]//figure[@class='items-box-photo']//img[1]").get_attribute("alt"))
        hrefs.append(driver.find_element_by_xpath("//div[@class='items-box-content clearfix category-brand-list']//section["+str(i)+"]//a[1]").get_attribute("href"))

    print(titles[1]+hrefs[1])
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
