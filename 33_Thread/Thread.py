
# Python提供两个模块进行多线程的操作，分别是thread和threading，
# 前者是比较低级的模块，用于更底层的操作，一般应用级别的开发不常用。

import threading
import time

# 创建threading.Thread子类，重写run方法
class MyThread(threading.Thread):
	def run(self):
		for i in range(5):
			print("thread{}, @number:{}".format(self.name, i))
			time.sleep(1)

def main():
	print("Start main threading")
	# 创建三个线程
	threads = [MyThread() for i in range(3)]
	# 启动三个线程
	for t in threads:
		t.start()
		# t.join()
	print("End main threading")

if __name__ == "__main__":
	main()

