## 1.前言
参考了作者布咯咯_rieuse的《爬取豆瓣电影中速度与激情8演员图片》一文，原文地址：爬取豆瓣电影中速度与激情8演员图片 。于是开始学习、模仿、改进。把自己学习的过程在此整理，与大家一起分享。
目标：爬取图片，并用对应图片的明星中文名字为文件名保存于电脑中。
地址：[战狼2](https://movie.douban.com/subject/20451290/celebrities) 
     ![pic1](https://github.com/boymag/pythoncode/blob/master/douban-movie/png/1.png)
## 2、分析
本次爬取使用第三方的requests库，同时也是使用了urllib.urlretrieve函数下载文件。
解析主要使用了BeautifulSoup，部分也使用了re正则表达式
1. 导入需要的库
```
import requests
from bs4 import BeautifulSoup 
```
2. 获取地址，使用BS库并使用lxml解析器
```
html=requests.get(url).content
soup=BeautifulSoup(html,'lxml')
```
3. 抓取<title>标签中的片名作为文件的保存目录
![pic2](https://github.com/boymag/pythoncode/blob/master/douban-movie/png/2.png)
