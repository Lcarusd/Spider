# -*- coding:utf-8 -*-

# split()：
# 拆分字符串。通过指定分隔符对字符串进行切片，并返回分割后的字符串列表。
# 语法：
# str.split(str="",num=string.count(str))[n]。
# str：
# 表示为分隔符，默认为空格，但是不能为空(' ')。若字符串中没有分隔符，则把整个字符串作为列表的一个元素。
# num：
# 表示分割次数。如果存在参数num，则仅分隔成 num+1 个子字符串，并且每一个子字符串可以赋给新的变量。
# [n]：   
# 表示选取第n个分片。

# 常用实例
u = "www.baidu.com.cn"  
  
#使用默认分隔符  
print(u.split()) 
# ['www.baidu.com.cn']
  
#以"."为分隔符  
print(u.split('.'))
#['www', 'baidu', 'com', 'cn']
  
#分割0次  
print(u.split('.',0))  
# ['www.baidu.com.cn']
  
#分割一次  
print(u.split('.',1))
# ['www', 'baidu.com.cn']
  
#分割两次  
print(u.split('.',2))
# ['www', 'baidu', 'com.cn']
  
#分割两次，并取序列为1的项  
print(u.split('.',2)[1])
# baidu  

#分割最多次（实际上与不加num参数相同）  
print(u.split('.',-1))
# ['www', 'baidu', 'com', 'cn']
  
#分割两次，并把分割后的三个部分保存到三个文件  
u1,u2,u3 = u.split('.',2)  
print(u1)
# www
print(u2) 
# baidu
print(u3)
# com.cn


# 一个很好的demo
str="hello boy<[www.baidu.com]>byebye"  
  
print(str.split("[")[1].split("]")[0]) 
# www.baidu.com 

print(str.split("[")[1].split("]")[0].split(".")) 
# ['www', 'baidu', 'com']  




