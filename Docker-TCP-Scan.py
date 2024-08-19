#!/usr/bin/env python
# coding=utf-8
  ################
 #   AabyssZG   #
################

from inc import output, console, run ,proxycheck
import argparse, sys, time

def get_parser():
    parser = argparse.ArgumentParser(usage='python3 Docker-TCP-Scan.py',description='Docker-TCP-Scan: 针对Docker的TCP Socket开源渗透框架',)
    p = parser.add_argument_group('SpringBoot-Scan 的参数')
    p.add_argument("-u", "--url", type=str, help="对单一URL进行Docker端点探测")
    p.add_argument("-uf", "--urlfile", type=str, help="读取目标TXT进行Docker端点探测")
    p.add_argument("-d", "--dump", type=str, help="下载指定Docker端点的容器日志（可提取敏感信息）")
    p.add_argument("-p", "--proxy", type=str, default='', help="使用HTTP代理")
    p.add_argument("-z", "--zoomeye", type=str, default='', help="使用ZoomEye导出Docker框架资产")
    p.add_argument("-f", "--fofa", type=str, default='', help="使用Fofa导出Docker框架资产")
    p.add_argument("-y", "--hunter", type=str, default='', help="使用Hunter导出Docker框架资产")
    p.add_argument("-t", "--newheader", type=str, help="从TXT文件中导入自定义HTTP头部")
    args = parser.parse_args()
    return args

def main():
    output.logo()
    args = get_parser()
    proxycheck.Docker_Scan_Proxy(args)

if __name__ == '__main__':
    main()
