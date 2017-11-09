# -*- coding: utf-8 -*-  
  
#====================  
#File: FormatTest.py 
#Author: Lcarusd 
#Date: 2017-07-15

# format()
# 格式化字符串函数
# 语法
# 它通过{}和:来代替%
# 使用方法：
# 通过映射：位置、关键字、对象、下标
# 使用格式限定符：语法是{}中带:号
# ^、<、>分别是居中、左对齐、右对齐，后面带宽度
#====================  
  
age = 22
name = 'Lcarusd'  
  
print('{0} is {1} years old. '.format(name, age)) #输出参数
#  Lcarusd is 22 years old. 

print('{0} is a girl. '.format(name))  
# Lcarusd is a girl. 

print('{0:.3} is a decimal. '.format(1/3)) #小数点后三位
# 0.333 is a decimal.

print('{0:_>11} is a 11 length. '.format(name)) #使用_补齐空位
# __Lcarusd__ is a 11 length.

print('{first} is as {second}. '.format(first=name, second='Wendy')) #别名替换
# Lcarusd is as Wendy. 

print('My name is {0.name}'.format(open('out.txt', 'w'))) #调用方法
# My name is out.txt

print('My name is {0:^8}.'.format('Fred')) #指定宽度
# My name is   Fred  .

print("通过位置:")
print('{0},{1}'.format('kzc',18))
print('{},{}'.format('kzc',18))
print('{1},{0},{1}'.format('kzc',18))

print("通过下标:")
p=['kzc',18]
print('{0[0]},{0[1]}'.format(p))

print("格式限定符:")
print('{:>8}'.format('189')) # 左对齐，8个字符空间
# '    189'
print('{:0<8}'.format('189')) # 右对齐，8个字符空间，使用0填充
# '18900000'
print('{:_^8}'.format('189')) # 中间对齐，8个字符空间，使用_填充
# '__189___'

print("精度与类型f:")
print('{:.2f}'.format(321.33345))
# '321.33'

print("各种进制类型:")
print('{:b}'.format(17))	# 二进制
# '10001'
print('{:d}'.format(17)) # 十进制
# '17'
print('{:o}'.format(17)) # 八进制
# '21'
print('{:x}'.format(17)) # 十六进制
# '11'







