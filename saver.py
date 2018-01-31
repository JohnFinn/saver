#!/usr/bin/python3

# когда пишешь что нибудь, что выполняется медленно,
# для того чтобы запускать програму несколько раз подряд,
# и не ждать каждый раз, можно сохранять результат

# цель - написать декоратор, сохраняющий возвращенный функцией результат, в файл
# и при следующем вызове брать результат из файла
# также нужно придумать механизм обнуления результата

import inspect
import pickle
import os

def saver(filename):
	def wrapper(func):
		return Saver(func, filename)
	return wrapper

class Saver:
	# saves result of wrapped function from previous program run for set of
	# *args, **kwargs
	# if function code was changed, results are calculated again
	# assumes that function will return same value for same arguments
	# assumes that file will be untouched

	def __init__(self, func, filename):
		self.func = func
		self.filename = filename
		# if source changed remove file
		if os.path.isfile(filename):
			with open(filename, 'rb') as file:
				content = pickle.load(file) # maybe need to add 'try-except' here
			source, values = content
			if source != inspect.getsource(self.func):
				os.remove(self.filename)

	def __call__(self, *args, **kwargs):
		key = args, pickle.dumps(kwargs) # dict can't be dict's key so I decided to serialize it with pickle
		if os.path.isfile(self.filename):
			with open(self.filename, 'rb') as file:
				source, results = pickle.load(file)
			if key not in results:
				results[key] = self.func(*args, **kwargs)
			result = results[key]
			with open(self.filename, 'wb') as file:
				pickle.dump((source, results), file)
		else:
			result = self.func(*args, **kwargs)
			with open(self.filename, 'wb') as file:
				pickle.dump((inspect.getsource(self.func), {key:result}), file)
		return result

@saver('some_file')
def foo(number):
	import time
	time.sleep(4)

	return number

print(foo(10))
print(foo(20))
