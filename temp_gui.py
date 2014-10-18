#! /usr/bin/python

import Image, ImageDraw, ImageTk
import Tkinter, subprocess, threading, Queue
#import time
import temp_control, wiringpi2

class temp_loop(threading.Thread):
    def __init__(self, queue_set, queue_read):
	threading.Thread.__init__(self)
	self.queue_set = queue_set
	self.queue_read = queue_read
	self.temp_controller = temp_control.temp_control()
	self.run_temp_control = 1
	self.count = 0
	self.temp_set = 25
	self.temp_read = 25

    def run(self):
	while self.run_temp_control:
		#time.sleep(0.001)
		wiringpi2.delay(100)
		if self.queue_set.empty() != True:
			temp = self.queue_set.get(0)
			if temp == -100:
				self.run_temp_control = 0
			else:
				self.temp_set = int(temp) 
		
		#self.temp_read = self.temp_set + 2
		self.temp_read = self.temp_controller.read_thermo_temp()
		self.temp_controller.regulate_temp(self.temp_set, self.temp_read)		
		wiringpi2.delay(100)
		self.queue_read.put(self.temp_read)

class temp_gui:
    def __init__(self):
        self.root = Tkinter.Tk()
        self.width = 320
        self.height = 240
        self.root.geometry('%dx%d+%d+%d' % (self.width, self.height, 0,0))
        self.root.overrideredirect(1)  #take off title bar
	self.splash_wait = 3000
	self.queue_set = Queue.Queue()
	self.queue_set.LifoQueue = 1
	self.queue_read = Queue.Queue()
	self.queue_read.LifoQueue = 1
	self.thread = temp_loop(self.queue_set, self.queue_read)
	self.temp_setting = 25
	self.read_temp = 25

        self.frame = {}
        self.frame['splash_screen'] = Tkinter.Frame(self.root,cursor="none")
        self.frame['main_screen'] = Tkinter.Frame(self.root,cursor="none")
        self.button = {}
        self.panel = {}
        self.tk_backgnd_pic = {}
	self.backgnd_pic = {}
	self.backgnd_pic['splash_screen'] = "/home/pi/temp_control/bird.png"
	#self.backgnd_pic['splash_screen'] = "/home/joe/Documents/temp_control/bird.png"
	self.backgnd_pic['main_screen'] = "/home/pi/temp_control/bird.png"
	#self.backgnd_pic['main_screen'] = "/home/joe/Documents/temp_control/bird.png"
	self.configure_panel('splash_screen')
	self.configure_main()
	self.show_splash_screen()

    def configure_panel(self, screen):
        self.frame[screen].place(width = self.width, height = self.height, relx = 0, rely = 0)
        self.panel[screen] = Tkinter.Label(self.frame[screen])
        picture = Image.open(self.backgnd_pic[screen])
        self.tk_backgnd_pic[screen] = ImageTk.PhotoImage(picture)
        self.panel[screen].configure(image = self.tk_backgnd_pic[screen])
        self.panel[screen].place(width = self.width, height = self.height, relx = 0, rely = 0)

    def configure_main(self):
        self.configure_panel('main_screen')

	self.scale = Tkinter.Scale(self.frame['main_screen'],cursor="none", from_ = 25, to = 150)
	self.scale.config(command=self.set_set_temp, orient="horizontal")
	self.scale.place(width = 250, height = 100, relx = 0.15, rely = 0.6)        

        self.quit_button = Tkinter.Button(self.frame['main_screen'])
        self.quit_button.config(command = self.quit)
        self.quit_button.config(cursor="none",text="Quit", font=("Century Schoolbook L",20))
        self.quit_button.place(width = 100, height = 50, relx = 0.7, rely = 0.1)

	self.entry_read = Tkinter.Entry(self.frame['main_screen'],cursor="none")
        self.entry_read.config(cursor="none",font=("Century Schoolbook L",20))
        self.entry_read.place(width = 100, height = 50, relx = 0.05, rely = 0.1)
	self.entry_read.insert(0, self.read_temp)

	self.entry_set = Tkinter.Entry(self.frame['main_screen'],cursor="none")
        self.entry_set.config(cursor="none", font=("Century Schoolbook L",20))
        self.entry_set.place(width = 100, height = 50, relx = 0.35, rely = 0.1)
	self.entry_set.insert(0, self.temp_setting)

    def show_splash_screen(self):
        self.frame['splash_screen'].lift()
	self.root.update()
	#time.sleep(self.splash_wait/1000)
	wiringpi2.delay(self.splash_wait)
	self.show_main_screen()

    def show_main_screen(self):
        self.frame['main_screen'].lift()
	self.start_temp()
	self.root.after(2000, self.update_read_temp)

    def update_read_temp(self):
	while self.queue_read.empty() != True:
		temp = self.queue_read.get(0)
	self.read_temp = temp
	self.entry_read.delete(0, Tkinter.END)
	self.entry_read.insert(0, self.read_temp)
	self.root.after(2000, self.update_read_temp)

    def set_set_temp(self, value):
	self.queue_set.put(value)
	self.temp_setting = value
	self.entry_set.delete(0, Tkinter.END)
	self.entry_set.insert(0, self.temp_setting)

    def start_temp(self):
	self.thread.run_temp_control = 1
	self.queue_set.put(self.temp_setting)
	self.thread.start()

    def quit(self):
	self.queue_set.put(-100)
	self.root.destroy()

top = temp_gui()
top.root.mainloop()
