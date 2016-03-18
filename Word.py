# coding: utf-8

class Word (object):
	def __init__(self, word, meaning, err_times):
		self.word = word
		self.meaning = meaning
		self.err_times = err_times
		
	def add_err_times(self, times=1):
		self.err_times += times
	
	def __str__(self):
		return '%d %s %s' % (self.err_times, self.word, self.meaning)

if __name__ == '__main__':
	word = Word('test', '测试', 0)
	print word