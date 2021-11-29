#! /bin/python3
import sys

import requests
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from interface import Ui_autorise
from ofinterface import Ui_Dialog
from os import system


lessons = []
Data_status = ""

# Объявляем функции для кодирования и декодирования

def encode_fun():                              #Фун-я кодирования



# ----------------------Окно для авторизации-----------------------

	class Autorise(QMainWindow, Ui_autorise):
		def __init__(self, *args, **kwargs):
			super(Autorise, self).__init__(*args, **kwargs)
			self.setupUi(self)
			self.center()

			self.visibility = False
			# binds
			self.eye.pressed.connect(lambda: self.change_visibility())
			self.logIn.pressed.connect(lambda: self.to_log_in())
			self.loginLine.returnPressed.connect(lambda: self.go_to_pass())
			self.passLine.returnPressed.connect(lambda: self.to_log_in())

		def center(self):
			qr = self.frameGeometry()
			cp = QDesktopWidget().availableGeometry().center()
			qr.moveCenter(cp)
			self.move(qr.topLeft())

		def change_visibility(self):
			if self.visibility:
				self.icon1 = QtGui.QIcon()
				self.icon1.addPixmap(QtGui.QPixmap("img/invisible.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
				self.passLine.setEchoMode(2)
				self.eye.setIcon(self.icon1)
				self.visibility = False
			else:
				self.passLine.setEchoMode(0)
				self.icon2 = QtGui.QIcon()
				self.icon2.addPixmap(QtGui.QPixmap("img/eye-close-up.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
				self.eye.setIcon(self.icon2)
				self.visibility = True


		def to_log_in(self):
			if len(self.loginLine.text()) > 3 and len(self.passLine.text()) > 3:

				global decoded_password_str, decoded_login_str

				decoded_login_str = self.loginLine.text()
				decoded_password_str = self.passLine.text()
				self.close()
			else:
				self.passLabel.setStyleSheet("#passLabel{color:red;}")
				self.loginLabel.setStyleSheet("#loginLabel{color:red;}")


		def go_to_pass(self):
			self.passLine.setFocus()


	app = QApplication([])
	win = Autorise()
	win.show()
	app.exec()

# -------------------создание файла с закодированными данными входа---------------------------



	with open('DataFiles/data1.txt', 'w') as f:#Безопасно открываем файл для дальнейшей записи зашифрованных данных

		for encsym1 in decoded_login_str:                #В цыкле обходим все символы, преобразуем из в двоичный код, "шифруем", и записываем в файл
			f.write( str( ord(encsym1) * 1024 ) + '\n' )
		f.write('stop' + '\n')                 #Это для того, чтобы отделить логин от пароля
		for encsym2 in decoded_password_str:
			f.write( str( ord(encsym2) * 1024 ) + '\n' )
		f.close()


def decoded_func():                             #Фун-я декодирования данных файла
	with open('DataFiles/data1.txt', 'r') as fr:          #Безопасно открываем файл
		decoded = fr.read().splitlines()        #Построчно читаем файл, параллельно записывая данные в список
		fr.close()

	decoded_login = []  						#Объявляем списки
	decoded_password = []

	p = 0
	for i in decoded:							#Цыкл, в котором обходится список с закодированной инфой, посредством ключевого слова отделяется лгин от пароля
		if i == 'stop':							#И идёт дешифровка, затем данные записываются по своим спискам
			p = 1

		if p == 0 and i != 'stop':
			decoded_login.append( chr( int(i) // 1024 ) ) 
		elif p == 1 and i != 'stop':
			decoded_password.append( chr( int(i) // 1024 ) ) 
	global decoded_login_str					#Переменные делаются глобальными
	global decoded_password_str
	decoded_login_str = ''.join(decoded_login)	#Преобразование списков в строки
	decoded_password_str = ''.join(decoded_password)






# -----------------Окно с сообщением о завершении парсинга и предложением открыть файл отчёта------------

def to_openFile():


	class OpeningFile(QDialog, Ui_Dialog):
		def __init__(self, *args, **kwargs):
			super(OpeningFile, self).__init__(*args, **kwargs)
			self.setupUi(self)

		def toOpenFile(self):
			system("x-www-browser site.html")
			self.close()

		def cancel(self):
			self.close()


	app = QApplication([])
	win = OpeningFile()
	win.show()
	app.exec()


# ------------------Блок парсинга--------------------------
def parsing():
	session = requests.Session()					#Создание сессии

	link = 'https://eos.sfvstu.ru/index.php'			#Ссылка на сайт
	# Объявление заголовков
	header = {
		'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/536.30.1 (KHTML, like Gecko) Version/6.0.5 Safari/536.30.1'
		
	}
	 
	# Блок с данными для входа 


	datas = {
		'login': decoded_login_str,    #decoded_login_str
		'password': decoded_password_str,       #decoded_password_str
		'op': 'login',
		'form_login': ''
	}

	# авторизация

	response = session.post(link, data = datas, headers = header)
	response = session.post(link, data = datas, headers = header)

	# Получение ссылок на страницы предметов
	response_text = BeautifulSoup(response.text)
	# Проверка на правильность введённых данных авторизации
	if response_text.find('div', {'class': 'form-item-input-short'}):
		global Data_status
		Data_status = "Данные авторизации неверные"
		encode_fun()
		parsing()
	else:
		print('Авторизация прошла успешно')
		# print(response_text.find('table'))
		table = response_text.find('table')
		for link in table.find_all('td', { "class" : "open-item" }):
			lessons.append(link.find('a').get('href'))
		print(response_text.find_all('td', { "class" : "open-item" }))

		# Блок, в котором в цыкле получаются страницы с таблицами, таблицы изымаются и помещаются в отдельно созданный файл
		print("Ссылки на предметы ", lessons)
		file = open("site.html", "w")
		file.write("<!DOCTYPE html>\n<html lang='ru'>\n<head>\n    <title>Отчёт</title>\n    <link rel='icon' href='css/ico.png'>\n    <link rel='stylesheet' type='text/css' href='css/common8.css'>\n</head><body>")
		for table in lessons:
			learn = 'http://eos.sfvstu.ru' + table
			content = session.get(learn)
			soup = BeautifulSoup(content.text)
			file.write(str(soup.find('div', {'class': 'section-header'})))
			file.write(str(soup.find('table')))
		file.write('<script type="text/javascript" src="js/jquery-3.4.1.min.js"></script>\n<script type="text/javascript" src="js/scropt1.js"></script> </body>\n</html>')
		file.close()

		to_openFile() #После завершения процесса парсинга открывается окно


#Проверка файла на существование (если его нет, выдаст ошибку, которая будет перехвачена и вызвана функция создания файла)
def main():
	try:											
		file = open('DataFiles/data1.txt')
		file.close()

		decoded_func()
		parsing()
			
	except FileNotFoundError:

		encode_fun()
		parsing()

if __name__ == '__main__':
	main()
