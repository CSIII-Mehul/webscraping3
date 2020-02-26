import requests
from bs4 import BeautifulSoup
import re
import urllib
from scrapy.http import TextResponse
from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed
)


def rank_sqft(sqft_urls):
 
  sqft_urls.sort() 
  sqft_urls.reverse()      
  #print(sqft_urls[0][0])
  

  ranks= sqft_urls
  
  return ranks

print(rank_sqft([[1,"rhrh"],[3,"fdgfgfg"], [2,"sdsdsd"]]))