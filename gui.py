from Tkinter import *


class App(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        self.pack()
        self.button = Button(self, text='QUIT', fg='red', command=self.quit)
        self.button.pack(side=LEFT)

        self.hi_there = Button(self, text='Hello', command=self.say_hi)
        self.hi_there.pack(side=LEFT)

    def say_hi(self):
        print 'hi there!'

root = Tk()

app = App(root)

app.mainloop()
