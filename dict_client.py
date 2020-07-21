"""
dict 客户端
发起请求，接收结果，呈现数据
"""

from socket import *
import sys

# 服务端地址
ADDR = ("127.0.0.1",8888)

# 二级界面
def second():
    while True:
        print("""
        ============ Query ================
        1. 查单词    2. 历史记录    3. 注销    
        ===================================
        """)
        cmd = input("请输入命令:")
        if cmd == "1":
            pass
        elif cmd == "2":
            pass
        elif cmd == "3":
            return
        else:
            print("请输入正确命令")

# 发送注册请求
def do_register(sockfd):
    name = input("Name:")
    passwd = input("Password:")
    passwd_ = input("Password again:")

    # 做一些输入的基本验证
    if passwd != passwd_ or " " in name or " " in passwd:
        print("用户名或密码错误")
        return

    msg = "R %s %s"%(name,passwd)
    sockfd.send(msg.encode()) # 发送请求
    # 等结果
    reslut = sockfd.recv(128).decode()
    if reslut == 'OK':
        print("注册成功")

    else:
        print("注册失败")

# 发送登录请求
def do_login(sockfd):
    name = input("Name:")
    passwd = input("Password:")
    msg = "L %s %s" % (name, passwd)
    sockfd.send(msg.encode())  # 发送请求
    # 等结果
    reslut = sockfd.recv(128).decode()
    if reslut == 'OK':
        print("登录成功")
        second() # 进入二级界面
    else:
        print("登录失败")

# 客户端启动函数
def main():
    # tcp套接字
    sockfd = socket()
    sockfd.connect(ADDR)

    # 进入一级界面
    while True:
        print("""
        ============= Welcome ==============
        1. 注册      2. 登录       3. 退出
        ====================================
        """)

        cmd = input("请输入命令:")
        sockfd.send(cmd.encode())
        if cmd == "1":
            do_register(sockfd)
        elif cmd == "2":
            do_login(sockfd)
        elif cmd == "3":
            sockfd.send(b"E")
            sys.exit("谢谢使用")
        else:
            print("请输入正确命令:1,2 or 3")

if __name__ == '__main__':
    main()





