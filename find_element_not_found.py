# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 13:06:21 2024

@author: NAdhikari
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import pandas as pd
import time
from selenium.common.exceptions import TimeoutException

import pickle
from collections import Counter

# def fetch_heim_names(driver, actions, wait, base_url):
#     index1 = 72
#     index2 = 73
#     heim_names = []

#     # Loop through the pages
#     while index1 <= 319: 
#         url = f'{base_url}offset={index1 * 9}&search=&page={index2}'   
#         driver.get(url)
#         time.sleep(2)  # Wait for the page to load
        
#         # Accept only optional cookies to open the page
#         try:
#             allen_zustimmen = wait.until(EC.element_to_be_clickable(
#                 (By.CSS_SELECTOR, '#app-main > div > section > div > div > div.cookieControl__BarButtons > button:nth-child(2)')))
#             actions.move_to_element(allen_zustimmen).pause(1).click(allen_zustimmen).perform()
#         except TimeoutException:
#             pass

#         # Fetch all 'heim' names
#         try:
#             seniorenheim = wait.until(EC.presence_of_all_elements_located(
#                 (By.CSS_SELECTOR, 'div > div.row.card-facility-top-section > div.col-sm-8.col-12 > div:nth-child(1) > div > h4 > a')))
#         except TimeoutException:
#             print(f"Element not found on page {index2}, skipping to the next page.")
#             continue 
        
#         try:
#             seniorenheim = driver.find_elements(By.CSS_SELECTOR, 
#                 'div > div.row.card-facility-top-section > div.col-sm-8.col-12 > div:nth-child(1) > div > h4 > a')
            
#             if not seniorenheim:
#                 print(f"No more 'heim' found on page {index2}. Exiting loop.")
#                 break

#             # Loop through each 'heim' on the page and extract the name
#             for heim in seniorenheim:
#                 actions.move_to_element(heim).perform()
#                 name_heim = heim.text
#                 heim_names.append(name_heim)  # Save name to the list
           
                
#         except Exception as e:
#             print(f"Error navigating or finding elements on page with index {index2}: {e}")
#             break
        
#         # Increment the page index for pagination
#         index1 += 1  
#         index2 += 1

#     return heim_names
                
# driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))

# base_url = 'https://heimverzeichnis.de/einrichtungen/suche?'
# actions = ActionChains(driver)
# wait = WebDriverWait(driver, 5)

# driver.quit()

# heim_names = fetch_heim_names(driver, actions, wait, base_url)

# with open('list.pkl', 'wb') as file:
#     pickle.dump(heim_names, file)
    
with open('list.pkl', 'rb') as file:
    heim_list = pickle.load(file)
    

    
df2 = pd.read_csv(r'Heimverzeichnis\heimverzeichnis1_73_648_319_2862.csv')
heim_list_stripped = [str(item).strip() for item in heim_list]
reha_column_stripped = df2['reha'].astype(str).str.strip().tolist()
heim_list_count = Counter(heim_list_stripped)
reha_column_count = Counter(reha_column_stripped)
elements_with_fewer_counts = {item: heim_list_count[item] - reha_column_count.get(item, 0)
                              for item in heim_list_count
                              if heim_list_count[item] > reha_column_count.get(item, 0)}
print(f"Number of elements with fewer occurrences in the dataframe: {len(elements_with_fewer_counts)}")
for item, diff in elements_with_fewer_counts.items():
    print(f"'{item}' appears {diff} more times in the list than in the dataframe.")