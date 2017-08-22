## 一、前言
这次的实验的任务是要爬取[天天基金网](http://fund.eastmoney.com/allfund.html)的6000多个基金，并把爬取的数据存放到Mongodb数据库中，数据以供下次分析使用。而此次 需要采集的数据来自两个页面
- [页面１](http://fund.eastmoney.com/allfund.html)：从该页面爬取 所有基金代码、基金名称、基金ＵＲＬ
- [页面２](http://fund.eastmoney.com/000001.html)：从上个页面获取的基金ＵＲＬ地址爬取对应基金的近1个月、近3个月、近6个月、近1年、近3年、成立来的变动百分比。

## 二、运行环境
- Python3
- requests
- MongoDb
- bs4
- pymongo
- re

由于python2的字符编码问题确实让人蛋疼，所以今后的试验项目全部改成python3开发,下面会详细介绍蛋疼的原因。

关于python2和python3字符编码的问题可以参考以下链接：
[关于Python2.X与Python3.X的编码问题](http://blog.csdn.net/mickeymouse1928/article/details/70168794)
[ Python2和Python3之间关于字符串编码处理的差别](http://blog.csdn.net/yanghuan313/article/details/63262477)

## 三、实例分析
### 页面一分析
1. [天天基金网](http://fund.eastmoney.com/allfund.html)这个页面所有从０至７开头的基金代码分别放在'class="num_box"对应的８个div中，其中每个li对应的就是基金所有信息，最后我们用正则表达式就可以取到我们需要的基金名称、基金代码和URL地址。
取所有li基金信息用BeautifulSoup的select方法:
```select('.num_right > li')```

2.  用循环方法取每个基金信息，并配合正则表达式，就可以得到我们需要的基金名称、基金代码和url地址。
```
for tag in tags:
　content=tag.a.text  #取第一个<a>的文本数据
　code=re.findall(r'\d+',content)[0]　＃\d+从文本数据里取数字，位数至少大于等于１位，正则表达式取得的结果用列表，所以后面用[0]取出数据
　name=content.split('）')[1]   #用中文'）'分割取第二个值得到基金名称
```
3. 七个.num中的最后一个<li>里面的内容为空值，需要在此做判断，否则会提示:not of index
```
if tag.a is None:
    contine　＃如果为空值，跳过
else:
    
```
 4. 两个页面分别用了两种编码方式，第一个页面是gb2312，第二个页面是utf-8，所以分别定义了２个不同编码函数，供两个页面调用
```
html=requests.get(url,headers=header).content.decode('gbk')
#gbk编码扩展了gb2312，还支持中文繁体
html=requests.get(url,headers=header).content.decode('utf-8')
```
### 页面二分析
1. 从页面1传给页面２的url地址，url格式如：http://fund.eastmoney.com/000001.html 可以分析得出需要的数据放在dd 标签里。
先用BeautifulSoup的select方法搜索到。
再用find_all方法获取dd标签里的第二个span标签。
```
tags=soup.select('dd')
m1=(tags[1].find_all('span')[1].string)
y1=(tags[2].find_all('span')[1].string)
m3=(tags[4].find_all('span')[1].string)
y3=(tags[5].find_all('span')[1].string)
m6=(tags[7].find_all('span')[1].string)
rece=(tags[8].find_all('span')[1].string)
detail={'代码':code,'名称':name,'近1月':m1,'近3月':m3,'近6月':m6,'近1年':y1,'近3年':y3,'成立来':rece}
```
2. 但当用以上方法获取信息到基金代码000009时，又提示错误“IndexError: list index out of range”，经分析从页面１获取的url地址在页面2生成的页面有２种布局方式。
于是再写一个函数获取第二种布局方式
```
tags=soup.find_all(class_='ui-font-middle ui-color-red ui-num')
m1=tags[3].string
y1=tags[4].string
m3=tags[5].string
y3=tags[6].string
m6=tags[7].string
rece=tags[8].string
detail={'代码':code,'名称':name,'近1月':m1,'近3月':m3,'近6月':m6,'近1年':y1,'近3年':y3,'成立来':rece}
```
在第一个方法里加入try...except...　捕捉错误，当遇到错误时运行第二个函数

３. 把requests和BeautifulSoup单独写成一个模块，以便给其他函数共用。
```
from bs4 import BeautifulSoup
import requests,random
def geturl_gbk(url):
	html=requests.get(url,headers=header).content.decode('gbk')
	soup=BeautifulSoup(html,'lxml')
	return soup
def geturl_utf8(url):
	html=requests.get(url,headers=header).content.decode('utf-8')
	soup=BeautifulSoup(html,'lxml')
	return soup	

```

### 导入MongoDb数据库

```
import pymongo
clients=pymongo.MongoClient('127.0.0.1')
#建立链接
db=clients['hexun']
#指定数据库
col1=db['fund']
＃返回数据集合１
col2=db['detail']
＃返回数据集合２
```
## 四、实战代码
代码贴图：
完整代码：
## 五、总结
1. requests.content和requests.text的方法．content返回的是二进制内容要用decode指定编码；text根据网页编码响应内容来猜测编码，但此处依旧要指定编码．
```
html=requests.get(url).decode('gbk')
print (html)
```
```
html=requests.get(url)
html.encoding='gbk'
print (html.text)
```

2. 此网站会判断爬虫，断开连接，如下提示：
>("Connection broken: ConnectionResetError(104, 'Connection reset by peer')", ConnectionResetError(104, 'Connection reset by peer'))

所以加上了随机代理
```
proxies=['http://118.178.124.33:3128',
'http://139.129.166.68:3128',
'http://61.163.39.70:9999',
'http://61.143.228.162']

html=requests.get(url,headers=header,proxies={'http':random.choice(proxies)}).content.decode('gbk')
```
