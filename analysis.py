
from selenium import webdriver

#Get all info from link;

options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images":2}

options.add_experimental_option("prefs",prefs)
options.add_argument("--start-maximized")

driver = webdriver.Chrome("S:/Career/merukali_price/chromedriver.exe",options=options)

driver.quit()
quit()
