import requests
import json
from ids_encrypt import encryptAES
from bs4 import BeautifulSoup


# 登录信息门户，返回登录后的session
def login(user_name, password):
    session = requests.Session() #session会话对象用于跨请求保持请求的参数。
    form = {"username": user_name}
    url = "https://newids.seu.edu.cn/authserver/login?goto=http://my.seu.edu.cn/index.portal"
    #  获取登录页面表单，解析隐藏值
    res = session.get(url) #先进行一次登录请求以获取登录表单
    soup = BeautifulSoup(res.text, 'html.parser') #获得网页源码
    attrs = soup.select('[tabid="01"] input[type="hidden"]')  #获取隐藏属性
    for k in attrs:
        if k.has_attr('name'):
            form[k['name']] = k['value']
        elif k.has_attr('id'):
            form[k['id']] = k['value']
    ##获取的form
    # {'username': 'username',
    #  'lt': 'LT-2571339-0RheEaOfeJ3IjCivf1NKRfarBc9fKz1639120490746-0Dan-cas',
    #  'dllt': 'userNamePasswordLogin',
    #  'execution': 'e1s1',
    #  '_eventId': 'submit',
    #  'rmShown': '1',
    #  'pwdDefaultEncryptSalt': 'zUscTwqgPeEgDJol'}
    form['password'] = encryptAES(password, form['pwdDefaultEncryptSalt']) #已经从form中获取加密形式，通过encryptAES进行特定格式的加密
    # 登录认证
    session.post(url, data=form, allow_redirects=False)
    # 登录ehall
    session.get('http://ehall.seu.edu.cn/login?service=http://ehall.seu.edu.cn/new/index.html')
    #获取个人信息
    res = session.get('http://ehall.seu.edu.cn/jsonp/userDesktopInfo.json')
    json_res = json.loads(res.text)
    try:
        name = json_res["userName"]
        print(f"小{name[0]}同学登陆成功！\n")
    except Exception:
        print("认证失败！")
        return False

    return session

def logging():
    print("请输入帐号:")
    user_name = input()
    print("请输入密码:")
    password = input()
    print("开始登陆")
    session = login(user_name, password)
    while session is False or session is None:
        print("请重新登陆")
        print("请输入帐号:")
        user_name = input()
        print("请输入密码:")
        password = input()
        print("开始登陆")
        session = login(user_name, password)
    return session