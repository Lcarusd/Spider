# -*- coding:utf-8 -*-

# if __name__ == '__main__' 
# 我们简单的理解就是： 
# 如果模块是被直接运行的，则代码块被运行，如果模块是被导入的，则代码块不被运行。

PI = 3.14

def main():
    print("PI:", PI)

if __name__ == "__main__":
    main()
