import requests
from bs4 import BeautifulSoup
import re
import urllib
from scrapy.http import TextResponse
from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed
)

url_string = "https://sfbay.craigslist.org/sfc/apa/d/oakland-house-for-rent/7069370575.html"
url_st= "https://sfbay.craigslist.org/sfc/apa/d/oakland-house-for-rent/7069370471.html"
sqft_urls= ["https://sfbay.craigslist.org/sfc/apa/d/oakland-house-for-rent/7069370575.html","https://sfbay.craigslist.org/sfc/apa/d/oakland-house-for-rent/7069370471.html"]
sqft_urls.append("https://sfbay.craigslist.org/sfc/apa/d/oakland-house-for-rent/7069370274.html")
no_repeats = sqft_urls
url_string= ""
removing= []
url= "https://sfbay.craigslist.org/search/sfc/apa"


#for getting pictures

urls= ["https://sfbay.craigslist.org/sfc/apa/d/pleasanton-fabulous-3-bed2bath/7073151657.html", "https://sfbay.craigslist.org/sfc/vac/d/oakland-rare-find-lodge-in-the-oakland/7071103395.html"]

import logging
import threading
import time


def load_url(url, timeout):
    return [timeout+60]

def sqft_search(housing_urls):
    housing_urls = housing_urls
   #list of sqft and corresponding urls
    sqft_urls =[]
    for i in range(len(housing_urls)): 
          r= requests.get(housing_urls[i]) 
          soup= BeautifulSoup(r.text, 'html.parser')

          spans= soup.findAll('span',{'class':'housing'})
          if len(spans) != 0:
            if re.search('.+\-(.+)ft.+',spans[0].text):
              sqfts= re.findall('.+\- (.+)ft.+',spans[0].text)
              sqft_urls.append([int(sqfts[0]), housing_urls[i]])
              print("done")
            else:
               housing_urls[i]= "error"
            spans.clear() 

                     
    return sqft_urls

def next_page(url):
    r= requests.get(url)
    new_url= ""
    soup = BeautifulSoup(r.text, 'html.parser')
    a_tags= soup.findAll('a',{'class':'button next'})
    for tag in a_tags:
        new_url = tag.get('href', None)
    
    
    return "https://sfbay.craigslist.org"+ new_url

def souper(url):
    r= requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    ul_tags = soup.findAll('ul',{'class':'rows'})
    s=0

    #supposed to have the urls for the 1 page
    housing_urls= []
    li_tags= soup.findAll('li',{'class':'result-row'})
    for i in range(len(li_tags)):
      for tag in li_tags[i].find_all('a'):
           if s%3 == 0:
             housing_urls.append(tag.get('href',None))
           s+=1       
    
    return housing_urls

def runner():
 url= "https://sfbay.craigslist.org/search/sfc/apa"
 pages=[url]
 for i in range(24):
    url= next_page(url)
    pages.append(url)
    if i==23:
        break

 print(pages)
 entire_apartment_list= []
 with ThreadPoolExecutor(max_workers=3) as executor:
         tasks = [executor.submit(souper, pages[pagenum]) for pagenum in range(4)]
         for future in as_completed(tasks):
             try:
                 apartment_list_from_page  = future.result()
                 if len(apartment_list_from_page) > 0:
                    entire_apartment_list.append(apartment_list_from_page)
             except Exception as exc:
                raise(exc)
 
 print("s")
 #flattens the apts urls 
 entire_apartment_list=sum(entire_apartment_list,[])
 return len(entire_apartment_list)


print(runner())
