#! /usr/bin/python

import Image, ImageDraw, ImageTk
import Tkinter, subprocess, time

class temp_gui:
    def __init__(self):
        self.root = Tkinter.Tk()
        self.width = 320
        self.height = 240
        self.root.geometry('%dx%d+%d+%d' % (self.width, self.height, 0,0))
        #self.root.overrideredirect(1)  #take off title bar
	self.splash_wait = 3

	self.backgnd_pic['splash_screen'] = "/home/pi/photo_booth/start_screen.png"
	self.backgnd_pic['main_screen'] = "/home/pi/photo_booth/preview.png"
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

        self.preview_pic_button = Tkinter.Button(self.frame['preview'],cursor="none")
        self.preview_pic_button.config(command = self.quit_photo_booth)
        self.preview_pic_button.place(width = 420, height = 280, relx = 0.44, rely = 0.04)
        
        self.snap_pic_button = Tkinter.Button(self.frame['preview'])
        self.snap_pic_button.config(command = self.show_3)
        self.snap_pic_button.config(cursor="none",text="Take a picture", font=("Century Schoolbook L",20))
        self.snap_pic_button.place(width = 250, height = 150, relx = 0.55, rely = 0.6)

    def show_splash_screen(self):
        self.frame['splash_screen'].lift()
	self.root.update()
	time.sleep(self.splash_wait)

    def show_main_screen(self):
        self.frame['main_screen'].lift()

top = temp_gui()
top.root.mainloop()