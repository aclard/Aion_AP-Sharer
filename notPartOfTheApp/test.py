from Tkinter import *

class A(Frame):
    def __init__(self, texte):
        Frame.__init__(self)
        Label(self, text=texte).pack()
        self.canvas = Canvas(self)
        self.canvas.pack()
        r=PhotoImage(file="ruban2.ppm")
        self.canvas.create_image(0,0,image=r)

a = A("salut")
a.mainloop()
