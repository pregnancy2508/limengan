#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import json
import time
import random
import atexit
import argparse
import urllib.request
from urllib.parse import urlsplit, urlunsplit

API_URL = 'https://hk4e-launcher-static.hoyoverse.com/hk4e_global/mdk/launcher/api/resource?launcher_id=10&key=gcStgarh&channel_id=1&sub_channel_id=3'

def scan_urls(dic):
    urls = []
    # 跳过小于1GiB的包
    if 'package_size' in dic and int(dic['package_size']) < 2**30:
        return urls
    for key, value in dic.items():
        if key == 'path' and value.startswith('http'):
            urls.append(value)
        elif isinstance(value, dict):
            urls.extend(scan_urls(value))
        elif isinstance(value, list):
            for v in value:
                if isinstance(v, dict):
                    urls.extend(scan_urls(v))
    return urls

def get_download_url():
    r = urllib.request.urlopen(API_URL)
    data = json.loads(r.read())
    urls = scan_urls(data['data']['game'])
    return random.choice(urls)

def clean():
    try:
        os.remove('trash')
        os.remove('trash.aria2')
    except:
        pass

def main(cdn_ip, speed):
    while True:
        url = get_download_url()
        try:
            url = get_download_url()
        except:
            url = 'https://autopatchhk.yuanshen.com/client_app/download/pc_zip/20230804185804_eTmE8EZjJZdAJapq/GenshinImpact_4.0.0.zip.001'
        new_url = urlunsplit(['http', cdn_ip] + list(urlsplit(url))[2:])
        print('Download: ' + new_url)
        clean()
        cmd = f'aria2c -o trash --allow-overwrite=true --auto-file-renaming=false --summary-interval=0 --file-allocation=none --header="Host: autopatchhk.yuanshen.com" --max-download-limit={speed}M {new_url}'
        os.system(cmd)
        time.sleep(1)

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    parser = argparse.ArgumentParser(description="SB X mengan")
    parser.add_argument("--ip", "-i", type=str, default="163.171.129.138", help="指定要使用的CDN的IP地址")
    parser.add_argument("speed", type=int, nargs='?', default=8, help="下载限速（整数，单位M）")
    if len(sys.argv) <= 1:
        opt = input("请设置下载限速等信息（整数，单位为M，留空直接以默认值8开始下载）") or '8'
        ls = opt.split()
    else:
        ls = sys.argv[1:]
    args = parser.parse_args(ls)

    atexit.register(clean)
    print('即将开始下载，下载过程中你可以随时按 Ctrl+C 停止\n')
    try:
        main(args.ip, args.speed)
    except KeyboardInterrupt:
        print('已停止下载')
