#!/usr/bin/env python
# coding=utf-8
  ################
 #   AabyssZG   #
################

from inc import output,run,console
import requests, sys, hashlib, json
from termcolor import cprint
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
outtime = 10

def Docker_Check(url,proxies,header_new):
    cprint("[.] 正在进行Docker的指纹识别","cyan")
    path = "version"
    check_status = 0
    test_url = str(url) + path
    r = requests.get(test_url, verify=False, timeout = outtime, headers=header_new, proxies=proxies)
    try:
        if ('GitCommit' in r.text) and ('Version' in r.text):
            containers = r.json()
            ver = containers['Version']
            cprint("[+] 站点指纹符合Docker特征，版本号为" + ver,"red")
            check_status = 1
        while check_status == 0:
            cprint("[-] 站点指纹不符合Docker特征，可能不是Docker框架","yellow")
            break
    except KeyboardInterrupt:
        print("Ctrl + C 手动终止了进程")
        sys.exit()
    except Exception as e:
        print("[-] 发生错误，已记入日志error.log\n")
        f2 = open("error.log", "a")
        f2.write(str(e) + '\n')
        f2.close()

def check(url,proxies,header_new):
    header_new = json.loads(header_new)
    if ('://' not in url):
        url = str("http://") + str(url)
    if str(url[-1]) != "/":
        url = url + "/"
    try:
        requests.packages.urllib3.disable_warnings()
        r = requests.get(url, verify=False, timeout = outtime, headers=header_new, proxies=proxies)
        if r.status_code == 503:
            sys.exit()
        else:
            Docker_Check(url,proxies,header_new)
            return url
    except KeyboardInterrupt:
        print("Ctrl + C 手动终止了进程")
        sys.exit()
    except Exception as e:
        cprint("[-] URL为 " + url + " 的目标积极拒绝请求，予以跳过！已记入日志error.log", "magenta")
        f2 = open("error.log", "a")
        f2.write(str(e) + '\n')
        f2.close()
        sys.exit()
