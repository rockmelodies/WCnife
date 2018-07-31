from django.shortcuts import render
from django.http import JsonResponse
from nife.core.SendCode import SendCode
# Create your views here.
# 先把基本功能实现， 一些异常情况在处理


def index(request):

    return render(request, 'nife/index.html')


def login(request):
    url = request.POST.get("url")
    pwd = request.POST.get("pwd")
    s = SendCode(url=url, pwd=pwd)
    path = s.getFilePath()
    filelist = s.getFilelist(path)
    filelist = formatsize(filelist)
    path_list = path.split("/")
    return render(request, 'nife/html/workbench.html', context={"files":  filelist, "path_list": path_list, "url": url, "pwd": pwd})

def getFile(request):
    url = request.POST.get("url")
    pwd = request.POST.get("pwd")
    path = request.POST.get("path")
    s = SendCode(url=url, pwd=pwd)
    abspath = s.getFilePath().split("/")
    index_num = len(abspath) - abspath.index(path)
    for i in range(index_num - 1):
        abspath.pop()
    newpath = "/".join(abspath)
    filelist = s.getFilelist(newpath)
    filelist = formatsize(filelist)
    return JsonResponse({"files":  filelist, "path_list": abspath, "url": url, "pwd": pwd})


def formatsize(filelist):
    KB = 1024
    MB = KB*1024
    GB = MB*1024
    for f in filelist:
        if f['size'] <= KB:
            f['size'] = str(f['size']) + "B"
        elif f['size'] <= MB:
            f['size'] = str(f['size']//KB) + "KB"
        elif f['size'] <= GB:
            f['size'] = str(f['size']//MB) + "M"
        else:
            f['size'] = str(f['size']//GB) + "G"
    return filelist
