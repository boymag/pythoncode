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
``` 
movie=soup.title.string.split(' ')[0]
```
4. 抓取演员和对应的图片url
从下图中分析可知中间的<div class="list-wrapper">对应的才是所有演员的信息，所以我们用BS抓取中间的部分，代码如下：
     ![pic3](https://github.com/boymag/pythoncode/blob/master/douban-movie/png/3.png)
     ![pic4](https://github.com/boymag/pythoncode/blob/master/douban-movie/png/4.png)
     
```
tags=soup.find_all(class_='list-wrapper')              #BS遍历所有的list-wrapper类
starts=[]
for tag in tags[1].find_all('li')                      #使用list-wrapper[1] 获取对应的演员的类，再次遍历其下的li 标签
    title=tag.a['title'].split(' ')[0]                 #获取演员名字，去除后面英文名字
    img_url=re.findall(r'https://img\d.doubanio.com/img/celebrity/medium/.*.jpg',str(tag))[0]  #正则表达式获取图片信息，正则表达式返回列表，使用[0]获取数据
     stars.append([title,img_url])                     #追加拼装数据
```     

## 3、完整代码参见github
![pic5](https://github.com/boymag/pythoncode/blob/master/douban-movie/png/5.png)

     
