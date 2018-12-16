# -*- coding:utf-8 -*-

text = "I'm a hand some boy!"

frequency = {}

for word in text.split():
    if word not in frequency:
        frequency[word] = 1
    else:
        frequency[word] += 1