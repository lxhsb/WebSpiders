
import re
import urllib.request
import urllib
from collections import deque

queue = deque()#deque is faster than list
vis = set()#visit

mainUrl = "http://www.yangpig.cn/"

queue.append(mainUrl)
vis.add(mainUrl)
cnt = 0
#using bfs algorithm
while queue:
    nowUrl = queue.popleft()
    cnt += 1

    print("searching:"+ nowUrl)
    open = urllib.request.urlopen(nowUrl)
    if 'htm' not in open.getheader('Content-Type') :#if the file is not htm/html ,cotinue
        continue

    data  = open.read().decode('UTF-8')

    linkre = re.compile('href="(.+?)"')

    for i in linkre.findall(data):
        if mainUrl in i and i not in vis:
             queue.append(i)
             vis.add(i)

print(cnt)#print the number of the pages