#file_receive.py 
import socket,subprocess,os 

# 获取当前脚本的完整路径
# 'd:\\zsh\\python\\http_service\\file'
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
# 创建套接字
sk = socket.socket() 
address = ('127.0.0.1',8001) 
# 绑定ip，端口
sk.bind(address) 
# TCP监听，最大连接数3
sk.listen(3) 
# 等待客户端连接
conn,addr = sk.accept() 
# 客户端多次发送数据，服务端就可以多次获取数据
# 第一次获取客户端请求数据,bytes格式的文件名和文件大小
fileinfo = conn.recv(1024) 

filename,filesize = str(fileinfo,'utf8').split('|') 

# os.makedirs(filename)
# 拼接路径，中间会自动加上'/'
# D:\zsh\python\http_service\file_recv\t.txt
# d:\\zsh\\python\\http_service\\file\\file_recv\\t.txt
path = os.path.join(BASE_DIR,filename)
# 根据路径打开文件
f = open(path,'wb')
# 第二次获取客户端发送的数据，bytes格式的文件内容b'zzzzzzz'
data = conn.recv(1024)
# 从客户端获取的文件写入数据至文件
f.write(data)

# 关闭文件
f.close() 
print('well done')
# 关闭套接字 
sk.close()