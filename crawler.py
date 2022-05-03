import numpy as np
import pandas as pd
import requests
import bs4
import lxml.etree as xml
import json
import pickle

URL = "https://en.wikipedia.org/wiki/Lists_of_World_Heritage_Sites"
web_page = bs4.BeautifulSoup(requests.get(URL, {}).text, "lxml")
cont_names =  web_page.find_all(name="span", attrs={"class": "mw-headline"})[2:]
continents_div = web_page.find_all(name="div", attrs={"class": "div-col"})[1:]
continents_li = []
cnt = 0
reg_info = []
cont_info = []
herit_dict = {}

def proc_country_page(country_web_page, reg_info):
    
    list_table = country_web_page.find_all(name="table")[0]
    
    if('peru' in reg_info.lower() 
       or 'bangladesh' in reg_info.lower()
       or 'united states' in reg_info.lower()
       or 'vietnam' in reg_info.lower()):
        list_table = country_web_page.find_all(name="table")[1]
    if('kingdom' in reg_info.lower()
       or 'san marino' in reg_info.lower()
       or 'andorra' in reg_info.lower()
       or 'laos' in reg_info.lower()
       or 'myanmar' in reg_info.lower()
       or 'singapore' in reg_info.lower()):
        list_table = country_web_page.find_all(name="table")[2]
    if('turkmenistan' in reg_info.lower() 
       or 'vatican' in reg_info.lower()
       or 'kyrgyzstan' in reg_info.lower()):
        return
        
    li_row = list_table.find_all("tr")
    headers = li_row[0].find_all("th")
    desc_idx = 0
    
    for count, header in enumerate(headers):

        if('description' in header.text.lower()):
            desc_idx = count - 1
 
    for site in li_row:

        if(site.find("th")):
            if(site.find("th").find("a")):

                try:
                    herit_dict[site.find("th").find("a").text] = {'continent': cont_info[cont_cnt], 
                                                                  'country' : reg_info}
                
                    if(site.find_all("td")):
                        herit_dict[site.find("th").find("a").text]['desc'] = site.find_all("td")[desc_idx].text
    
                        if(site.find_all('td')[0].find("a")):
                            img_url = "https://en.wikipedia.org/" + site.find_all('td')[0].find("a")["href"]
                            img_pg = bs4.BeautifulSoup(requests.get(img_url, {}).text, "lxml")
                            if(img_pg.find_all(name="div", attrs={"class": "fullImageLink"})):
                                img_file_link = img_pg.find_all(name="div", attrs={"class": "fullImageLink"})[0].find("a")["href"]
                            herit_dict[site.find("th").find("a").text]['img_link'] = img_file_link
    
                        if(site.find_all('td')[1].find("a")):
                            img_url = "https://en.wikipedia.org/" + site.find_all('td')[1].find("a")["href"]
                            img_pg = bs4.BeautifulSoup(requests.get(img_url, {}).text, "lxml")

                            if(img_pg.find_all(name="div", attrs={"class": "fullImageLink"})):
                                img_file_link = img_pg.find_all(name="div", attrs={"class": "fullImageLink"})[0].find("a")["href"]
                            herit_dict[site.find("th").find("a").text]['img_link'] = img_file_link
                except:
                    herit_dict.pop(site.find("th").find("a").text)
            
        elif(site.find_all("td")):  
            
            if(site.find("td").find("a")):

                try:
                    herit_dict[site.find("td").find("a").text] = {'continent': cont_info[cont_cnt], 
                                                                  'country' : reg_info}
                
                
                    herit_dict[site.find("td").find("a").text]['desc'] = site.find_all("td")[desc_idx].text
                    
                    if(site.find_all("td")[1].find("a")):
                        img_url = "https://en.wikipedia.org/" + site.find_all("td")[1].find("a")["href"]
                        img_pg = bs4.BeautifulSoup(requests.get(img_url, {}).text, "lxml")
                        if(img_pg.find_all(name="div", attrs={"class": "fullImageLink"})):
                            img_file_link = img_pg.find_all(name="div", attrs={"class": "fullImageLink"})[0].find("a")["href"]
                            herit_dict[site.find("td").find("a").text]['img_link'] = img_file_link
                except:
                    herit_dict.pop(site.find("td").find("a").text)
                
            else:
                herit_dict[site.find_all("td")[1].text] = {'continent': cont_info[cont_cnt], 
                                                              'country' : reg_info}
                
                herit_dict[site.find_all("td")[1].text]['desc'] = site.find_all("td")[desc_idx].text
                
                if(site.find_all("td")[2].find("a")):
                    img_url = "https://en.wikipedia.org/" + site.find_all("td")[2].find("a")["href"]
                    img_pg = bs4.BeautifulSoup(requests.get(img_url, {}).text, "lxml")

                    if(img_pg.find_all(name="div", attrs={"class": "fullImageLink"})[0].find("a")):
                        img_file_link = img_pg.find_all(name="div", attrs={"class": "fullImageLink"})[0].find("a")["href"]
                        herit_dict[site.find_all("td")[1].text]['img_link'] = img_file_link

cont_cnt = 0

for continent in continents_div:
        cont_info.append(cont_names[cont_cnt].text)
        continent_div = continent.find_all("ul")

        for region in continent_div:
            region_div = region.find_all("ul")
            
            for countries in region_div:
                country_list = countries.find_all("li")
                
                for country in country_list:
                    if(cnt < 100):
                        country_anch = country.find("a")
                        country_split = country_anch['title'].split('List of World Heritage Sites')
                        print(country_split)
                        reg_info.append(country_split[len(country_split) - 1])
                        country_url = "https://en.wikipedia.org/" + country_anch['href']
                        country_web_page = bs4.BeautifulSoup(requests.get(country_url, {}).text, "lxml")
                        proc_country_page(country_web_page, reg_info[0])
                        print(cnt)
                        reg_info = []
                    cnt += 1
        cont_cnt += 1

URL = "https://en.wikipedia.org/wiki/List_of_World_Heritage_Sites_in_Central_America"
web_page = bs4.BeautifulSoup(requests.get(URL, {}).text, "lxml")
herit_li = web_page.find_all(name="table")[0]
li_row = herit_li.find_all("tr")

for site in li_row:
    if(site.find("th")):
        if(site.find("th").find("a")):
            herit_dict[site.find("th").find("a").text] = {'continent': 'Americas', 
                                                          'country' : 'Central America'}
    
            herit_dict[site.find("th").find("a").text]['desc'] = site.find_all("td")[len(site.find_all("td")) - 2].text
            
    if(site.find("td")):

        if(site.find("td").find("a")):
            img_url = "https://en.wikipedia.org/" + site.find("td").find("a")["href"]
            img_pg = bs4.BeautifulSoup(requests.get(img_url, {}).text, "lxml")
            img_file_link = img_pg.find_all(name="div", attrs={"class": "fullImageLink"})[0].find("a")["href"]
            herit_dict[site.find("th").find("a").text]['img_link'] = img_file_link
        
URL = "https://en.wikipedia.org/wiki/List_of_World_Heritage_Sites_in_Oceania"
web_page = bs4.BeautifulSoup(requests.get(URL, {}).text, "lxml")
herit_li = web_page.find_all(name="table")[0]
li_row = herit_li.find_all("tr")

for site in li_row:
    if(site.find("th")):
        if(site.find("th").find("a")):
            herit_dict[site.find("th").find("a").text] = {'continent': 'Oceania', 
                                                          'country' : 'Oceania'}
        
            herit_dict[site.find("th").find("a").text]['desc'] = site.find_all("td")[len(site.find_all("td")) - 1].text
        
        if(site.find("td")):
            if(site.find("td").find("a")):
                img_url = "https://en.wikipedia.org/" + site.find("td").find("a")["href"]
                img_pg = bs4.BeautifulSoup(requests.get(img_url, {}).text, "lxml")
                img_file_link = img_pg.find_all(name="div", attrs={"class": "fullImageLink"})[0].find("a")["href"]
                herit_dict[site.find("th").find("a").text]['img_link'] = img_file_link

try:
    herit_dict_file = open('E:\Important\Study_Material\CA6005\Project 2\herit_dict.pkl', 'wb')
    pickle.dump(herit_dict, herit_dict_file)
    herit_dict_file.close()
  
except:
    print("Something went wrong")