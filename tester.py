import requests
from bs4 import BeautifulSoup
import re
import urllib
from scrapy.http import TextResponse
from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed
)
from itertools import chain


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
 with ThreadPoolExecutor(max_workers=24) as executor:
         tasks = [executor.submit(souper, pages[pagenum]) for pagenum in range(25)]
         for future in as_completed(tasks):
             try:
                 apartment_list_from_page  = future.result()
                 if len(apartment_list_from_page) > 0:
                    entire_apartment_list.append(apartment_list_from_page)
             except Exception as exc:
                raise(exc)
 
 
 #flattens the apts urls 
 #entire_apartment_list=sum(entire_apartment_list,[])
 
 ordered_sqft= []
 with ThreadPoolExecutor(max_workers=24) as executor:
         tasks = [executor.submit(sqft_search, entire_apartment_list[pagenum]) for pagenum in range(25)]
         for future in as_completed(tasks):
             try:
                 sqft_from_page  = future.result()
                 if len(sqft_from_page) > 0:
                    ordered_sqft.append(sqft_from_page)
             except Exception as exc:
                raise(exc)


 ordered_sqft = chain(*ordered_sqft)
 ordered_sqft = list(ordered_sqft)
 ordered_sqft.sort()
 ordered_sqft.reverse()
 ordered_sqft=repeat_check(ordered_sqft)


 return ordered_sqft

def repeat_check(sqft_urls):
     no_repeats = sqft_urls
     url_string = ""
     removing = []
     for i in range(len(sqft_urls) - 1):
         j = i + 1
         url_string = sqft_urls[i][1]
         url_st = sqft_urls[j][1]
         # re.search('.+\/d/(.+)\/.+',url_string)
         lists = re.findall('.+\/d/(.+)\/.+', url_string)
         temp = re.findall('.+\/d/(.+)\/.+', url_st)
         if lists[0] == temp[0]:
             # print("check")
             removing.append([sqft_urls[j][0], sqft_urls[j][1]])

     for counter in range(len(removing)):
         no_repeats.remove(removing[counter])

     return no_repeats


print(runner())
