# -*- coding:utf-8 -*-

import re


print("==============re.match函数==============")
# 描述：
# 从字符串的起始位置匹配一个模式。
# 如果不是起始位置匹配成功的话，match()则返回none。
# 语法：
# re.match(pattern, string, flags=0) 
# pattern	：匹配的正则表达式。
# string	：要匹配的字符串。
# flags	：标志位，用于控制正则表达式的匹配方式，如：是否区分大小写，多行匹配等等。
# 说明：匹配成功re.match方法返回一个匹配的对象，否则返回None。

print(re.match('www', 'www.runoob.com').span())  # 在起始位置匹配 
print(re.match('com', 'www.runoob.com'))         # 不在起始位置匹配

line = "Cats are smarter than dogs"  
matchObj = re.match( r'(.*) are (.*?) .*', line, re.M|re.I)  
if matchObj:  
   print("matchObj.group() : ", matchObj.group())
   print("matchObj.group(1) : ", matchObj.group(1))
   print("matchObj.group(2) : ", matchObj.group(2))  
else:  
   print("No match!!")


print("==============re.search函数==============")
# 描述:
# 匹配并提取第一个符合规律的内容，返回一个正则表达式对象object；
# 语法:
# re.search(pattern, string, flags=0)

print(re.search('www', 'www.runoob.com').span())         # 在起始位置匹配  
print(re.search('com', 'www.runoob.com').span())         # 不在起始位置匹配 

line = "Cats are smarter than dogs";  
searchObj = re.search( r'(.*) are (.*?) .*', line, re.M|re.I)  
if searchObj:  
   print("searchObj.group() : ", searchObj.group())   # obj.group()的值是整个字符串  
   print("searchObj.group(1) : ", searchObj.group(1)) # obj.group(1)的值是第一个匹配字符串，这里是(.*)匹配的字符串  
   print("searchObj.group(2) : ", searchObj.group(2)) # obj.group(2)的值是第二个匹配字符串，这里是(.*?)匹配的字符串  
else:  
   print("Nothing found!!")  


print("==============re.match与re.search的区别==============")
# re.match只匹配字符串的开始，如果字符串开始不符合正则表达式，则匹配失败，函数返回None；
# re.search匹配整个字符串，直到找到一个匹配。
line = "Cats are smarter than dogs";  
matchObj = re.match( r'dogs', line, re.M|re.I)  
if matchObj:  
   print("match --> matchObj.group() : ", matchObj.group())
else:  
   print("No match!!")  
matchObj = re.search( r'dogs', line, re.M|re.I)  
if matchObj:  
   print("search --> matchObj.group() : ", matchObj.group())
else:  
   print("No match!!") 


print("==============检索和替换==============")
# 描述:
# re.sub替换符合规律的内容，返回替换后的值；
# 语法:
# re.sub(pattern, repl, string, max=0)
print("re.sub方法：")
phone = "2004-959-559 # This is Phone Number"  
                                          
num = re.sub(r'#.*$', "", phone)  
print("Phone Num : ", num) 
                                       
num = re.sub(r'\D', "", phone)      
print("Phone Num : ", num)

#sub的使用举例  
s = '123rrrrr123'  
output = re.sub('123(.*?)123','123%d123'%789,s)  
print(output)    # 输出：123789123  

print("re.findall方法：")
# 描述:
# 匹配所有符合规律的内容，返回包含结果的列表。


print("==============对比findall与search的区别==============")
s2 = 'asdfxxIxx123xxlovexxdfd'  
  
f1 = re.search('xx(.*?)xx123xx(.*?)xx',s2).group()  
print(f1)   #输出：xxIxx123xxlovexx  
f2 = re.search('xx(.*?)xx123xx(.*?)xx',s2).group(1)  
print(f2)   #输出：I  
f3 = re.search('xx(.*?)xx123xx(.*?)xx',s2).group(2)  
print(f3)   #输出：love  
  
f2 = re.findall('xx(.*?)xx123xx(.*?)xx',s2)  
print(f2)         # 输出：[('I', 'love')]  
print(f2[0])      # 输出：('I', 'love')  
print(f2[0][0])   # 输出：I  
print(f2[0][1])   # 输出：love


print("==============正则表达式修饰符——可选标志==============")
# re.I	使匹配对大小写不敏感
# re.L	做本地化识别（locale-aware）匹配
# re.M	多行匹配，影响 ^ 和 $
# re.S	使 . 匹配包括换行符在内的所有字符
# re.U	根据Unicode字符集解析字符。这个标志影响 \w, \W, \b, \B.
# re.X	该标志通过给予你更灵活的格式以便你将正则表达式写得更易于理解。
# 如：re.I | re.M 被设置成 I 和 M 标志

# re.S匹配包含换行符的字符  
s = '''''sdfxxhello 
xxfsdfxxworldxxasdf'''  
d2=re.findall('xx(.*?)xx',s)  
print(d2)   # 输出：['fsdf']  
d1 = re.findall('xx(.*?)xx',s,re.S)  
print(d1)   #输出：['hello\n', 'world'] 


print("==============正则表达式模式中匹配及实例==============")
# 下面列出了正则表达式模式语法中的特殊元素:
# .		匹配任意字符，换行符\n除外
# *		匹配前一个字符0次或无限次
# ?		匹配前一个字符0次或1次
# .*	贪心算法（提取最多的内容）
# .*?	非贪心算法（少量多餐）
# ()	括号内的数据作为结果返回

# . 的使用举例  
a = 'xy123'  
b = re.findall('x..',a)  
print(b)      # 输出：['xy1']  
  
# * 的使用举例  
a = 'xxyxy123'  
b = re.findall('x*',a)  
print(b)      # 输出：['xx', '', 'x', '', '', '', '', '']  
  
# ? 的使用举例  
a = 'xyxx123'  
b = re.findall('x?',a)  
print(b)      # 输出：['x', '', 'x', 'x', '', '', '', '']  

secret_code = 'xxIxxfasdjifja134xxlovexx23345sdfxxyouxx'
# .* 的使用举例  
b = re.findall('xx.*xx',secret_code)  
print(b)   # 输出：['xxIxxfasdjifja134xxlovexx23345sdfxxyouxx']  
# .*? 的使用举例  
c = re.findall('xx.*?xx',secret_code)  
print(c)   # 输出：['xxIxx', 'xxlovexx', 'xxyouxx']

# 使用括号与不使用括号的差别(括号内容将作为结果返回)
d1 = re.findall('xx.*?xx',secret_code)  
print(d1)   # 输出：['xxIxx', 'xxlovexx', 'xxyouxx']  
d2 = re.findall('xx(.*?)xx',secret_code)  
print(d2)   # 输出：['I', 'love', 'you']


print("==============正则表达式模式==============")
'''
	^				匹配字符串的开头
	$				匹配字符串的末尾。
	.				匹配任意字符，除了换行符，当re.DOTALL标记被指定时，则可以匹配包括换行符的任意字符。
	[...]			用来表示一组字符,单独列出：[amk] 匹配 'a'，'m'或'k'
	[^...]			不在[]中的字符：[^abc] 匹配除了a,b,c之外的字符。
	re*				匹配0个或多个的表达式。
	re+				匹配1个或多个的表达式。
	re?				匹配0个或1个由前面的正则表达式定义的片段，非贪婪方式
	re{ n}	 
	re{ n,}			精确匹配n个前面表达式。
	re{ n, m}		匹配 n 到 m 次由前面的正则表达式定义的片段，贪婪方式
	a| b			匹配a或b
	(re)			G匹配括号内的表达式，也表示一个组
	(?imx)			正则表达式包含三种可选标志：i, m, 或 x 。只影响括号中的区域。
	(?-imx)			正则表达式关闭 i, m, 或 x 可选标志。只影响括号中的区域。
	(?: re)			类似 (...), 但是不表示一个组
	(?imx: re)		在括号中使用i, m, 或 x 可选标志
	(?-imx: re)		在括号中不使用i, m, 或 x 可选标志
	(?#...)			注释.
	(?= re)			前向肯定界定符。如果所含正则表达式，以 ... 表示，在当前位置成功匹配时成功，否则失败。
					但一旦所含表达式已经尝试，匹配引擎根本没有提高；模式的剩余部分还要尝试界定符的右边。
	(?! re)			前向否定界定符。与肯定界定符相反；当所含表达式不能在字符串当前位置匹配时成功
	(?> re)			匹配的独立模式，省去回溯。
	\w				匹配字母数字
	\W				匹配非字母数字
	\s				匹配任意空白字符，等价于 [\t\n\r\f].
	\S				匹配任意非空字符
	\d				匹配任意数字，等价于 [0-9].
	\D				匹配任意非数字
	\A				匹配字符串开始
	\Z				匹配字符串结束，如果是存在换行，只匹配到换行前的结束字符串。c
	\z				匹配字符串结束
	\G				匹配最后匹配完成的位置。
	\b				匹配一个单词边界，也就是指单词和空格间的位置。
					例如， 'er\b' 可以匹配"never" 中的 'er'，但不能匹配 "verb" 中的 'er'。
	\B				匹配非单词边界。'er\B' 能匹配 "verb" 中的 'er'，但不能匹配 "never" 中的 'er'。
	\n, \t, 等.		匹配一个换行符。匹配一个制表符。等
	\1...\9			匹配第n个分组的子表达式。
	\10				匹配第n个分组的子表达式，如果它经匹配。否则指的是八进制字符码的表达式。
'''

# 字符匹配
# python	匹配 "python".

# 字符类
# [Pp]ython	匹配 "Python" 或 "python"
# rub[ye]		匹配 "ruby" 或 "rube"
# [aeiou]		匹配中括号内的任意一个字母
# [0-9]		匹配任何数字。类似于 [0123456789]
# [a-z]		匹配任何小写字母
# [A-Z]		匹配任何大写字母
# [a-zA-Z0-9]	匹配任何字母及数字
# [^aeiou]	除了aeiou字母以外的所有字符
# [^0-9]		匹配除了数字外的字符

# 特殊字符类
# .	匹配除 "\n" 之外的任何单个字符。要匹配包括 '\n' 在内的任何字符，请使用象 '[.\n]' 的模式。
# \d	匹配一个数字字符。等价于 [0-9]。
# \D	匹配一个非数字字符。等价于 [^0-9]。
# \s	匹配任何空白字符，包括空格、制表符、换页符等等。等价于 [ \f\n\r\t\v]。
# \S	匹配任何非空白字符。等价于 [^ \f\n\r\t\v]。
# \w	匹配包括下划线的任何单词字符。等价于'[A-Za-z0-9_]'。
# \W	匹配任何非单词字符。等价于 '[^A-Za-z0-9_]'。









