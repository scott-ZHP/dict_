"""
dict 服务端
接收请求，逻辑处理，数据组织，发送响应
"""

from socket import *
from multiprocessing import Process
import signal,sys
from dict_data import *

# 全局变量
HOST = '0.0.0.0'
PORT = 8888
ADDR =  (HOST,PORT) #  服务器地址

# 提前建立数据库连接
db = DataHandle()

# 注册功能
def do_register(connfd,name,passwd):
    if db.register(name,passwd):
        connfd.send(b"OK")
    else:
        connfd.send(b"FAIL")

# 登录功能
def do_login(connfd,name,passwd):
    if db.login(name,passwd):
        connfd.send(b"OK")
    else:
        connfd.send(b"FAIL")

# 处理客户端请求 子进程执行
def do_request(connfd):
    db.create_cursor() # 每个进程创建游标
    # 接受某个客户端的所有请求，分情况处理
    while True:
        data = connfd.recv(1024).decode() # 接受请求
        tmp = data.split(' ')
        if not data or tmp[0] == 'E':
            break
        elif tmp[0] == 'R':
            # tmp--> [R,name,passwd]
            do_register(connfd,tmp[1],tmp[2])
        elif tmp[0] == 'L':
            # tmp--> [L,name,passwd]
            do_login(connfd,tmp[1],tmp[2])

    db.cursor.close()
    connfd.close()

def main():
    # tcp套接字创建
    sock = socket()
    sock.bind(ADDR)
    sock.listen(5)
    print("Listen the port %s"%PORT)
    signal.signal(signal.SIGCHLD,signal.SIG_IGN) # 处理僵尸进程

    # 循环连接客户端
    while True:
        try:
            connfd,addr = sock.accept()
            print("Connect from",addr)
        except KeyboardInterrupt:
            db.close() # 关闭数据库
            sock.close()
            return
        # 为连接进来的客户端创建单独的子进程
        p = Process(target = do_request,args=(connfd,))
        p.daemon = True # 父进程退出，子进程终止服务
        p.start()

if __name__ == '__main__':
    main()