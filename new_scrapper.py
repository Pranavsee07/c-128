from selenium import webdriver 
from selenium.webdriver.common.by import By  
from bs4 import BeautifulSoup  
import time 
import pandas as pd 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC  
# import request module
import requests

browser = webdriver.Chrome() 

new_planets_data = []  

def scrape_more_data(hyperlink):
        # Use request to get the hyperlink and store in page variable
        page = requests.get(hyperlink)
        # Create soup using BeautifulSoup
        soup = BeautifulSoup(page.content,"html.parser")
        # Create empty temp_list
        temp_list = []
        # Create a list information_to_extract with text of each div for which information is needed
        information_to_extract = ["Planet Type:","Discovery Date:","Planet Mass:","Planet Radius:","Orbital Radius:","Orbital Period:","Discovery Method:"]
        

        # Run a for loop for each info_name in  information_to_extract
        for info_name in information_to_extract:
                # Add try block
                try:
                    # Get the value needed using find() and find_next() and append to temp_list
                    value = soup.find('div',text = info_name).find_next('span').text.strip()
                    print(value)
                    temp_list.append(value)
                # Add a except block
                except:
                    # Add Unknown to temp_list
                    temp_list.append("Unknown")
        # append temp_list to new_planets_data
        new_planets_data.append(temp_list)
        

# Read the scrapped_data.csv in planet_df_1
planet_df_1 = pd.read_csv("scraped_data.csv")
# Loop through each row 
for index,row in planet_df_1.iterrows():
      
    # Print hyperlink
    print(row["hyperlink"])
    # Call scrap_more_data and pass hyperlink
    scrape_more_data(row["hyperlink"])
    # Print Data scrapping at hyperlink completed
    print(f"datascrapping@hyperlink{index + 1}completed")

headers = ["planet_type","discovery_date", "mass", "planet_radius", "orbital_radius", "orbital_period", "detection_method"]
new_planet_df_1 = pd.DataFrame(new_planets_data,columns = headers)
new_planet_df_1.to_csv('new_scraped_data.csv',index=True, index_label="id")
