# http://codingpy.com/article/python-201-a-tutorial-on-threads/

# Threading 模块从 Python 1.5.2 版开始出现，用于增强底层的多线程模块 thread 。
# 如果你要做的是 CPU 密集型操作，那么你需要使用 Python 的 multiprocessing 模块。

import threading

# 可以被多线程使用的一个函数
def double(number):
	# 打印出调用这个函数的线程的名称，并在最后打印一行空行
	print(threading.currentThread().getName() + "\n")
	print(number * 2)
	print()


if __name__ == "__main__":
	# 创建五个线程并且依次启动它们
	for i in range(5):
		my_thread = threading.Thread(target=double, args=(i,))
		my_thread.start()