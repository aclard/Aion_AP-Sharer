# -*- coding: cp1252 -*-
import threading
from mtTkinter import *
from utils import *
from chatlog import *
from tkFileDialog import *
import os
from SysTrayIcon import *

global sha

class UI(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.counter = 0
        self.toplevels = []
        self.img_quit = PhotoImage(file="images/quit.gif")
        self.img_quitI = PhotoImage(file="images/quit_invert.gif")
        self.img_valid = PhotoImage(file="images/valid.gif")
        self.img_validI = PhotoImage(file="images/valid_invert.gif")
        self.img_config = PhotoImage(file="images/config.gif")
        self.img_configI = PhotoImage(file="images/config_invert.gif")
        self.img_title = PhotoImage(file="images/title.gif")
        self.img_save = PhotoImage(file="images/save.gif")
        self.img_saveI = PhotoImage(file="images/save_invert.gif")
        self.img_close = PhotoImage(file="images/close.gif")
        self.img_closeI = PhotoImage(file="images/close_invert.gif")
        self.img_browse = PhotoImage(file="images/folder.gif")
        self.img_browseI = PhotoImage(file="images/folder_invert.gif")
        self.img_bg = PhotoImage(file="images/bg.ppm")


        
        self.pseudo_canvas = Canvas(self.master, width=374, height=359, bg="red", bd=0, relief='ridge', highlightthickness=0)
        self.pseudo_canvas.place(x=0, y=0)
        self.pseudo_canvas.create_image(187,180, image = self.img_bg)

        self.pseudo_canvas.bind("<ButtonPress-1>", self.StartMove)
        self.pseudo_canvas.bind('<ButtonRelease-1>', self.StopMove)
        self.pseudo_canvas.bind('<B1-Motion>', self.OnMotion)

        self.gamepath = StringVar()
        self.e1 = Entry(self.master,textvariable=self.gamepath)
        self.e1.config(relief="flat", bd=1, highlightthickness=1, width=21)
        self.e1.insert(0,path)
        
        self.uilang = StringVar()
        self.uilang.set(lang["lang"])
        self.e2 = OptionMenu(self.master, self.uilang, "Français", "English")
        self.e2.config(bg="WHITE", width=20, bd=0, highlightthickness=1, relief='sunken')
        
        self.charname = StringVar()
        self.e3 = Entry(self.master,textvariable=self.charname)
        self.e3.config(relief="flat", bd=1, highlightthickness=1, width=21)
        #self.e3.insert(0,path)
        
        self.panel = []
        self.main_panel()

    def main_panel(self, event=None):
        for i in self.panel:
            self.pseudo_canvas.delete(i)
        self.panel = []
        self.e1.place_forget()
        self.e2.place_forget()
        self.panel.append(self.pseudo_canvas.create_image(187,176, image=self.img_title))#  0
        self.panel.append(self.pseudo_canvas.create_image(110,260, image=self.img_config))# 1
        self.panel.append(self.pseudo_canvas.create_image(187,270, image=self.img_valid))#  2
        self.panel.append(self.pseudo_canvas.create_image(265,260, image=self.img_quit))#   3
        self.panel.append(self.pseudo_canvas.create_text(187,120, text=lang["title"], font=("Gisha", 9, "bold"), fill="#515151"))#4

        self.pseudo_canvas.tag_bind(self.panel[1],'<Enter>', lambda event, item=self.panel[1], command=self.config_panel, image=self.img_configI:   self.entering_button(event,item,command,image))
        self.pseudo_canvas.tag_bind(self.panel[1],'<Leave>', lambda event, item=self.panel[1], arg=self.img_config:                                 self.leaving_button(event,item,arg))

        self.pseudo_canvas.tag_bind(self.panel[2],'<Enter>', lambda event, item=self.panel[2], command=reduce_me, image=self.img_validI:   self.entering_button(event,item,command,image))
        self.pseudo_canvas.tag_bind(self.panel[2],'<Leave>', lambda event, item=self.panel[2], arg=self.img_valid:                                 self.leaving_button(event,item,arg))

        self.pseudo_canvas.tag_bind(self.panel[3],'<Enter>', lambda event, item=self.panel[3], command=self.myquit, image=self.img_quitI:    self.entering_button(event,item,command,image))
        self.pseudo_canvas.tag_bind(self.panel[3],'<Leave>', lambda event, item=self.panel[3], arg=self.img_quit:                            self.leaving_button(event,item,arg))

    def config_panel(self,event):
        for i in self.panel:
            self.pseudo_canvas.delete(i)
        self.panel=[]
        self.e1.place(x=170, y=140)
        self.e2.place(x=170, y=170)
        self.panel.append(self.pseudo_canvas.create_text(155, 157, anchor="se", text=lang["statment2"], font=("MS Serif",12)))# 0
        self.panel.append(self.pseudo_canvas.create_image(147,280, image=self.img_save))#                                       1
        self.panel.append(self.pseudo_canvas.create_image(217,280, image=self.img_close))#                                      2
        self.panel.append(self.pseudo_canvas.create_text(155, 192, anchor="se", text=lang["statment3"], font=("MS Serif",12)))# 3
        self.panel.append(self.pseudo_canvas.create_image(314,150, image=self.img_browse))#                                     4 
        self.panel.append(self.pseudo_canvas.create_text(187,80, text=lang["config"], font=("Gisha", 19, "bold"), fill="#515151"))#5


        self.pseudo_canvas.tag_bind(self.panel[1],'<Enter>', lambda event, item=self.panel[1], command=self.config_save, image=self.img_saveI:   self.entering_button(event,item,command,image))
        self.pseudo_canvas.tag_bind(self.panel[1],'<Leave>', lambda event, item=self.panel[1], arg=self.img_save:                                self.leaving_button(event,item,arg))
        
        self.pseudo_canvas.tag_bind(self.panel[2],'<Enter>', lambda event, item=self.panel[2], command=self.main_panel, image=self.img_closeI:   self.entering_button(event,item,command,image))
        self.pseudo_canvas.tag_bind(self.panel[2],'<Leave>', lambda event, item=self.panel[2], arg=self.img_close:                               self.leaving_button(event,item,arg))

        self.pseudo_canvas.tag_bind(self.panel[4],'<Enter>', lambda event, item=self.panel[4], command=self.askfile, image=self.img_browseI:     self.entering_button(event,item,command,image))
        self.pseudo_canvas.tag_bind(self.panel[4],'<Leave>', lambda event, item=self.panel[4], arg=self.img_browse:                              self.leaving_button(event,item,arg))
        

    def switch_icon(self, event, arg, item):
        self.pseudo_canvas.itemconfigure(item, image=arg)

    def entering_button(self, event, item, command, image):
        self.pseudo_canvas.unbind("<ButtonPress-1>")
        self.pseudo_canvas.unbind('<ButtonRelease-1>')
        self.pseudo_canvas.unbind('<B1-Motion>')
                
        self.pseudo_canvas.tag_bind(item,'<ButtonRelease-1>', command)
        self.pseudo_canvas.tag_bind(item,'<ButtonPress-1>', lambda event, arg=image, item=item: self.switch_icon(event,arg,item))

    def leaving_button(self, event, item, arg):
        self.pseudo_canvas.bind("<ButtonPress-1>", self.StartMove)
        self.pseudo_canvas.bind('<ButtonRelease-1>', self.StopMove)
        self.pseudo_canvas.bind('<B1-Motion>', self.OnMotion)
        self.pseudo_canvas.tag_unbind(item, '<ButtonRelease-1>')
        self.pseudo_canvas.itemconfigure(item, image=arg)
        

    def config_save(self, event):
        global lang
        save_settings(gamefile_path=self.gamepath.get(),lang=self.uilang.get())
        lang = apply_settings()
        self.main_panel()

    def askfile(self, event=None):
        self.e1.delete(0, END)
        self.e1.insert(0, askdirectory(initialdir="C:\\", title=lang["statment4"]))

    def myquit(self, event=None):
        global parsing, bigloop
        bigloop = False
        for i in self.panel:
            self.pseudo_canvas.delete(i)
        parsing._stopevent.set( )
        self.master.quit()
        self.master.destroy()

    def create_window(self,dic):
        i=0
        a = sorted(dic.values())
        a.reverse()
        while a != []:
            for key in dic:
                if dic[key]==a[0]:
                    t = PlayerWindow(i+1,key,bg="red")
                    self.toplevels.append(t)
                    self.toplevels[i].wm_attributes("-topmost", True)
                    i+=1
                    a.pop(0)
                    break
            
    def _test(self):
        s=Sharer(1)
        s.add(1,1,lang["c_m"])
        s.add(1,1,lang["c_s"])
        s.add(1,1,lang["i_s"])
        a=PlayerWindow(1,"Dhalsim",bg="red")
        a.unwrap(s[0][0])

    def update(self,total):
        for i in range(len(self.toplevels)):
            self.toplevels[i].update(total[i])

    def unwrap(self):
        global sha
        for i in range(len(self.toplevels)):
            self.toplevels[i].unwrap(sha[-2][i])
            
    def StartMove(self,event):
        self.x = event.x
        self.y = event.y

    def StopMove(self, event):
        self.x = None
        self.y = None
        
    def OnMotion(self,event):
        try:
            x = (event.x_root - self.x - self.winfo_rootx() + self.winfo_rootx())
            y = (event.y_root - self.y - self.winfo_rooty() + self.winfo_rooty())
            self.master.geometry("+%s+%s" % (x, y))
        except:
            pass #We don't care
            
class PlayerWindow(Tk):
    '''A toplevel widget with the ability to fade in'''
    def __init__(self, x, lbl, *args, **kwargs):
        global geo_y
        Tk.__init__(self)
        img = PhotoImage(file="images/ruban2.ppm")
        #self.attributes("-alpha", 0.8)
        self.geo_y = geo_y
        #background_label = Label(self, image=self.img1)
        #background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.pseudo_canvas = Canvas(self, width=185, height=85, bg="red", bd=0, relief='ridge', highlightthickness=0)
        self.pseudo_canvas.place(x=0, y=0)
        self.pseudo_canvas.create_image(92,42, image = img)
        self.pseudo_canvas.create_text(92,54, font=("MS Serif",18), text=lbl)
        self.total_ap = self.pseudo_canvas.create_text(92,25, font=("Impact",16), text=str(x)+string_position(x))
        self.attributes("-transparentcolor", "red")
        self.overrideredirect(1)
        self.geometry('185x'+str(self.geo_y)+'+'+str(x*150)+'+200')
        self.bind("<ButtonPress-1>", self.StartMove)
        self.bind('<ButtonRelease-1>', self.StopMove)
        self.bind('<B1-Motion>', self.OnMotion)
        self.ribbons = []

    def update(self,n):
        self.pseudo_canvas.itemconfig(self.total_ap, text=str(n))
        
    def StartMove(self,event):
        self.x = event.x
        self.y = event.y

    def StopMove(self, event):
        self.x = None
        self.y = None
        
    def OnMotion(self,event):
        x = (event.x_root - self.x - self.winfo_rootx() + self.winfo_rootx())
        y = (event.y_root - self.y - self.winfo_rooty() + self.winfo_rooty())
        self.geometry("+%s+%s" % (x, y))

    def unwrap(self, joueur):
        for key in joueur:
            if joueur[key] != 0:
                self.geo_y += 25
                self.geometry('185x'+str(self.geo_y))
                r=Ribbon(self, joueur[key], key)
                r.place(x=0,y=str(self.geo_y-25))
                self.ribbons.append(r)


class Ribbon(Canvas):
    def __init__(self, master, i, relic):
        Canvas.__init__(self, master=master, cnf={"width":185,"height":25, "bg":"red", "bd":0, "relief":"ridge", "highlightthickness":0})
        self.create_image(12,13, image = apbank[relic][2])
        self.create_text(27, 8, anchor="nw", font=("MS Serif",10), text="x"+str(i)+" "+relic, fill='SlateGray2')


def parser(fichier):
    global sha
    current_time = time.strftime("%Y.%m.%d %H:%M:%S", time.localtime())
    f = open(fichier+r"\Chat.log","r")
    line = f.readline()
    while line!="":
        line = f.readline()
    print "End of file"
    while not parsing._stopevent.isSet():
        line = f.readline()
        if line.find(".roll") != -1:
            print "Registering rolls..."
            dic = get_the_roll(line, f)
            sha = Sharer(len(dic))
            print "Roll sequence done. Registering AP..."
            ui.create_window(dic)
            ap_parser(line, f)

def ap_parser(line, f):
    global sha
    while not parsing._stopevent.isSet():
        lis = []
        while line.find(".ok") == -1:
            line=f.readline()
            for key in apbook:
                if line.find(key) != -1:
                    print key
                    line = line.split(" ")[-2]
                    while len(line)>=25:
                        lis.append(apbook[line[:25]])
                        line = line[25:]
        sha.share(lis) #On partage!
        t = sha.total()
        ui.update(t) #Mise à jour des toplevels
        ui.unwrap() #On développe les popups
        line = f.readline()
        print "Distribution done."

def reduce_me(event=None):
    global ui, GEOMETRY, parsing
    #os.listdir(
    if not parsing.is_alive():
        parsing.start()
    GEOMETRY = ui.master.winfo_geometry()
    hover_text = "AP Sharer"
    menu_options = (('Ouvrir', None, lambda x: None),)
    for i in ui.panel:
        ui.pseudo_canvas.delete(i)
    ui.master.quit()
    ui.master.destroy()
    SysTrayIcon("ap.ico", hover_text, menu_options, on_quit=bye)

def bye(sysTrayIcon):
    global bigloop
    bigloop=False

def main():
    global ui, geo_y, GEOMETRY
    root = Tk()
    #__________________Loading AP icons_____________________
    apbank[lang["i_i"]].append(PhotoImage(file="images/i_inf.ppm"))
    apbank[lang["i"]].append(PhotoImage(file="images/i.ppm"))
    apbank[lang["i_s"]].append(PhotoImage(file="images/i_sup.ppm"))
    apbank[lang["i_m"]].append(PhotoImage(file="images/i_maj.ppm"))
    apbank[lang["s_i"]].append(PhotoImage(file="images/s_inf.ppm"))
    apbank[lang["s"]].append(PhotoImage(file="images/s.ppm"))
    apbank[lang["s_s"]].append(PhotoImage(file="images/s_sup.ppm")) 
    apbank[lang["s_m"]].append(PhotoImage(file="images/s_maj.ppm"))
    apbank[lang["t_i"]].append(PhotoImage(file="images/t_inf.ppm"))
    apbank[lang["t"]].append(PhotoImage(file="images/t.ppm"))
    apbank[lang["t_s"]].append(PhotoImage(file="images/t_sup.ppm"))
    apbank[lang["t_m"]].append(PhotoImage(file="images/t_maj.ppm"))
    apbank[lang["c_i"]].append(PhotoImage(file="images/c_inf.ppm"))
    apbank[lang["c"]].append(PhotoImage(file="images/c.ppm"))
    apbank[lang["c_s"]].append(PhotoImage(file="images/c_sup.ppm"))
    apbank[lang["c_m"]].append(PhotoImage(file="images/c_maj.ppm"))
    #¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
    root.geometry(GEOMETRY)
    root.attributes("-transparentcolor", "red")
    root.overrideredirect(1)
    root.title("AP Sharer")
    geo_y = 85
    a = PlayerWindow(1, "Dhalsim", bg="red")
    ui = UI(master=root)
    ui.mainloop()

if __name__ == "__main__":
    GEOMETRY = '374x359+200+200'
    parsing = threading.Thread(None, parser, None, (path,))
    parsing._stopevent = threading.Event( )
    bigloop=True
    while bigloop:
        main()
    pid = os.getpid()
    os.kill(pid,15) #TERM SIGNAL
