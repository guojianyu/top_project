#代理池使用代码
import requests
def change_proxy():
    content = {'ali_user': 'root','ali_pwd':'FAJN%v1*dKjW1o4Z','ali_ip':"39.106.218.107",'ali_port':22,
                'vpn_user':'5533','vpn_pwd':'123',
               'region':'henan'
               }
    #region:区域
    r=requests.post('http://192.168.1.163:8000/Back_manager/change_proxy',data=content)
    return r


def get_ip_info(ip_dd):#如果使用的公用通道则只需要将ali的固定ip作为代理即可
    ip = 'ip'
    address = 'address'
    proxies = {'http': 'http://%s:8080' % ip_dd, 'https': 'https://%s:8080' % ip_dd}
    r = requests.get('http://ip.chinaz.com/getip.aspx', proxies=proxies)
    get = r.text
    get = eval(get)
    return get
if  __name__ == '__main__':
    ret = change_proxy()
    ali_ip = "39.106.218.107"
    ip_info = get_ip_info(ali_ip)
    print (ip_info)