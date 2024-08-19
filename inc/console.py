#!/usr/bin/env python
# coding=utf-8
  ################
 #   AabyssZG   #
################

from inc import output,run,dockercheck,zoom,fofa,hunter,exemption
import sys

# 控制台-参数处理和程序调用
def Docker_Scan_console(args, proxies, header_new):
    if args.url:
        exemption.Disclaimer()
        urlnew = dockercheck.check(args.url, proxies, header_new)
        run.url(urlnew, proxies, header_new)
    if args.urlfile:
        exemption.Disclaimer()
        run.file(args.urlfile, proxies, header_new)
    if args.dump:
        exemption.Disclaimer()
        urlnew = dockercheck.check(args.dump, proxies, header_new)
        run.dump(urlnew, proxies, header_new)
    if args.zoomeye:
        zoom.ZoomDowload(args.zoomeye,proxies)
    if args.fofa:
        fofa.FofaDowload(args.fofa,proxies)
    if args.hunter:
        hunter.HunterDowload(args.hunter,proxies)
    else:
        output.usage()
        sys.exit()
