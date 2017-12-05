# http://www.runoob.com/python/python-multithreading.html

import thread
import time

# 为线程定义一个函数
def print_time(threadName, delay):
	count = 0
	while count < 5:
		time.sleep(delay)
		count += 1
		print("%s: %s" % (threadName, time.ctime(time.time())))

# 创建两个线程 
try:
	thread.start_new_thread(print_time, ("thread-1", 2))
	thread.start_new_thread(print_time, ("thread-2", 4))
except:
	print("Error: unable to start thread")

while 1:
	pass