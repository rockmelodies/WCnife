from django.shortcuts import render
from django.http import JsonResponse
from django.http import FileResponse
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponsePermanentRedirect
import urllib.parse

from nife.core.SendCode import SendCode
# Create your views here.
# 先把基本功能实现， 一些异常情况在处理


def index(request):
    return render(request, 'nife/index.html')


def login(request):
    if request.method == 'POST':
        url = request.POST.get("url", None)
        pwd = request.POST.get("pwd", None)
    else:

        if request.session.get('url') == None:
            return HttpResponsePermanentRedirect("/")
        else:
            url = request.session.get("url")
            pwd = request.session.get("pwd")

    s = SendCode(url=url, pwd=pwd)
    path = request.session.get("now_path")
    if path == None:
        path = s.getFilePath()
    filelist = s.getFilelist(path)
    filelist = formatsize(filelist)
    path_list = path.split("/")
    if path_list[0] == '':
        path_list[0] = '/'
    # 设置path_sesion 记录用户当前访问的路径
    request.session['now_path'] = path
    request.session['url'] = url
    request.session['pwd'] = pwd
    return render(request, 'nife/html/workbench.html',
                  context={"files": filelist, "path_list": path_list, "url": url, "pwd": pwd})



def getFile(request):
    """
    目录遍历
    :param request:
    :return:
    """
    url = request.session.get("url")
    pwd = request.session.get("pwd")
    path = request.POST.get("path")
    s = SendCode(url=url, pwd=pwd)
    now_path = request.session.get('now_path')
    abspath = now_path.split("/")
    try:
        # 进入上级目录
        index_num = len(abspath) - abspath.index(path)
        for i in range(index_num - 1):
            abspath.pop()
    except ValueError:
        # 进入子目录
        abspath.append(path)
    if path == '/':
        newpath = '/'
        abspath = '/'
    else:
        if abspath[0] == '':
            abspath[0] = '/'
        abspath = [x for x in abspath if x != '']
        newpath = "/".join(abspath)

    # 更新now_path
    request.session['now_path'] = newpath
    filelist = s.getFilelist(newpath)
    filelist = formatsize(filelist)
    return JsonResponse({"files":  filelist, "path_list": abspath, "url": url, "pwd": pwd})


def download(request):
    url = request.session.get("url")
    pwd = request.session.get("pwd")
    s = SendCode(url=url, pwd=pwd)
    filename = request.GET.get('filename')
    filepath = request.session.get('now_path') + '/' + filename
    now_filepath = s.getFile(filename, filepath)
    file = open(now_filepath, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="%s"' % filename
    return response


def deleteFile(request):
    url = request.session.get("url")
    pwd = request.session.get("pwd")
    now_filepath = request.session.get('now_path')
    path = now_filepath.split('/')[-1]
    s = SendCode(url=url, pwd=pwd)
    filename = request.GET.get('filename')
    filepath = now_filepath + '/' +filename
    res = str(s.deleteFile(filepath))
    return JsonResponse({"status": res, 'path': path})


def uploadFile(request):
    if request.method == 'POST':
        url = request.session.get("url")
        pwd = request.session.get("pwd")
        s = SendCode(url=url, pwd=pwd)
        newfile = request.FILES.get("newfile")
        now_filepath = request.session.get('now_path')
        path = now_filepath.split('/')[-1]
        filename = newfile.name
        filepath = now_filepath + "/" + filename
        content = ""
        for chunk in newfile.chunks():
            content = chunk.hex()
        res = s.uploadFile(filepath, content)
        return JsonResponse({"status": res, "path": path})
    else:
        return HttpResponsePermanentRedirect("/")


def renameFile(request):
    pass

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
