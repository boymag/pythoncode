#coding=utf-8
import geturl,re,urllib,os
soup=geturl.geturl('https://movie.douban.com/subject/20451290/celebrities')
movie=soup.title.string.split(' ')[0]
tags=soup.find_all(class_='list-wrapper')
stars=[]
for tag in tags[1].find_all('li'):
    title=tag.a['title'].split(' ')[0]
    img_url=re.findall(r'https://img\d.doubanio.com/img/celebrity/medium/.*.jpg',str(tag))[0]
    stars.append([title,img_url])

if not os.path.exists(movie):
    os.makedirs(movie)
    for star in stars:
        filename=os.path.join(movie,star[0]+'.jpg')
        with open(filename,'w') as f:
            urllib.urlretrieve(star[1],filename)
