import requests
import wx
import wx.xrc
from bs4 import BeautifulSoup
from os import unlink, system
from sys import exit

lessons = []
Data_status = ""

# Объявляем функции для кодирования и декодирования

def encode_fun():                              #Фун-я кодирования



# ----------------------Окно для авторизации-----------------------

	class siginWindow ( wx.Frame ):

		def __init__( self, parent ):
			wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Данные авторизации", pos = wx.DefaultPosition, size = wx.Size( 255,220 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.TAB_TRAVERSAL )

			self.Bind(wx.EVT_CLOSE, self.windowClose)

			self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

			bSizer1 = wx.BoxSizer( wx.VERTICAL )

			self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"Использование данной программы ", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ST_NO_AUTORESIZE )
			self.m_staticText3.Wrap( -1 )

			bSizer1.Add( self.m_staticText3, 0, wx.ALL|wx.EXPAND, 2 )

			self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"несёт угрозу вашим данным авторизации", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
			self.m_staticText4.Wrap( -1 )

			bSizer1.Add( self.m_staticText4, 0, wx.ALL|wx.EXPAND, 2 )

			fgSizer1 = wx.FlexGridSizer( 0, 2, 0, 0 )
			fgSizer1.SetFlexibleDirection( wx.BOTH )
			fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

			self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Логин", wx.DefaultPosition, wx.DefaultSize, 0 )
			self.m_staticText1.Wrap( -1 )

			fgSizer1.Add( self.m_staticText1, 0, wx.ALL, 10 )

			self.m_textCtrl1 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
			fgSizer1.Add( self.m_textCtrl1, 0, wx.ALL, 5 )

			self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Пароль", wx.DefaultPosition, wx.DefaultSize, 0 )
			self.m_staticText2.Wrap( -1 )

			fgSizer1.Add( self.m_staticText2, 0, wx.ALL, 5 )

			self.m_textCtrl2 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PASSWORD|wx.TE_PROCESS_ENTER )
			fgSizer1.Add( self.m_textCtrl2, 0, wx.ALL, 5 )


			bSizer1.Add( fgSizer1, 1, wx.ALL|wx.EXPAND|wx.TOP, 5 )

			self.m_button1 = wx.Button( self, wx.ID_ANY, u"Войти", wx.DefaultPosition, wx.DefaultSize, 0 )
			bSizer1.Add( self.m_button1, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
			self.Bind(wx.EVT_BUTTON, self.login, self.m_button1)

			self.data_status = wx.StaticText( self, wx.ID_ANY, u""+Data_status, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
			self.data_status.Wrap( -1 )

			bSizer1.Add( self.data_status, 0, wx.ALL|wx.EXPAND, 5 )

			self.SetSizer( bSizer1 )
			self.Layout()

			self.Centre( wx.BOTH )

		def __del__( self ):
			pass

		def windowClose(self, event):
			exit()

		def login(self, event):
			if len(self.m_textCtrl1.GetValue()) > 3 and len(self.m_textCtrl2.GetValue()) > 3:

				global decoded_password_str
				global decoded_login_str

				decoded_login_str = self.m_textCtrl1.GetValue()
				decoded_password_str = self.m_textCtrl2.GetValue()
				self.Destroy()
			else:
				self.data_status.SetLabel("Введите данные")



	app = wx.App()
	frame = siginWindow(None) #"Форма авторизации"
	frame.Show()
	app.MainLoop()
	

# -------------------создание файла с закодированными данными входа---------------------------



	with open('DataFiles\\data1.txt', 'w') as f:          #Безопасно открываем файл для дальнейшей записи зашифрованных данных

		for encsym1 in decoded_login_str:                #В цыкле обходим все символы, преобразуем из в двоичный код, "шифруем", и записываем в файл
			f.write( str( ord(encsym1) * 1024 ) + '\n' )
		f.write('stop' + '\n')                 #Это для того, чтобы отделить логин от пароля
		for encsym2 in decoded_password_str:
			f.write( str( ord(encsym2) * 1024 ) + '\n' )
		f.close()

def decoded_func():                             #Фун-я декодирования данных файла
	with open('DataFiles\\data1.txt', 'r') as fr:          #Безопасно открываем файл
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

###########################################################################
## Class OpeningFile
###########################################################################

	class OpeningFile ( wx.Frame ):

		def __init__( self, parent ):
			wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Открыть отчёт?", pos = wx.DefaultPosition, size = wx.Size( 404,107 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL )

			# self.Bind(wx.EVT_CLOSE, self.windowClose)

			self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

			bSizer1 = wx.BoxSizer( wx.VERTICAL )

			self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Парсинг окончен, открыть файл отчёта в браузере?", wx.DefaultPosition, wx.DefaultSize, 0 )
			self.m_staticText1.Wrap( -1 )

			bSizer1.Add( self.m_staticText1, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

			bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

			self.m_button3 = wx.Button( self, wx.ID_ANY, u"Да", wx.DefaultPosition, wx.DefaultSize, 0 )
			bSizer2.Add( self.m_button3, 0, wx.ALL, 5 )

			self.Bind(wx.EVT_BUTTON, self.to_openFile, self.m_button3)

			self.m_button4 = wx.Button( self, wx.ID_ANY, u"Нет", wx.DefaultPosition, wx.DefaultSize, 0 )
			bSizer2.Add( self.m_button4, 0, wx.ALL, 5 )

			self.Bind(wx.EVT_BUTTON, self.to_notopenFile, self.m_button4)


			bSizer1.Add( bSizer2, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )


			self.SetSizer( bSizer1 )
			self.Layout()

			self.Centre( wx.BOTH )

		def __del__( self ):
			pass

		def to_openFile(self, event):
			system("start site.html")
			self.Destroy()

		def to_notopenFile(self, event):
			self.Destroy()

		def windowClose(self, event):
			pass


	app = wx.App()
	frame = OpeningFile(None) 
	frame.Show()
	app.MainLoop()



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
		'login': decoded_login_str,
		'password': decoded_password_str,
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
		# print(response_text.find('table', border=1))
		response_text.find('table', border=1).extract()
		for link in response_text.find_all('td', { "class" : "open-item" }):
			lessons.append(link.find('a').get('href'))
			# print(link)

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
		file = open('DataFiles\\data1.txt')
		file.close()

		decoded_func()
		parsing()
			
	except FileNotFoundError:


		encode_fun()
		parsing()

if __name__ == '__main__':
	main()
