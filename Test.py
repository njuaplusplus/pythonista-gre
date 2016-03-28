# coding: utf-8
from Recite import Recite
import ui
import speech

LABEL_WORD_NAME = 'label_word'
LABEL_ERR_CNT_NAME = 'label_err_cnt'
LABEL_RECITED_CNT_NAME = 'label_recited_cnt'
LABEL_TOTAL_NUM_NAME = 'label_total_num'
TEXTVIEW_MEANING_NAME = 'textview_meaning'
BUTTON_ERROR_NAME = 'button_error'
BUTTON_RIGHT_NAME = 'button_right'
BUTTON_SHOW_NAME = 'button_show'
BUTTON_EXIT_NAME = 'button_exit'
BUTTON_MENU_START_NAME = 'button_menu_start'
BUTTON_MENU_EXIT_NAME = 'button_menu_exit'
BUTTON_SPEAK_NANE = 'button_speak'
TEXTFIELD_ERR_TIMES_THRESHOLD = 'textfield_err_times_threshold'
TEXTFIELD_MAX_RECITING = 'textfield_max_reciting'
SWITCH_SHUFFLE = 'switch_shuffle'
SWITCH_SPEECH = 'switch_auto_speech'

class ReciteMenuView(ui.View):
	def __init__(self):
		self.start2recite = False
	

class ReciteView (ui.View):
	def __init__(self):
		self.recite = Recite('words.txt')
		self.auto_speech = False
		
	def did_load(self):
		self[BUTTON_RIGHT_NAME].enabled = False
		self[BUTTON_ERROR_NAME].enabled = False
		self[TEXTVIEW_MEANING_NAME].editable = False
		self[LABEL_RECITED_CNT_NAME].text = str(self.recite.current_index+1)
		self[LABEL_ERR_CNT_NAME].text = '0'
		
	def will_close(self):
		self.recite.save('words.txt')
		
	def shuffle(self):
		self.recite.shuffle()
	
	def filter(self, max_reciring, err_times_threshold):
		self.recite.filter(max_reciting, err_times_threshold)
	
	def before_present(self):
		word = self.recite.pickone()
		if word is None:
			self.close()
		else:
			self[LABEL_WORD_NAME].text = word.word
			self[LABEL_TOTAL_NUM_NAME].text = str(self.recite.reciting_length())
			if self.auto_speech:
				speech.say(word.word, 'en-US')
		
		
def button_tapped(sender):
	button_name = sender.name
	label_word = sender.superview[LABEL_WORD_NAME]
	textview_meaning = sender.superview[TEXTVIEW_MEANING_NAME]
	if button_name == BUTTON_ERROR_NAME:
		sender.superview.recite.record_error()
	elif button_name == BUTTON_SHOW_NAME:
		sender.superview[BUTTON_RIGHT_NAME].enabled = True
		sender.superview[BUTTON_ERROR_NAME].enabled = True
		textview_meaning.text = sender.superview.recite.current_word().meaning
		return
	elif button_name == BUTTON_EXIT_NAME:
		sender.superview.close()
		return
	elif button_name == BUTTON_MENU_START_NAME:
		sender.superview.start2recite	= True
		sender.superview.close()
		return
	elif button_name == BUTTON_MENU_EXIT_NAME:
		sender.superview.start2recite = False
		sender.superview.close()
		return
	elif button_name == BUTTON_SPEAK_NANE:
		speech.say(label_word.text, 'en-US')
		return
	sender.superview[BUTTON_RIGHT_NAME].enabled = False
	sender.superview[BUTTON_ERROR_NAME].enabled = False
	word = sender.superview.recite.pickone()
	if word is None:
		sender.superview.close()
	else:
		label_word.text = word.word
		textview_meaning.text = ''
		sender.superview[LABEL_RECITED_CNT_NAME].text = str(sender.superview.recite.current_index+1)
		sender.superview[LABEL_ERR_CNT_NAME].text = str(sender.superview.recite.error_cnt())
		if sender.superview.auto_speech:
			speech.say(word.word, 'en-US')

if __name__ == '__main__':
	menu = ui.load_view('Menu')
	menu.present(orientations=['portrait'], hide_title_bar=True)
	menu.wait_modal()
	if menu.start2recite:
		v = ui.load_view('Test')
		err_times_threshold = 0
		max_reciting = 100
		try:
			err_times_threshold = int(menu[TEXTFIELD_ERR_TIMES_THRESHOLD].text)
			max_reciting = int(menu[TEXTFIELD_MAX_RECITING].text)
		except ValueError as err:
			print('Can not convert to int' + str(err))
		v.filter(max_reciting, err_times_threshold)
		if menu[SWITCH_SHUFFLE].value == True:
			v.shuffle()
		v.auto_speech = menu[SWITCH_SPEECH].value
		v.before_present()
		v.present(orientations=['portrait'], hide_title_bar=True)