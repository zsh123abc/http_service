#file_send.py 
import socket,os 
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
# 获取当前脚本的完整路径
print(BASE_DIR)

# 创建套接字
sk = socket.socket() 
address = ('127.0.0.1',8001)

# 客户端主动连接连接指定ip，端口
sk.connect(address)

# 键盘输入要上传文件的名字
filename = input("please input filename:") 
# 拼接路径，中间会自动加上'/'
path = os.path.join(BASE_DIR,filename) 
# os.stat是将文件的相关属性读出来
os_stat = os.stat(path)
# 获取文件的大小
filesize = os_stat.st_size
# 文件名和文件大小拼接，中间| 隔开
fileinfo = '%s|%s'%(filename,str(filesize)) 
# 发送完整的TCP数据，send发送可能需要多次,发送文件名，文件大小
# 第一次发送数据给服务端，文件名和文件大小
sk.sendall(bytes(fileinfo,'utf8'))
# 打开指定目录文件
f = open(path,'rb')
has_sent = 0

# 读取打开文件的1024个字节的数据
data = f.read(1024) 
# 第二次发送数据给服务端，将读取的文件内容发送
sk.sendall(data) 

print('well done!') 
# 关闭文件
f.close() 
# 关闭套接字
sk.close()