# -*- coding:utf-8 -*-

# if __name__ == '__main__' 
# 我们简单的理解就是： 
# 如果模块是被直接运行的，则代码块被运行，如果模块是被导入的，则代码块不被运行。

from NameMainTest import PI

def calc_round_area(radius):
    return PI * (radius ** 2)

def main():
    print("round area: ", calc_round_area(2))

main()