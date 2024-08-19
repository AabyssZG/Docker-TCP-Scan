#!/usr/bin/env python
# coding=utf-8
  ################
 #   AabyssZG   #
################

from inc import output,run,dockercheck,zoom,fofa,hunter
import sys
from termcolor import cprint

# 免责声明
def Disclaimer():
    print('''
免责声明：
1.如果您下载、安装、使用、修改本工具及相关代码，即表明您信任本工具
2.在使用本工具时造成对您自己或他人任何形式的损失和伤害，我们不承担任何责任
3.如您在使用本工具的过程中存在任何非法行为，您需自行承担相应后果，我们将不承担任何法律及连带责任
4.请您务必审慎阅读、充分理解各条款内容，特别是免除或者限制责任的条款，并选择接受或不接受
5.除非您已阅读并接受本协议所有条款，否则您无权下载、安装或使用本工具
6.您的下载、安装、使用等行为即视为您已阅读并同意上述协议的约束''')
    ExeCheck = input("是否同意接受该免责声明的所有内容（Y/N）: ")
    if (ExeCheck != "Y" and ExeCheck != "y"):
        cprint("[-] 您没有同意该免责协定的所有内容，程序自动结束！", "yellow")
        sys.exit()
