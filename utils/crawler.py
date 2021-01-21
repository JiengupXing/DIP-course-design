#! usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  7 10:56:13 2017
CSDN对应文章连接
http://blog.csdn.net/Hk_john/article/details/78455889
@author: HK
"""
import urllib.error
import time
import os
import urllib.request
import urllib.parse
from PIL import Image
from bs4 import BeautifulSoup
#从得到的图片链接下载图片，并保存
f=open('out.txt','w',encoding='utf-8')

def Handle(file):
    try:
        img = Image.open(file)
        size = img.size
        output_size = ()
        if min(size) < 512:
            os.remove(file)
            ret = 0
        elif size[0] == size[1]:
            output_size = (512, 512)
            ret = 1
        elif size[0] == max(size):
            output_size = (512, 384)
            ret = 1
        else:
            output_size = (384, 512)
            ret = 1
        if ret == 1:
            print(file + "transfoming to ", output_size)
            out = img.resize(output_size, Image.ANTIALIAS)
            out.save(file)
    except Exception as e:
        print(e)
        print("Exception raised, the image is dropped")
        os.remove(file)
        ret = 0
    return ret

def SaveImage(link,InputData,count):
    try:
        time.sleep(0.2)
        urllib.request.urlretrieve(link,'./'+InputData+'/'+str(count)+'.jpg')
        time.sleep(1)
        success = Handle('./'+InputData+'/'+str(count)+'.jpg')
    except urllib.error.HTTPError as urllib_err:
        print(urllib_err)
    except Exception as err:
        time.sleep(1)
        print(err)
        print("产生未知错误，放弃保存")
    else:
        print("已有" + str(count+success-1) + "张图")
#找到图片的链接
def FindLink(PageNum,InputData,word):
    for i in range(PageNum):
        print(i)
        try:
            url = 'http://cn.bing.com/images/async?q={0}&first={1}&count=35&relp=35&lostate=r&mmasync=1&dgState=x*175_y*848_h*199_c*1_i*106_r*0'
            agent = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.165063 Safari/537.36 AppEngine-Google."}
            page1 = urllib.request.Request(url.format(InputData, i*35+1), headers=agent)
            page = urllib.request.urlopen(page1)
            soup = BeautifulSoup(page.read(), 'html.parser')
            print(type(soup))
            print(soup,file=f)
            #print(soup.decode('utf-8'))
            if not os.path.exists("./" + word):
                os.mkdir('./' + word)

            for StepOne in soup.select('.iusc'):
                link = StepOne.attrs['href']
                link='https://cn.bing.com'+link

                parse_result = urllib.parse.urlparse(link)

                lst_query = urllib.parse.parse_qsl(parse_result.query)  # 使用parse_qsl返回列表
                dict1 = dict(lst_query)  # 将返回的列表转换为字典
                mediaurl=dict1.get('mediaurl')

                count = len(os.listdir('./' + word)) + 1
                if count > 400:
                    return
                SaveImage(mediaurl,word,count)
        except Exception as e:
            print(e)

#https://cn.bing.com/images/search?view=detailV2&ccid=GWu4xSvg&id=720A65ED142E68F0C3EA43C5B1D536E423BACD10&thid=OIP.GWu4xSvggKN_5eW48Bn7XQHaF7&mediaurl=http%3a%2f%2fpic5.nipic.com%2f20100128%2f4159633_091147761472_2.jpg&exph=819&expw=1024&q=%e9%93%b6%e8%a1%8c%e5%8d%a1&simid=607996750287472454&selectedIndex=0&ajaxhist=0
#https://cn.bing.com/images/search?view=detailV2&ccid=FyPv4HU3&id=736FAE4071CAF037A359F90E1C9BF1A7C3F31DFF&thid=OIP.FyPv4HU3x3wFbNSMz6KbogHaFC&mediaurl=http%3A%2F%2Fpic.baike.soso.com%2Fp%2F20130621%2F20130621111328-1696794195.jpg&exph=340&expw=500&q=%e9%93%b6%e8%a1%8c%e5%8d%a1&simid=608018560113836225&selectedindex=1&ajaxhist=0&vt=0
if __name__=='__main__':
    #输入需要加载的页数，每页35幅图像
    PageNum = 10000
    #输入需要搜索的关键字
    word=["包子"]
    for w in word:
        InputData=urllib.parse.quote(w)
        FindLink(PageNum,InputData,w)
