import urllib
import urllib.request
import urllib.error
import gzip
import re
import collections
import time
import random
import os
import datetime
class Article(object):#用来存放含有所包含关键词的文章类
    def __init__(self,_title,_url,_count=0):#标题，相对链接，进队列次数
        self.title = _title
        self.url = _url
        self.count = _count
class Modelpage(object):#用来存放目录列表
    def __init__(self,_page,_count=0):
        self.page=_page
        self.count=_count
class Tools(object):#一些常用函數
    def __init__(self,_headers  ):
        self.headers=_headers
        return

    def ungzip(self,data):#解壓頁面
        print('正在解壓頁面')
        try:
            data = gzip.decompress(data)
            print('解壓成功')
            return  data
        except Exception as e:
            e.reason = '解壓失敗'
            raise e


    def decode(self,data,code='gb18030'):#經過搜索得知1024默認的編碼方式是gb18030，雖然頁面上寫的是gb2312，求指導怎樣獲取準確的編碼方式
        print('正在轉碼頁面')
        try:
            data=data.decode(code)
            print('轉碼成功')
            return data
        except Exception as e:
            e.reason = '转码失败'
            raise e

    def get_page_data(self,url,gziped = False,code=''):#默認不需要解壓，不需要解碼
        print('正在获取页面'+ url)
        req = urllib.request.Request(url=url,headers=self.headers)
        try :
            data = urllib.request.urlopen(req).read()
            if gziped:
                data = self.ungzip(data)
            if len(code) >= 1:
                data = self.decode(data,code)
            print('获取成功')
            return data
        except urllib.error.HTTPError as e:
            print('HTTP Error')
            print(e.code)
            print(e.reason)
            return False
        except urllib.error.URLError as e:
            print('URL error')
            print(e.reason)
            return False
        except Exception as e:
            if hasattr(e,'reason'):
                print(e.reason)
            print(e)
            return False

    def get_max_page(self):
         while True:
             max_page = input('请输入最大页码，不要大于99\n')
             try :
                 max_page = int(max_page)
                 if(max_page <= 99):
                     return max_page
             except Exception as e :
                 continue


    def dealtitle(self,title):
        title_re_str = '(<.+?>)'
        title_re = re.compile(title_re_str)
        title =title_re.sub('',title)
        return title

    def sleep(self):
        randtime = random.randint(0,10)
        print('请等待'+str(randtime)+'sec...\n')
        time.sleep(randtime)
    def mkdir(self,path):
        try:
            path = path.strip()+str(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
            print('正在创建目录名为'+path)
            os.mkdir(path)
            return path
        except Exception as e:
            print('创建失败')
            print(e)
    def save(self,url,path,filename):
        try:
            data = self.get_page_data(url)
            f = open(path+'/'+filename,'wb')
            f.write(data)
            f.close()
        except Exception as e:
            print('保存失败')
            print(e)



    class Url(object):
      def __init__(self,_main_url):
        self.main_url =_main_url
        self.index = "index.php"
        self.dagaier_page = "thread0806.php?fid=16"
        self.page_num_url="&search=&page="#后跟页码 非会员貌似只能<100
        return
    class Re(object):#在抓取页面时常用的正则表达式
      def __init__(self):
        # 0 是链接 1是title 使用此re时可能要将标题中的<br>等标签去除 在Tools类中已经写了，欢迎更好地正则表达式！
        self.title_link_re_str = '<tr align="center" class="tr3 t_one"><td><a title=".+?" href="(.+?)" target="_blank">.::</a></td><td style="text-align:left;padding-left:8px" id="">.+?<h3><a href=".+?" target="_blank" id="">(.+?)</a></h3>'
        self.title_link_re = re.compile(self.title_link_re_str,re.S)
        self.title_re_str = '(<.+?>)'
        self.title_re = re.compile(self.title_re_str,re.S)
        # 0 是链接
        self.img_link_re_str = '<input src=\'(.+?)\' type=\'image\' onclick="window.open.+?;return false;">'
        self.img_link_re = re.compile(self.img_link_re_str,re.S)
        #获取图片是jpg，png 还是什么。
        self.file_kind_re_str = '(\.\w{1,4}$)'
        self.file_kind_re = re.compile(self.file_kind_re_str)
if __name__ == '__main__':
    vis = set()
    Modelpage_deque=collections.deque()
    #Modelpage_fail_deque = collections.deque()
    Article_deque=collections.deque()
    #Article_fail_deque = collections.deque()#用来存放一些可能暂时失败的帖子页面
    myheaders={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    main_url = 'http://t66y.com/'
    tools = Tools(myheaders)
    myurl = Tools.Url(main_url)
    myre = Tools.Re()
    max_page = tools.get_max_page()
    pages = [x+1 for x in range(max_page)]
    keyword = input('请输入你感兴趣的关键词，用，隔开 比如 学生，90后 \n').split(',')
    for i in pages:
        tmp_Modelpage= Modelpage(i)
        Modelpage_deque.append(tmp_Modelpage)
    while Modelpage_deque :
        now_Modelpage = Modelpage_deque.popleft()
        now_Modelpage.count += 1
        print('正在搜索第 '+str(now_Modelpage.page)+' 页,是第'+str(now_Modelpage.count)+'次查询')
        now_Modelpage_url = myurl.main_url+myurl.dagaier_page+myurl.page_num_url+str(now_Modelpage.page)
        now_Modelpage_data = tools.get_page_data(now_Modelpage_url,gziped=True,code='gb18030')
        if now_Modelpage_data == False:
            if now_Modelpage.count <= 5:
                Modelpage_deque.append(now_Modelpage)
            continue
        #print(now_Modelpage_data)
        items = re.findall(myre.title_link_re,now_Modelpage_data)
        for item in items:
            link = str(item[0])
            title = str(item[1])

            title = tools.dealtitle(title)
            #print(title)
            for kw in keyword:
                if kw in title:
                    print('找到 '+title+' 已加入队列')
                    tmp_Article = Article(_title=title,_url=link)
                    Article_deque.append(tmp_Article)

        while Article_deque:
            tools.sleep()#防止过快链接
            now_Article = Article_deque.popleft()
            now_Article.count += 1
            print('正在抓取'+now_Article.title)
            now_Article_url = myurl.main_url+now_Article.url
            now_Article_data = tools.get_page_data(now_Article_url,gziped=True,code='gb18030')
            if now_Article_data == False:
                if now_Article.count <= 5:
                    Article_deque.append(now_Article)
                continue
            now_Article_data = str(now_Article_data).split('回覆 [樓主]')
            imgs_url = re.findall(myre.img_link_re,now_Article_data[0])
            path = tools.mkdir(now_Article.title)
            count = 1
            for imgurl in imgs_url:
                imgkind = str(re.findall(myre.file_kind_re,imgurl)[0])
                #print(imgkind)
                print('正在保存第'+str(count)+'张图片')
                filename = str(count)+str(imgkind)
                tools.save(imgurl,str(path),str(filename))
                count += 1
            print('保存完毕')

        tools.sleep()












