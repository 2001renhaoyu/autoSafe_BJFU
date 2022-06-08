import time
import json
from lxml import etree
from requests import session

import execjs


def des(data, firstKey, secondKey, thirdKey):
    with open('des.js', 'r', encoding='UTF-8') as f:
        js_code = f.read()
    context = execjs.compile(js_code)
    return context.call("strEnc", data, firstKey, secondKey, thirdKey)


class BJFU:
    UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 " \
         "Safari/537.36"

    def __init__(self,
                 uid, psw,
                 url_login='https://cas.bjfu.edu.cn/cas/login?service=https%3A%2F%2Fs.bjfu.edu.cn%2Ftp_fp%2Findex.jsp',
                 url_submit='https://s.bjfu.edu.cn/tp_fp/formParser?status=update&formid=7394b770-ba93-4041-91b7'
                            '-80198a68&workflowAction=startProcess&seqId=&unitId=&applyCode=&workitemid=&process'
                            '=bae380db-7db4-4c7c-9458-d79188fa359a'):
        self.session = session()
        self.session.headers['User-Agent'] = self.UA
        self.url_login = url_login
        self.url_submit = url_submit

        self.uid = uid
        self.psw = psw

    def _page_init(self):
        page_login = self.session.get(self.url_login)
        if page_login.status_code == 200:
            return page_login.text
        else:
            self.close()

    def login(self):
        page_login = self._page_init()
        html = etree.HTML(page_login, etree.HTMLParser())

        data = {
            'rsa': '',
            'ul': len(self.uid),
            'pl': len(self.psw),
            'lt': html.xpath("/html/body/form/input[@name='lt']/@value")[0],
            'execution': html.xpath("/html/body/form/input[@name='execution']/@value")[0],
            '_eventId': 'submit'
        }
        data['rsa'] = des(self.uid + self.psw + data['lt'], '1', '2', '3')

        headers = {
            "Host": "cas.bjfu.edu.cn",
            "Origin": "https://cas.bjfu.edu.cn",
            "Referer": self.url_login,
            "User-Agent": self.UA
        }

        post = self.session.post(
            self.url_login,
            data=data,
            headers=headers,
            allow_redirects=False)

        if post.status_code == 302:
            return True
        else:
            self.close()
            return False

    def submit(self):
        with open("jsonData.json", 'r', encoding='UTF-8') as json_file:
            jsonData = json.load(json_file)
            jsonData['body']['dataStores']['298d8761-e06c-455f-ae6d-0beb7639']['rowSet']['primary'][0][
                'JRRQ'] = time.strftime("%Y-%m-%d", time.localtime())

            headers = {
                "Content-Type": "text/plain;charset=UTF-8",
            }

            post = self.session.post(
                self.url_submit,
                data=json.dumps(jsonData),
                headers=headers,
                allow_redirects=True)

        if post.status_code == 200:
            return True
        else:
            self.close()
            return False

    def close(self):
        self.session.close()


bjfu = BJFU("191002309", "07280015")
if not bjfu.login():
    print("登陆失败")

if not bjfu.submit():
    print("提交失败")


