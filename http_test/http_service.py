# -*- coding: utf-8 -*-

import socket
import re
import urllib.parse
# import logging
import settings

"""
服务器绑定ip端口并监听,然后等待浏览器客户端访问ip端口连接
连接后获取客户端的请求报文，不同的请求做不同处理
处理完后，返回响应报文给客户端，
一次交互完成，服务器进入阻塞等待下次客户端连接
"""

def service_client(new_socket):
    # 连接后获取请求报文，处理请求
    # 为这个客户端返回数据                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
    # 1.接收浏览器(客户端)发过来的请求，即http请求: GET / HTTP/1.1

    # recv(1024) 接收TCP数据，1024为一次数据接收的大小
    # decode('utf-8') utf-8格式，bytes解码成字符串
    request = new_socket.recv(1024)
    settings.logging.info("格式为：{}".format(type(request)))
    request_decode = request.decode('utf-8') # 收取消息,收到请求头的所有消息
    if request == "":
        return
    request_header_lines = request_decode.splitlines() # 按照行分隔，返回一个包含请求头所有元素的列表

    # 从字符串的开始位置进行匹配,如果起始位置匹配成功,则返回Match对象,否则返回None
    # match匹配完后用正则匹配筛选，只获取'/'和'/'后面的
    # request_header_lines[0] ：获取请求头中的第一条数据'GET /a HTTP/1.1'
    request_header_line = request_header_lines[0]
    ret = re.match(r'[^/]+(/[^ ]*)',request_header_line)

    path_name = "/"

    # 收到客户端请求头数据，取出请求路径'/'并且解码
    if ret:
        # group(1)列出第一个括号匹配部分，取出第一个匹配到的'/'
        path = ret.group(1) # 取出请求中的路径名 # 未解码：/%E4%BD%A0%E5%A5%BD

        # 浏览器请求的路径中带有中文，会被自动编码，需要先解码成中文，才能找到后台中对应的html文件
        path_name = urllib.parse.unquote(path) # 解码后：/你好

        print("请求路径：{}".format(path_name))

    if path_name == "/":  # 用户请求/时，返回当前目录下的index.html页面
        path_name = "/index.html" 
 
    # 2.返回http格式的数据给浏览器
    file_name = "D:/zsh/http_service"+path_name
    try:
        # 路径没错，打开指定路径文件
        f = open(file_name,'rb')

    except:
        # 路径不存在或文件不存在，手动报错，自定义状态码,返回报错信息给客户端
        response = "HTTP/1.1 404 NOT FOUND\r\n" # '\r\n'回车换行
        response += "\r\n"
        # 两个'\r\n' 就多出一个空行
        # 空行代表协议头结束，
        # 后面部分是正文，正文存在，协议头里会加上Content-length:1111标识正文的长度

        # 请求和响应报文格式一样，格式：首行，协议头(请求/响应)，空行，正文
        #   首行：方法(GET/POST)，URL(http://127.0.0.1:8100/)，http版本号(HTTP/1.1)
        #   协议头：键值对结构(Connection:keep-alive长链接)
        #   空行：协议头和正文的分割线，表示协议头结束，协议头里的键值对有多个，没有空行，tcp会出现粘包问题，
        #           可能应该在正文里的出现在协议头里，客户端解析出错
        #   正文：请求正文(post才会有),响应正文:相应的是html，内容就会在正文中

        response += "------file not found------" # 响应正文
        # send() 发送TCP数据，python3发送数据的格式必须是bytes格式
        # encode("utf-8") 指定编码格式编码字符串,默认编码格式为'utf-8'
        new_socket.send(response.encode("utf-8")) # 返回消息
    else:
        html_content = f.read() # 读取文件数据:b'zsh'
        # settings.logger.info(html_content)
        f.close() # 读取完数据后关闭文件

        # 准备发给浏览器的数据 -- header
        # 手动返回正确信息给客户端
        response = "HTTP/1.1 200 OK\r\n"
        response += "\r\n"

        # response += "z"
        # encode("utf-8") 指定编码格式编码字符串,默认编码格式为'utf-8'
        res_encode = response.encode("utf-8")
        
        new_socket.send(res_encode) # utf-8编码后返回消息给客户端
        new_socket.send(html_content) # 从文件读取到的数据就是bytes格式，不需要在重新编码，返回消息
    # 关闭套接字
    new_socket.close()


def main():
    # 用来完成整体的控制
    # 1.创建套接字，
        # family（socket.AF_INET）指明了协议族/域，
            # socket.AF_UNIX 基于文件的，socket.AF_INET 面向网络的
        # type（socket.SOCK_STREAM）是套接口类型，有连接：传输数据可靠，效率低，无连接：追求速度，可能会丢失数据
            # socket.SOCK_STREAM 面向连接的套接字，socket.SOCK_DGRAM 无连接的套接字
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 设置当服务器先close 即服务器端4次挥手之后资源能够立即释放，
    # 这样就保证了，下次运行程序时 可以立即绑定7788端口

    # setsockopt()：socket的格外扩展，用于对socket函数的补充，
    # socket.SOL_SOCKET：基本套接口，要在套接字级别上设置选项，就必须把level设置为 SOL_SOCKET
    # socket.SO_REUSEADDR, 1：允许重用本地地址和端口，value不等于0时就是允许
    tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # 绑定(主机,端口号)""ip为当前主机ip，8100端口 到套接字
    tcp_server_socket.bind(("",8100))
    # 3.变为监听套接字,开始TCP监听
    tcp_server_socket.listen(128) # 参数定义了 sockfd 的挂起连接队列可能增长到的最大长度
    
    # 一直循环，就可以一直建立通信
    while True:
        # 4.等待新客户端的链接，被动接受TCP客户的连接,(阻塞式)等待连接的到来
        # 后面每次交互重复当前操作，交互一次跳到这开始等待客户端连接,
        # 客户端访问服务器监听的端口连接
        new_socket, client_addr = tcp_server_socket.accept()
        print('.......')
        # 5.为这个客户端服务
        service_client(new_socket)
        
    # 关闭监听套接字
    tcp_server_socket.close()
        
if __name__ == '__main__':
    main()
