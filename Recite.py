# coding: utf-8
from Word import Word
import random
from datetime import datetime

class Recite (object):
	def  __init__(self, filename):
		self.words = []
		self.reciting_words = []
		self.err_words = []
		self.current_index = -1
		self.shuffled = False
		self.err_times_threshold = 0
		try:
			with open(filename) as data:
				for line in data:
					err_times, word, meaning = line.split(' ', 2)
					self.words.append(Word(word, meaning, int(err_times)))
		except IOError as err:
			print('File error: ' + str(err))
			
	def recite(self):
		for word in self.recitig_words:
			print word.word
			s = raw_input('input 1')
			print word.meaning
			s = raw_input('1 for err, 2 for right, 3 for exit')
			if s == '1':
				word.add_err_times()
			elif s == '3':
				break
				
	def save(self, filename):
		try:
			with open(filename, 'w') as data:
				data.writelines([str(w) for w in self.words])
		except IOError as err:
			print('File error: ' + str(err))
		try:
			with open('status.txt', 'a') as data:
				data.write(datetime.today().strftime('%Y%m%d %H:%M:%S\n'))
				data.write('Err: %d, recited: %d, total: %d\n' % (self.error_cnt(), self.current_index, self.length()))
				data.write('Shuffled: %s, err_times_threshold: %d,  reciting_length: %d\n' % (self.shuffled, self.err_times_threshold, self.reciting_length()))
				data.writelines([str(w) for w in self.err_words])
				data.write('==================\n')
		except IOError as err:
			print('File error: ' + str(err))

	def pickone(self):
		self.current_index += 1
		if self.current_index == self.reciting_length():
			return None
		return self.reciting_words[self.current_index]
		
	def current_word(self):
		return self.reciting_words[self.current_index]
	
	def record_error(self):
		self.reciting_words[self.current_index].add_err_times()
		self.err_words.append(self.reciting_words[self.current_index])
		
	def length(self):
		return len(self.words)
	
	def reciting_length(self):
		return len(self.reciting_words)
		
	def error_cnt(self):
		return len(self.err_words)
	
	def shuffle(self):
		random.shuffle(self.reciting_words)
	
	def filter(self, max_reciting,  err_times_threshold):
		self.reciting_words = self.words[-max_reciting:]
		self.err_times_threshold = err_times_threshold
		self.reciting_words = [w for w in self.reciting_words if w.err_times >= err_times_threshold]
		
if __name__ == '__main__':
	recite = Recite('words.txt')
	recite.save('output.txt')
	