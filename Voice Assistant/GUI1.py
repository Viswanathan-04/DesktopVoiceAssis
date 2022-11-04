from tkinter import *
from tkinter import ttk,messagebox
from playsound import playsound
import threading
import pyttsx3
import time
import subprocess
import requests
import os
import wikipedia
import webbrowser
import json
from bs4 import BeautifulSoup
import speech_recognition as sr

try:
	main=Tk()
	engine=pyttsx3.init()
	engine.setProperty('rate', 190)
	r=sr.Recognizer()
	voices=engine.getProperty('voices')
	act='activate.wav'
	deact='deactivate.wav'
	try:	
		f=open('sett.json','r')
		jsonContent=f.read()
		alist=json.loads(jsonContent)
		f.close()
	except:
		with open('sett.json','w') as f:
			adict={'background':'Snow','foreground':'Black','Name':'Your name','voice':"0"}
			jsonString=json.dumps(adict)
			f.write(jsonString)
		f=open('sett.json','r')
		jsonContent=f.read()
		alist=json.loads(jsonContent)
		f.close()
	background,foreground,name,voi=alist['background'],alist['foreground'],alist['Name'],alist['voice']
	engine.setProperty('voice', voices[int(voi)].id)
	url="https://www.google.com/search?q="+'weather'
	page=requests.get(url)
	soup=BeautifulSoup(page.text,'html.parser')
	con=soup.find_all(class_='BNeawe')			
	loc=con[0].text.split()
	temp=con[3].text
	weat=con[5].text
	li=con[5].text.split()
	l=[i.lower() for i in li]

	#Functions

	def wish():
		ctime=time.strftime("%H:%M:%S")
		if '00:00:00'<ctime<'12:00:00':
			engine.say("Good Morning")
		elif '12:00:00'<ctime<'16:00:00':
			engine.say("Good Afternoon")
		else:
			engine.say("Good Evening")
		engine.say("How may I help you?")
		engine.runAndWait()
		threading.Thread(target=listen).start()

	def menu():
		b=Tk()
		def write():
			if bddm3.get()=="Male":
				voi="0"
			else:
				voi="1"
			with open('sett.json','w') as f:
				adict={'background':bddm1.get(),'foreground':bddm2.get(),'Name':bent1.get(),'voice':voi}
				jsonString = json.dumps(adict)
				f.write(jsonString)
			messagebox.showinfo(parent=b,title="Information",message='This application needs to restart to save changes')
			os._exit(0)
		blab0=Label(b,text='Settings',font=('Calibri',24),bg=background,fg=foreground)
		blab0.place(relx=0.25,rely=0.075,relwidth=0.5,relheight=0.07)
		blab1=Label(b,text='Background Color',font=('Calibri',18),bg=background,fg=foreground)
		blab1.place(relx=0.01,rely=0.2,relwidth=0.5,relheight=0.07)
		bddm1=ttk.Combobox(b,font='Arial 14',width=12,state="readonly")
		bddm1['values']=("Grey20","Snow","Purple3","Brown","Yellow")
		bddm1.current(0)
		bddm1.place(relx=0.54,rely=0.2,relwidth=0.45,relheight=0.07)
		blab2=Label(b,text='Foreground Color',font=('Calibri',18),bg=background,fg=foreground)
		blab2.place(relx=0.01,rely=0.3,relwidth=0.5,relheight=0.07)
		bddm2=ttk.Combobox(b,font='Arial 14',width=12,state="readonly")
		bddm2['values']=("Orange","Black","SpringGreen","Lemon Chiffon","Red")
		bddm2.current(0)
		bddm2.place(relx=0.54,rely=0.3,relwidth=0.45,relheight=0.07)
		blab1=Label(b,text='Your Name',font=('Calibri',18),bg=background,fg=foreground)
		blab1.place(relx=0.01,rely=0.4,relwidth=0.5,relheight=0.07)
		bent1=Entry(b,text='',font=('Calibri',17))
		bent1.insert(END,'Enter your Name')
		bent1.bind('<Button-1>',lambda x:bent1.delete(0,END))
		bent1.place(relx=0.54,rely=0.4,relwidth=0.45,relheight=0.07)
		blab3=Label(b,text='Voice',font=('Calibri',18),bg=background,fg=foreground)
		blab3.place(relx=0.01,rely=0.5,relwidth=0.5,relheight=0.07)
		bddm3=ttk.Combobox(b,font='Arial 14',width=12,state="readonly")
		bddm3['values']=("Male","Female")
		bddm3.current(0)
		bddm3.place(relx=0.54,rely=0.5,relwidth=0.45,relheight=0.07)
		bbtn1=Button(b,text='Save Changes',command=write,bd=0,font=('Calibri',18),bg=background,fg=foreground)
		bbtn1.place(relx=0.25,rely=0.75,relwidth=0.5,relheight=0.07)
		b.geometry("400x640+550+75")
		b.resizable(0,0)
		b.config(bg=background)
		b.title('Personal Assistant - Settings')
		b.mainloop()

	def listen():
		while True:
			with sr.Microphone() as source:
				try:
					r.adjust_for_ambient_noise(source, duration=0.5)
					playsound(act)
					btn1.config(fg=foreground)
					btn1.config(text='Listening...')
					audio=r.listen(source,phrase_time_limit=5)
					btn1.config(text='Processing...')
					text=r.recognize_google(audio)
					btn1.config(text="Say 'Ok google'")
					tb1.delete('1.0',END)
					tb1.insert('1.0',' You Said : '+text)
					search(text.lower())
					continue

				except sr.UnknownValueError:
					btn1.config(text="Say 'Ok google'")
					playsound(deact)
					threading.Thread(target=wake).start()
					break

				except:
					playsound(deact)
					btn1.config(text="Say 'Ok google'")
					messagebox.showerror(parent=main,title="Error",message='No Internet Connection\nPlease relaunch application after connecting to internet')
					threading.Thread(target=wake).start()
					break

	def hear():
		while True:
			with sr.Microphone() as source:
				try:
					r.adjust_for_ambient_noise(source, duration=0.5)
					btn1.config(text='Listening...')
					audio=r.listen(source,phrase_time_limit=5)
					btn1.config(text='Processing...')
					text=r.recognize_google(audio)
					btn1.config(text="Say 'Ok google'")
					return text
					break
				except:
					break

	def search(ques):
		btn1.config(text="Say 'Ok google'")
		if "news" in ques:
			url="https://news.google.com/topstories"
			page=requests.get(url)
			soup=BeautifulSoup(page.text,'html.parser')
			con=soup.find_all(class_='ipQwMb ekueJc RD0gLb')
			for i in rangxe(5):				
				engine.say(con[i].text)
				print(con[i].text)
		elif 'your name' in ques:
			engine.say('My name is Google')
		elif 'my name' in ques:
			engine.say('Your name is'+name)
		elif 'how are you' in ques:
			engine.say("I'm fine")
			engine.say("how are you")
		elif 'i am fine' in ques or "i'm fine" in ques:
			engine.say("Good to hear that. How may I help you?")
		elif 'what is the time now' in ques or 'what time is it' in ques:
			ctime=time.strftime("%H:%M:%S %p")
			engine.say(ctime)
		elif 'open notepad' in ques:
			engine.say('Opening Notepad')
			subprocess.Popen("notepad.exe")
		elif 'close notepad' in ques:
			engine.say('Closing Notepad')
			os.system("taskkill /F /IM notepad.exe")
		elif 'open youtube' in ques:
			engine.say("Opening Youtube")
			con=webbrowser.open('https://www.youtube.com')
		elif 'in youtube' in ques:
			engine.say("Here are some of the videos I found related to your query")
			con=webbrowser.open('https://www.youtube.com/results?search_query='+ques.replace('play','').replace('in youtube',''))
		elif 'open chrome' in ques or 'open google chrome' in ques:
			engine.say('Opening Google Chrome')
			subprocess.Popen("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
		elif 'close chrome' in ques or 'close google chrome' in ques:
			engine.say('Closing Google Chrome')
			os.system("taskkill /F /IM chrome.exe")
		elif 'open microsoft edge' in ques or 'open edge' in ques:
			engine.say('Opening Microsoft Edge')
			subprocess.Popen("C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe")
		elif 'close microsoft edge' in ques or 'close edge' in ques:
			engine.say('Closing Microsoft Edge')
			os.system("taskkill /F /IM msedge.exe")
		elif 'open sublime text' in ques:
			engine.say('Opening Sublime Text')
			subprocess.Popen("C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\sublime_text.exe")
		elif 'close sublime text' in ques:
			engine.say('Closing Sublime Text')
			os.system("taskkill /F /IM sublime_text.exe")
		elif 'change voice' in ques or 'change your voice' in ques:
			threading.Thread(target=menu).start()
			engine.say("I have opened the menu for you to change the voice. Please make the changes")
		elif 'weather in' in ques:
			url="https://www.google.com/search?q="+ques
			page=requests.get(url)
			soup=BeautifulSoup(page.text,'html.parser')
			con=soup.find_all(class_='BNeawe')
			engine.say(con[0].text)
			engine.say("Its"+con[3].text+'outside')
			engine.say(con[5].text)
		elif 'weather' in ques:
			url="https://www.google.com/search?q="+'weather'
			page=requests.get(url)
			soup=BeautifulSoup(page.text,'html.parser')
			con=soup.find_all(class_='BNeawe')
			engine.say(con[0].text)
			engine.say("Its"+con[3].text+'outside')
			engine.say(con[5].text)
		elif 'meaning of' in ques:
			url="https://www.google.com/search?q="+ques
			page=requests.get(url)
			soup=BeautifulSoup(page.text,'html.parser')
			con=soup.find_all('div',attrs={'class':'BNeawe s3v9rd AP7Wnd'})
			print(con[2].text)
		elif 'what is' in ques or 'who is the' in ques or 'how is' in ques or 'which is' in ques:
			engine.say('Here are some of the results I found realted to your query')
			con=webbrowser.open('https://www.google.com/search?q='+ques)
		elif 'open menu' in ques:
			engine.say("Opening menu")
			threading.Thread(target=menu).start()
		elif 'close menu' in ques:
			engine.say("Closing menu")
			b.destroy()
		elif 'open whatsapp' in ques:
			engine.say('Opening Whatsapp')
			subprocess.Popen("C:\\Users\\vish2\\AppData\\Local\\WhatsApp\\whatsapp.exe")
		elif 'close whatsapp' in ques:
			engine.say("Closing menu")
			os.system("taskkill /F /IM whatsapp.exe")
		elif 'when' in ques:
			url="https://www.google.com/search?q="+ques
			page=requests.get(url)
			soup=BeautifulSoup(page.text,'html.parser')
			con=soup.find_all(class_='BNeawe')
			engine.say(con[1].text)
		elif 'who is' in ques:
			qu=ques.replace('who is','')
			con=wikipedia.summary(qu,sentences=3)
			engine.say(con)
		elif 'where is' in ques or 'navigate me to ' in ques or 'take me to ' in ques:
			ques=ques.replace('where is ','').replace('navigate me to ','').replace('take me to ','').replace('located','')
			con=webbrowser.open('https://www.google.com/maps?q='+ques)
			engine.say('Locating'+ques)
		elif 'goodbye' in ques or 'bye' in ques:
			engine.say('Goodbye. See you later')
			engine.runAndWait()
			playsound(deact)
			os._exit(0)
		else:
			engine.say("Sorry. Didn't get what you said")
		engine.runAndWait()

	def wake():
		with sr.Microphone() as source:
			while True:
				try:
					r.adjust_for_ambient_noise(source, duration=0.5)
					btn1.config(fg='Gold3')
					audio=r.listen(source,phrase_time_limit=5)
					text=r.recognize_google(audio).lower()
					if 'google' in text:
						threading.Thread(target=listen).start()
						break
				except:
					print("Didn't hear that")

	def onclosing():
		os._exit(0)

	#Window GUI
	btn1=Button(main,text="Say 'Ok google'",font=('ink free',20,'bold'),bd=0,bg=background,fg=foreground)
	btn1.place(relx=0.23,rely=0.915,relwidth=0.5,relheight=0.07)
	def ctime():
		ct=time.strftime("%H:%M:%S")
		lab1.config(text=ct)
		main.after(1000,ctime)
	lab1=Label(main,text='',font=('Calibri',20,'bold'),bg=background,fg=foreground)
	lab1.place(relx=0.0,rely=0.015,relwidth=0.35,relheight=0.07)
	ctime()
	lab2=Button(main,text='☰',command=menu,font=('Calibri',22),bd=0,bg=background,fg=foreground)
	lab2.place(relx=0.85,rely=0.015,relwidth=0.15,relheight=0.07)
	tb1=Text(main,font=('Calibri',18,'italic'),bd=0,bg=background,fg=foreground)
	tb1.place(relx=0.02,rely=0.7,relwidth=0.96,relheight=0.2)
	if 'cloudy' in l or 'clear' in l or 'fog' in l:
		img=PhotoImage(file="cloudy.png")
		image=Label(main, image=img)
	elif 'sunny' in l:
		img=PhotoImage(file="sunny.png")
		image=Label(main, image=img)
	elif 'rainy' in l:
		img=PhotoImage(file="rainy.png")
		image=Label(main, image=img)
	elif 'windy' in l or 'haze' in l:
		img=PhotoImage(file="windy.png")
		image=Label(main, image=img)
	elif 'snow' in l:
		img=PhotoImage(file="snow.png")
		image=Label(main, image=img)
	else:
		image=Label(main,text='- -',font=('Calibri',30,'bold'),bg=background,fg=foreground)
	image.place(relx=0.02,rely=0.2,relwidth=0.5,relheight=0.3)
	weather=Label(main,text=loc[0].replace(',','')+'\n'+temp+'\n'+weat,font=('Calibri',18,'italic'),bg=background,fg=foreground)
	weather.place(relx=0.52,rely=0.2,relwidth=0.5,relheight=0.3)

	main.geometry("375x640+550+75")
	main.resizable(0,0)
	main.config(bg=background)
	main.title('Personal Assistant')
	threading.Thread(target=wish).start()
	main.protocol("WM_DELETE_WINDOW",onclosing)
	main.mainloop()

except:
	messagebox.showerror(title="Error",message='No Internet Connection\nPlease relaunch application after connecting to internet')
