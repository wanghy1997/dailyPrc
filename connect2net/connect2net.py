"""
@author yutanglee
@description 这个代码可以免浏览器拨号上网，原理很简单，就是给认证服务器发送一个http请求。
@use 你需要提供上网账号、密码和运营商，是否采用手机端或者PC端是可选的。手机端和PC端是指，重邮的每个上网账号可以同时存在一个PC账号和手机端。
"""
from ast import arg
from pydoc import describe
import requests
import subprocess
import re
import argparse
import base64


def login(usr, psw, isp, ip, mobile=True):
    
    url = 'http://192.168.200.2:801/eportal/?c=Portal&a=login&callback=dr1003&login_method=1&' +\
        'user_account=%2C0%2C' + usr + '%40' + isp +'&user_password=' + psw + '&wlan_user_ip=' + ip + \
        '&wlan_user_ipv6=&wlan_user_mac=000000000000&wlan_ac_ip=&wlan_ac_name=&jsVersion=3.3.3&v=10390'
    if not mobile:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.58'}
    else:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36 Edg/114.0.1823.58'}
    r = requests.get(url=url, headers=headers)
    return r.text

def get_local_ip():
    try:
        # 运行 ip a 命令获取网络接口信息
        output = subprocess.check_output(["ip", "a"]).decode("utf-8")
        
        # 使用正则表达式解析 IP 地址
        ip_pattern = r"inet (\d+\.\d+\.\d+\.\d+)"
        match = re.findall(ip_pattern, output)
        
        # 筛选出以特定 IP 段开头的 IP 地址
        target_ips = [ip for ip in match if ip.startswith("10.16.") or ip.startswith("10.20.")]
        
        if target_ips:
            return target_ips[0]  # 返回第一个满足条件的 IP 地址
        else:
            return None
    except subprocess.CalledProcessError:
        return None

    
if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--user', type=str, default='3222615', help='your account for CQUPT network, maybe is your id number login ehall.cqupt.edu.cn')
    args.add_argument('--psw', type=str, default='CScqupt6267', help='password')
    args.add_argument('--isp', type=str, default='cmcc', help='cmcc|telecom|unicom|xyw')
    args.add_argument('--mobile', action='store_true', help='do you want use mobile mode?')
    args = args.parse_args()
    
    if args.isp != 'cmcc' and args.isp != 'telecom' and args.isp != 'unicom' and args.isp != 'xyw':
        print('运营商只支持cmcc|telecom|unicom|xyw  重新检查输入！')
        exit(1)

    ip = get_local_ip()
    if ip is None:
        ip = input("自动获取IP失败, 请你输入正确的IP: ")
    print('your ip is:', ip)
    print('your user is:', args.user)
    print('your password is:', args.psw)    
    print('your isp is:', args.isp)
    args.mobile = True

    response = login(args.user, args.psw, args.isp, ip, args.mobile)
    start_index = response.find('"result":"') + len('"result":"')
    end_index = response.find('"', start_index)
    result_value = response[start_index:end_index]
    if result_value == '1':
        print('登录成功！')
    else:
        start_index = response.find('"msg":"') + len('"msg":"')
        end_index = response.find('"', start_index)
        msg_encoded = response[start_index:end_index]
        # 对msg进行Base64解码
        msg_decoded = base64.b64decode(msg_encoded).decode('utf-8')

        print(msg_decoded, response)
        if msg_decoded == 'ldap auth error':
            print('密码错误！')
        elif msg_decoded == 'userid error1':
            print('账号不存在！')