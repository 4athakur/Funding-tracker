import pandas as pd
import requests
from bs4 import BeautifulSoup
header={'User-Agent':'Mozila/5.0'}
url='https://coinswitch.co/pro/futures-perpetual/USINR'
r=requests.get(url)
webpage=r.text
soup=BeautifulSoup(webpage,'lxml')
print(soup.prettify())
# data=soup.find_all('div')
# print(soup.find('p', class_="tw-mt-2 tw-flex tw-w-full tw-items-center tw-gap-x-2 tw-overflow-x-scroll tw-scrollbar-hide"))