#!/usr/bin/env python
# coding: utf-8

# In[1]:


# !conda install -c anaconda beautifulsoup4 requests pymongo -y

from bs4 import BeautifulSoup as bs
import requests
import re
from pymongo import MongoClient
import time
import datetime


# In[2]:


response = requests.get("http://www.gutenberg.org/wiki/Gutenberg:Offline_Catalogs")


# In[3]:


html_soup = bs(response.text, 'html.parser')


# In[6]:


def process_txt(text):
    book_list=[]
    text = text.encode('utf-8').decode("ascii","ignore")
    # pattern fails to match every deatils for very long titles
    for match in re.findall(r"(^(?:[\w,.-]+\s)+)\s+(\d{5})\s+((?:\[.*?\n*.*?\])(?:\s)*)*",text, re.MULTILINE):
        # ignore non english books with [Language: *]
        if not re.match("\[Language:",match[-1].strip()):
            book_details = [x.strip() for x in match[0].split(', by')]
            # ignore books with no author name
            if len(book_details) > 1 and len(book_details) < 3:
#                 title, author = book_details
                book_list.append(book_details)
    return book_list
mongoConnectionString="mongodb://csciDarshan:csciDarshan123@docdb-2020-03-11-00-58-01.cluster-chnyvyrv3c0z.us-east-1.docdb.amazonaws.com:27017/?ssl=true&ssl_ca_certs=rds-combined-ca-bundle.pem&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false"


def insert_books(file, book_list, start_time, end_time):
    client = MongoClient(mongoConnectionString)
    booksdb = client["gu_books"]
    bookscol = booksdb["books"]
    for (title, author) in book_list:
        bookscol.insert_one({"title":title,"author":author})
    # store filename , start_time, end_time
    booksdb["p_time"].insert_one({"file":file_name, "start": start_time, "end": end_time})
#     print(bookscol.inserted_ids)


# In[8]:


#mw-content-text > div > ul:nth-child(12)
for li in html_soup.select("#mw-content-text > div > ul:nth-child(12) li"):
    file_name = li.a["href"].split("/")[-1]
    print(file_name)
    start_time = datetime.datetime.now()
    txt_file = requests.get("http:"+str(li.a["href"])).text
    book_list = process_txt(txt_file)
    end_time = datetime.datetime.now()
    insert_books(file_name, book_list, start_time, end_time)
    time.sleep(300)


# In[ ]:




