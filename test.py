# print('asdfg\nss', end='') # \n换行

# response = "HTTP/1.1 404 NOT FOUND\r\n" # '\r\n'换行
# response += "\r\n"
# response += "------file not found------"
# print(response.encode("utf-8"))

import urllib.parse
path = '%E8%9B%8B%E7%B3%95'
path_name = urllib.parse.unquote(path)
print(path_name)