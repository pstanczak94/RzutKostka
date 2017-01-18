#! python2.7-32
# -*- coding: utf-8 -*-

import sys
import math
import random
import os
import time
import msvcrt

import Tkinter
from Tkinter import *

def rzut_kostka():
	return random.randint(1, 6)

settings = {
	'n_tur' : 5,
	'zwyciestwa' : [0, 0],
	'remisy' : 0,
	'tura' : 1,
	'gracz' : 0,
	'rzut' : 0,
	'rzuty' : [[], []],
	'wyniki' : [[], []]
}

def next_step(s):
	global mainFrame
	info = ""
	
	if s['tura'] <= s['n_tur'] or s['zwyciestwa'][0] == s['zwyciestwa'][1]:
		
		mainFrame.setTura(s['tura'])
		mainFrame.setTura2(s['tura'] > s['n_tur'])
		mainFrame.setGracz(s['gracz'] +1)
		
		if s['rzut'] == 0:
			s['rzuty'][s['gracz']].append([0, 0])
		
		if s['rzut'] == 1 or s['rzut'] == 2:
			s['rzuty'][s['gracz']][s['tura']-1][s['rzut']-1] = rzut_kostka()

		rzut1 = s['rzuty'][s['gracz']][s['tura']-1][0]
		rzut2 = s['rzuty'][s['gracz']][s['tura']-1][1]
		wynik = rzut1 + rzut2
		
		if s['rzut'] >= 1:
			info += "Pierwszy rzut: " + str(rzut1) + "\n"
			
		if s['rzut'] >= 2:
			info += "Drugi rzut: " + str(rzut2) + "\n"
			info += "Razem: " + str(wynik) + "\n"
		
		if s['rzut'] >= 1:
			info += "\n"
		
		if s['rzut'] == 0:
			info += "Nacisnij kontynuuj, aby wykonac pierwszy rzut...\n\n"
		elif s['rzut'] == 1:
			info += "Nacisnij kontynuuj, aby wykonac drugi rzut...\n\n"

		s['rzut'] += 1
		
		if s['rzut'] == 3:
			s['wyniki'][s['gracz']].append(wynik)
			s['rzut'] = 0
			s['gracz'] += 1
			
		if s['gracz'] == 2:
			wynik1 = s['wyniki'][0][s['tura']-1]
			wynik2 = s['wyniki'][1][s['tura']-1]
			
			if wynik1 > wynik2:
				s['zwyciestwa'][0] += 1
			elif wynik2 > wynik1:
				s['zwyciestwa'][1] += 1
			else:
				s['remisy'] += 1
				
			s['tura'] += 1
			s['gracz'] = 0
	else:
		mainFrame.txtInfo["font"] = ("Verdana", 18, "bold")
		mainFrame.txtInfo["fg"] = "darkgreen"
		mainFrame.txtLiczbaTur.pack_forget()
		mainFrame.txtTura.pack_forget()
		mainFrame.txtTura2.pack_forget()
		mainFrame.txtGracz.pack_forget()
		mainFrame.btnContinue.pack_forget()
		mainFrame.txtWynik.pack(side='top', fill='x', expand=1)
		mainFrame.txtInfo.pack(side='top', fill='x', expand=1)
		
		if s['zwyciestwa'][0] > s['zwyciestwa'][1]:
			info += "Wygrał gracz pierwszy!"
		elif s['zwyciestwa'][1] > s['zwyciestwa'][0]:
			info += "Wygrał gracz drugi!"
		else:
			info += "Remis!"
		
	mainFrame.setWynik(s['zwyciestwa'])
	mainFrame.setInfo(info.strip())

# GUI

class Window(Tk):
	def __init__(self, master=None):
		Tk.__init__(self, master)
		
class RootFrame(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.pack(padx=10, pady=10)
	def continueAction(self):
		global settings
		next_step(settings)
	def exitAction(self):
		global mainWindow
		mainWindow.destroy()
	def setLiczbaTur(self, wartosc):
		self.txtLiczbaTur["text"] = "Liczba tur: " + str(wartosc)
	def setWynik(self, arr):
		self.txtWynik["text"] = "Wynik [" + str(arr[0]) + ":" + str(arr[1]) + "]"
	def setTura(self, tura):
		self.txtTura["text"] = "Tura numer " + str(tura)
	def setTura2(self, tura):
		if tura == True:
			self.txtTura2["text"] = "(dodatkowa tura)"
		else:
			self.txtTura2["text"] = ""
	def setGracz(self, gracz):
		self.txtGracz["text"] = "Tura gracza nr " + str(gracz)
	def setInfo(self, info):
		self.txtInfo["text"] = info
		
mainWindow = Window()
mainWindow.title('rzut_kostka')
mainWindow.minsize(500, 400)
mainWindow.resizable(FALSE, FALSE)

mainFrame = RootFrame(mainWindow)
mainFrame.pack(anchor='nw', fill='both', expand=1)

txtLiczbaTur = Label(mainFrame)
txtLiczbaTur["font"] = ("Verdana", 12, "normal")
txtLiczbaTur.pack(side='top', anchor='w')
mainFrame.txtLiczbaTur = txtLiczbaTur

txtWynik = Label(mainFrame)
txtWynik["font"] = ("Verdana", 16, "bold")
txtWynik.pack(side='top', fill='x', ipady=10)
mainFrame.txtWynik = txtWynik

txtTura = Label(mainFrame)
txtTura["font"] = ("Verdana", 12, "normal")
txtTura.pack(side='top', fill='x')
mainFrame.txtTura = txtTura

txtTura2 = Label(mainFrame)
txtTura2["font"] = ("Verdana", 12, "normal")
txtTura2.pack(side='top', fill='x')
mainFrame.txtTura2 = txtTura2

txtGracz = Label(mainFrame)
txtGracz["font"] = ("Verdana", 12, "normal")
txtGracz.pack(side='top', fill='x')
mainFrame.txtGracz = txtGracz

txtInfo = Label(mainFrame)
txtInfo["font"] = ("Verdana", 10, "normal")
txtInfo["text"] = 'Nacisnij kontynuuj, aby rozpoczac...'
txtInfo.pack(side='top', fill='both', expand=1, ipady=5)
mainFrame.txtInfo = txtInfo

buttons = Frame(mainFrame)
buttons.pack(side='bottom', fill='x')

btnContinue = Button(buttons)
btnContinue.pack(side='left')
btnContinue.configure(text='Kontynuuj', fg='darkgreen', padx=20, pady=2)
btnContinue["font"] = ("Comic Sans MS", 12, "normal")
btnContinue["command"] = mainFrame.continueAction
mainFrame.btnContinue = btnContinue

btnQuit = Button(buttons)
btnQuit.pack(side='right')
btnQuit.configure(text='Wyjdz', fg='red', padx=20, pady=2)
btnQuit["font"] = ("Comic Sans MS", 12, "normal")
btnQuit["command"] = mainFrame.exitAction
mainFrame.btnQuit = btnQuit

if len(sys.argv) > 1: # jezeli podano dodatkowy parametr do programu
	settings['n_tur'] = int(sys.argv[1]) # pobierz liczbe tur z parametrow programu

mainFrame.setLiczbaTur(settings['n_tur'])
mainFrame.setWynik([0, 0])

mainWindow.mainloop()