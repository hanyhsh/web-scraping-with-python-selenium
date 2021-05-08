# -*- coding: utf-8 -*-
"""
Created on Sat May  1 11:51:10 2021

@author: Hany Awadalla
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pickle
import pandas as pd
import time


# geolocation API not supported
geoDisabled = webdriver.FirefoxOptions()
geoDisabled.set_preference("geo.enabled", False)
#

driver = webdriver.Firefox(executable_path="./geckodriver.exe",options=geoDisabled)

link = "https://www.eat.ch/speisekarte/restaurant-lalina"

#"https://www.eat.ch/speisekarte/vapiano-zuerich-raemistrasse"
driver.get(link)
html = driver.page_source


cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
    driver.add_cookie(cookie)

#pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
################################################################################

start_time = time.time()


ggo = driver.find_elements_by_class_name('menucard__meals-group') # the food sections



sidedishes_list = []
df_list = []
for s in ggo:
    category = s.find_element_by_class_name('menucard__category-name').text
    g = s.find_element_by_class_name('menucard__meals') # the menuu inside each container
    c = g.find_elements_by_class_name("meal-container")
    for i in c:
        name  = i.find_elements_by_class_name("notranslate")[0].text
        price = i.find_elements_by_class_name("notranslate")[1].text
        try:
            info  = i.find_elements_by_class_name("meal__description-additional-info")
            for e in info:
                meal__info = e.text
        except:
            meal__info = ""
            pass
        try:
            meal__choose = i.find_element_by_class_name("meal__description-choose-from").text
        except:
            meal__choose = ""
            pass
        try:
            mm = i.find_elements_by_class_name("meal__description-attribute-description")
            if len(mm)> 1:
                attribute = mm[0].text + mm[2].text
            else:
                attribute = mm[0].text
        except:
            attribute = ""
            pass
        
        try:
            i.find_element_by_class_name('js-meal__add-to-basket-button').click()
        except:
            pass
        try:
            ff= i.find_elements_by_class_name('show-more')
            for f in ff:
                f.click()
        except:
            pass
        
        sidedishes_list = []
        mo = i.find_elements_by_class_name('inline-desc')
        for n in mo:
            sidedish= n.text
            
            try:
                sidedishprice = n.find_element_by_class_name('sidedish-item-price').get_attribute('innerText')
            except:
                sidedishprice= ""
                
            sidedishes =  sidedish + " "+ sidedishprice              
            
            sidedishes_list.append({sidedishes})
            pass
        try:
            me = i.find_elements_by_class_name('pulldown')
            dropdown = me[0].text.replace("\n", ", ")
        except:
            dropdown = ""
            pass
        
        
        
        try:
            me = i.find_elements_by_class_name('pulldown')
            dropdown2 = me[3].text.replace("\n", ", ")
        except:
            dropdown2 = ""
            pass
        if len(dropdown2) <30:
            dropdown2 = ""
            
        

        
        df_list.append({"category":category,"name":name,"price":price, "meal__info":meal__info,\
                        "meal__choose":meal__choose, "attribute":attribute, "sidedishes_list":sidedishes_list,\
                            "dropdown":dropdown,"dropdown2":dropdown2})

print("\nThis took %s seconds." % (time.time() - start_time)) 
          
df = pd.DataFrame(df_list, columns=("category","name","price", "meal__info", "meal__choose", "attribute","sidedishes_list", "dropdown", "dropdown2"))
df.to_csv("006.csv",index= False, encoding=('utf-8'))
