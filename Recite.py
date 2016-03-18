# coding: utf-8
from Word import Word
import random
from datetime import datetime

class Recite (object):
	def  __init__(self, filename):
		self.words = []
		self.err_words = []
		self.current_index = -1
		self.shuffled = False
		try:
			with open(filename) as data:
				for line in data:
					err_times, word, meaning = line.split(' ', 2)
					self.words.append(Word(word, meaning, int(err_times)))
		except IOError as err:
			print('File error: ' + str(err))
			
	def recite(self):
		for word in self.words:
			print word.word
			s = raw_input('input 1')
			print word.meaning
			s = raw_input('1 for err, 2 for right, 3 for exit')
			if s == '1':
				word.add_err_times()
			elif s == '3':
				break
				
	def save(self, filename):
		if self.shuffled:
			self.words.sort(key=lambda w: w.word)
		try:
			with open(filename, 'w') as data:
				data.writelines([str(w) for w in self.words])
		except IOError as err:
			print('File error: ' + str(err))
		try:
			with open('status.txt', 'a') as data:
				data.write(datetime.today().strftime('%Y%m%d %H:%M:%S\n'))
				data.write('Err: %d, recited: %d, total: %d\n' % (self.error_cnt(), self.current_index, self.length()))
				data.writelines([str(w) for w in self.err_words])
				data.write('==================\n')
		except IOError as err:
			print('File error: ' + str(err))

	def pickone(self):
		self.current_index += 1
		if self.current_index == self.length():
			return None
		return self.words[self.current_index]
		
	def current_word(self):
		return self.words[self.current_index]
	
	def record_error(self):
		self.words[self.current_index].add_err_times()
		self.err_words.append(self.words[self.current_index])
		
	def length(self):
		return len(self.words)
	
	def error_cnt(self):
		return len(self.err_words)
	
	def shuffle(self):
		random.shuffle(self.words)
		self.shuffled = True
	
	def filter(self, err_times):
		if err_times > 0:
			self.words = [w for w in self.words if w.err_times > err_times]
		
if __name__ == '__main__':
	recite = Recite('words.txt')
	recite.save('output.txt')
	