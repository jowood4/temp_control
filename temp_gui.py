#! /usr/bin/python

import Image, ImageDraw, ImageTk
import Tkinter, subprocess, threading, Queue
#import temp_control, wiringpi2

class temp_loop(threading.Thread):
    def __init__(self, queue):
	threading.Thread.__init__(self)
	self.queue = queue
	self.temp_controller = temp_control.temp_control()
	self.temp_setting = 25
	self.read_temp = 25
	self.run_temp_control = 1

    def set_entry(self, entry):
	self.entry_read = entry
	self.entry_read.insert(0, self.temp_setting)
	
    def update_read_temp(self):
	self.entry_read.delete(0, Tkinter.END)
	self.entry_read.insert(0, self.read_temp)

    def run(self):
	#print self.read_temp
	while self.run_temp_control:
		if self.queue.empty() != True:
			temp = self.queue.get(0)
			print temp
			if temp == -100:
				self.run_temp_control = 0
			else:
				self.temp_setting = temp 

		self.read_temp = self.temp_controller.read_thermo_temp()
		self.temp_controller.regulate_temp(self.temp_setting, self.read_temp)
		self.update_read_temp()		
		wiringpi2.delay(100)

class temp_gui:
    def __init__(self):
        self.root = Tkinter.Tk()
        self.width = 320
        self.height = 240
        self.root.geometry('%dx%d+%d+%d' % (self.width, self.height, 0,0))
        #self.root.overrideredirect(1)  #take off title bar
	self.splash_wait = 3000
	self.queue = Queue.Queue()
	self.thread = temp_loop(self.queue)

        self.frame = {}
        self.frame['splash_screen'] = Tkinter.Frame(self.root,cursor="none")
        self.frame['main_screen'] = Tkinter.Frame(self.root,cursor="none")
        self.button = {}
        self.panel = {}
        self.tk_backgnd_pic = {}
	#self.backgnd_pic = {}
	#self.backgnd_pic['splash_screen'] = "/home/pi/photo_booth/start_screen.png"
	#self.backgnd_pic['main_screen'] = "/home/pi/photo_booth/preview.png"
	self.configure_panel('splash_screen')
	self.configure_main()
	self.show_splash_screen()

    def configure_panel(self, screen):
        self.frame[screen].place(width = self.width, height = self.height, relx = 0, rely = 0)
        self.panel[screen] = Tkinter.Label(self.frame[screen])
        #picture = Image.open(self.backgnd_pic[screen])
        #self.tk_backgnd_pic[screen] = ImageTk.PhotoImage(picture)
        #self.panel[screen].configure(image = self.tk_backgnd_pic[screen])
        self.panel[screen].place(width = self.width, height = self.height, relx = 0, rely = 0)

    def configure_main(self):
        self.configure_panel('main_screen')

        self.up_button = Tkinter.Button(self.frame['main_screen'],cursor="none")
        self.up_button.config(command = self.increase)
	self.up_button.config(cursor="none",text="Up", font=("Century Schoolbook L",20))
        self.up_button.place(width = 100, height = 50, relx = 0.6, rely = 0.1)
        
        self.down_button = Tkinter.Button(self.frame['main_screen'])
        self.down_button.config(command = self.decrease)
        self.down_button.config(cursor="none",text="Down", font=("Century Schoolbook L",20))
        self.down_button.place(width = 100, height = 50, relx = 0.6, rely = 0.4)
        
        self.quit_button = Tkinter.Button(self.frame['main_screen'])
        self.quit_button.config(command = self.quit)
        self.quit_button.config(cursor="none",text="Quit", font=("Century Schoolbook L",20))
        self.quit_button.place(width = 100, height = 50, relx = 0.6, rely = 0.7)

	entry_read = Tkinter.Entry(self.frame['main_screen'],cursor="none")
        entry_read.config(cursor="none",font=("Century Schoolbook L",20))
        entry_read.place(width = 100, height = 50, relx = 0.1, rely = 0.3)
	self.thread.set_entry(entry_read)	

	self.entry_set = Tkinter.Entry(self.frame['main_screen'],cursor="none")
        self.entry_set.config(cursor="none", font=("Century Schoolbook L",20))
        self.entry_set.place(width = 100, height = 50, relx = 0.1, rely = 0.6)
	self.entry_set.insert(0, self.thread.temp_setting)

    def show_splash_screen(self):
        #self.frame['splash_screen'].lift()
	#self.root.update()
	#wiringpi2.delay(self.splash_wait)
	self.show_main_screen()

    def show_main_screen(self):
        self.frame['main_screen'].lift()
	self.thread.run_temp_control = 1
	self.thread.start()

    def increase(self):
	self.thread.temp_setting = self.thread.temp_setting + 1
	self.entry_set.delete(0, Tkinter.END)
	self.entry_set.insert(0, self.thread.temp_setting)
	self.queue.put(self.thread.temp_setting)

    def decrease(self):
	self.thread.temp_setting = self.thread.temp_setting - 1
	self.entry_set.delete(0, Tkinter.END)
	self.entry_set.insert(0, self.thread.temp_setting)
	self.queue.put(self.thread.temp_setting)

    def quit(self):
	self.queue.put(-100)
	#self.root.destroy()

top = temp_gui()
top.root.mainloop()
