# coding: utf-8
from Recite import Recite
import ui
LABEL_WORD_NAME = 'label_word'
LABEL_ERR_CNT_NAME = 'label_err_cnt'
LABEL_RECITED_CNT_NAME = 'label_recited_cnt'
LABEL_TOTAL_NUM_NAME = 'label_total_num'
TEXTVIEW_MEANING_NAME = 'textview_meaning'
BUTTON_ERROR_NAME = 'button_error'
BUTTON_RIGHT_NAME = 'button_right'
BUTTON_SHOW_NAME = 'button_show'

class ReciteView (ui.View):
	def __init__(self):
		self.recite = Recite('words.txt')
		self.recite.shuffle()
	def did_load(self):
		self[BUTTON_RIGHT_NAME].enabled = False
		self[BUTTON_ERROR_NAME].enabled = False
		self[TEXTVIEW_MEANING_NAME].editable = False
		self[LABEL_WORD_NAME].text = self.recite.pickone().word
		self[LABEL_TOTAL_NUM_NAME].text = str(self.recite.length())
		self[LABEL_RECITED_CNT_NAME].text = str(self.recite.current_index+1)
		self[LABEL_ERR_CNT_NAME].text = '0'
	def will_close(self):
		self.recite.save('words.txt')

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

if __name__ == '__main__':
	v = ui.load_view('Test')
	if ui.get_screen_size()[1] >= 768:
		# ipad
		v.present('sheet')
	else:
		# iphone
		v.present(orientations=['portrait'])