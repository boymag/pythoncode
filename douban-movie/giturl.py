#coding=utf-8
import requests
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
def geturl(url):
    html=requests.get(url).content
    soup=BeautifulSoup(html,'lxml')
    return soup
