import matplotlib
matplotlib.use("TKAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib import pyplot as plt
from matplotlib import style


import sqlite3
# import mainprocess
import pandas as pd

from PIL import Image,ImageTk

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

title_font = ("Times New Roman",50,'bold')
subtitle_font = ("Times New Roman",20,'bold')
large_font = {"Times New Roman":15}
style.use('ggplot')
indexlist = ['SP500','CPI','CCI','USD','UR','FFR','VIX','clear']

# def dataupdate():
#     mainprocess.main()

def plotdata():        
    db = sqlite3.connect('us_finance.sqlite')
    cur = db.cursor()
    data = cur.execute("""SELECT * FROM plot""").fetchall()
    db.close()
    data = pd.DataFrame(data,columns=['DATE','SP500','USD','VIX','FFR','CCI','CPI','UR'])
    return data

def popupmsg(msg):
    messagebox.showwarning('ERROR', msg)

def tut(index):
    db = sqlite3.connect('us_finance.sqlite')
    cur = db.cursor()
    data = cur.execute("""SELECT * FROM tut""").fetchall()
    db.close()
    return data[index][1]

def destroyWidget(container):
    container.destroy()

def indextut(index,perent):
    perent.destroy()
    pop = tk.Tk()
    pop.geometry('700x250')
    pop.title('Tutorial')
    l1 = tk.Label(pop,text=indexlist[index],height=1,bg='white',width=100)
    l1.pack(side='top')
    # l1.place(anchor='nw',x=0,y=0)
    l2 = tk.Label(pop,text=tut(index),background='skyblue',width=100,wraplength=700,justify='left')
    l2.pack(side='top')
    # l2.place(anchor='nw',x=0,y=20)
    
    if index == 0:
        btn1 = tk.Button(pop,text='Next',width=10,command = lambda:indextut(index+1,pop))
        btn2 = tk.Button(pop,text='Quit',width=10,command = lambda:destroyWidget(pop)) #
        btn1.place(anchor='nw',x=240,y=200)
        btn2.place(anchor='nw',x=360,y=200)
    elif index == 6:
        btn1 = ttk.Button(pop,text='Prev',width=10,command = lambda:indextut(index-1,pop))
        btn2 = ttk.Button(pop,text='Quit',width=10,command = lambda:destroyWidget(pop))
        btn1.place(anchor='nw',x=240,y=200)
        btn2.place(anchor='nw',x=360,y=200)
    else:
        btn0 = ttk.Button(pop,text='Next',width=10,command = lambda:indextut(index+1,pop))
        btn1 = ttk.Button(pop,text='Prev',width=10,command = lambda:indextut(index-1,pop))
        btn2 = ttk.Button(pop,text='Quit',width=10,command = lambda:destroyWidget(pop))
        btn0.place(anchor='nw',x=180,y=200)
        btn1.place(anchor='nw',x=300,y=200)
        btn2.place(anchor='nw',x=420,y=200)
    pop.mainloop()

class USfinance(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) #本行意義即為，self = Tk() 
        self.geometry('1200x800') 
        self.iconbitmap(self,'icon.ico') #設定程式圖樣
        self.title('US Finance Observation') #設定程式名稱


        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(container)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label='save settings', command= lambda: popupmsg("Not suppoerted just yet!"))
        filemenu.add_separator()
        filemenu.add_command(label='exit', command=quit)
        menubar.add_cascade(label='File', menu=filemenu)

        datamenu = tk.Menu(menubar, tearoff=1)
        datamenu.add_command(label='data update', command= lambda: popupmsg("Not suppoerted just yet!"))
        menubar.add_cascade(label='data', menu=datamenu)

        tutmenu = tk.Menu(menubar, tearoff=1)
        tutmenu.add_command(label='Index Tutorial', command = lambda: indextut(0,tk.Tk()))
        menubar.add_cascade(label='Help', menu=tutmenu)

        tk.Tk.config(self, menu=menubar)        

        self.frames = {}
        for i in [StartPage,PageGraph1,PageGraph2]: #,PageOne,Page2,TestPage
            frame = i(container, self)
            self.frames[i] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)
    
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

# def qf(param):
#     print(param)
# lambda: qf('666')

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        label1 = tk.Label(self, text="US Economic Observations", font=title_font)
        label1.pack(pady=10, padx=10)
        label2 = tk.Label(self, text="Plotting Chart Application", font=subtitle_font)
        label2.pack(pady=10, padx=10)
        label6 = tk.Label(self, text="How Many Lines Overlap on Your Chart ?", font=large_font)
        label6.pack(pady=10, padx=10)
        
        # btn1 = ttk.Button(self, text='Test', command=lambda: controller.show_frame(TestPage))
        # btn1.pack()

        btn2 = ttk.Button(self, text='1', command=lambda: controller.show_frame(PageGraph1))
        btn2.place(x=440,y=225,anchor='nw')
        btn3 = ttk.Button(self, text='2', command=lambda: controller.show_frame(PageGraph2))
        btn3.place(x=550,y=225,anchor='nw')
        btn3 = ttk.Button(self, text='Quit', command=quit)
        btn3.place(x=660,y=225,anchor='nw')

        fr = tk.Canvas(self,border=10,width=1100,height=400)#,bg='white'

        load1 = Image.open('test.png')
        load2 = Image.open('test2.png')
        load3 = Image.open('test3.png')
        img1 = ImageTk.PhotoImage(load1)
        img2 = ImageTk.PhotoImage(load2)
        img3 = ImageTk.PhotoImage(load3)

        label3 = tk.Label(fr,image=img3)
        label3.image = img3
        label4 = tk.Label(fr,image=img1)
        label4.image = img1
        label5 = tk.Label(fr,image=img2)
        label5.image = img2
        

        label3.place(x=50,y=50,anchor='nw')
        label4.place(x=750,y=50,anchor='nw')
        label5.place(x=750,y=250,anchor='nw')
        
        fr.place(x=50,y=250,anchor='nw')#side="bottom", expand = True, fill="x"
# def pr():
#     print('5655646')
        
# class TestPage(tk.Frame):

#     def __init__(self, parent, controller):
#         super().__init__(parent)
#         btn = ttk.Button(self, text="back", command=lambda: controller.show_frame(StartPage))
#         btn.grid()
#         btn2 = ttk.Button(self, text='print', command=pr)#lambda:
#         btn2.grid()
#         btn3 = ttk.Button(self, text='print', command=lambda:pr())#
#         btn3.grid()
        
# class PageOne(tk.Frame):
#     def __init__(self, parent, controller):
#         super().__init__(parent)
#         label = tk.Label(self, text="Page 1", font=large_font)
#         label.pack(pady=10, padx=10)

#         btn1 = ttk.Button(self, text='Back To Home', command=lambda: controller.show_frame(StartPage))
#         btn1.pack()
#         btn2 = ttk.Button(self, text='Visit Page 2', command=lambda: controller.show_frame(Page2))
#         btn2.pack()
#         btn3 = ttk.Button(self, text='Visit Page Graph', command=lambda: controller.show_frame(PageGraph))
#         btn3.pack()
    
class PageGraph1(tk.Frame):
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = tk.Label(self, text="Page Graph", font=large_font)
        label.pack(pady=10, padx=10)

        self.data = plotdata()

        btn1 = ttk.Button(self, text='Back To Home', command=lambda: controller.show_frame(StartPage))
        btn1.pack()
        btn2 = ttk.Button(self, text='I Want Two Lines!', command=lambda: controller.show_frame(PageGraph2))
        btn2.pack()
        cb1 = ttk.Combobox(self, values=indexlist)
        cb1.current(0)
        cb1.pack()
        btn3 = ttk.Button(self, text='OK', command=lambda:self.plot(cb1.get())) #
        btn3.pack()
        # btn3.bind('<Button-1>',self.plot(cb1.get()))
        
        self.f = plt.figure(figsize=(16,8),clear=True)
        self.subplot1 = self.f.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.f, self)
        toolbar = NavigationToolbar2Tk(self.canvas, self)
        toolbar.update()
        toolbar.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=0)

    def plot(self,a):
        print(a)
        try:
            self.subplot1.clear()
        except: pass
            
        try:
            # self.f,ax = plt.subplots(figsize=(16,8),clear=True)
            self.subplot1.plot(self.data['DATE'],self.data[a],color='r',label=a)
            self.subplot1.legend()
            self.subplot1.set_xlabel('year',fontsize=16)
            self.subplot1.set_xticks([250*i for i in range(-1,19,1)],[2004+i for i in range(20)])
            self.subplot1.set_ylabel(a,fontsize=16)
            self.subplot1.set_title(a,fontsize=22)  
            self.canvas.draw() # show----->draw
        except:
            self.canvas.draw()
            return

class PageGraph2(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = tk.Label(self, text="Page Graph", font=large_font)
        label.pack(pady=10, padx=10)

        btn1 = ttk.Button(self, text='Back To Home', command=lambda: controller.show_frame(StartPage))
        btn1.pack()       
        btn2 = ttk.Button(self, text='I Want One Line!', command=lambda: controller.show_frame(PageGraph1))
        btn2.pack()
        cb1 = ttk.Combobox(self, values=indexlist)
        cb1.pack()
        cb1.current(0)
        cb2 = ttk.Combobox(self, values=indexlist)
        cb2.pack()
        cb2.current(1)
        btn3 = ttk.Button(self, text='OK', command=lambda:self.plot(cb1.get(),cb2.get()))
        btn3.pack()

        self.data = plotdata()

        self.f = plt.figure(figsize=(16,8),clear=True)
        self.subplot1 = self.f.add_subplot(111)
        self.ax2 = self.subplot1.twinx()
        self.canvas = FigureCanvasTkAgg(self.f, self)
        # self.canvas.draw() # show----->draw
        toolbar = NavigationToolbar2Tk(self.canvas, self)
        toolbar.update()
        toolbar.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True) #

    def plot(self,a,b):
        print(a+'&'+b)
        try:
            self.f.clear()
            self.subplot1 = self.f.add_subplot(111)
            self.ax2 = self.subplot1.twinx()
        except: pass

        try:
            self.subplot1.plot(self.data['DATE'],self.data[a],color='r',label=a,linewidth=1) 
            self.subplot1.set_ylabel(a,fontsize=16)
            self.subplot1.tick_params(axis='y')
            
            self.ax2.plot(self.data['DATE'],self.data[b],color='g',label=b,linewidth=1)
            self.ax2.set_ylabel(b,fontsize=16)
            self.ax2.tick_params(axis='y')
            self.f.legend(loc=2, bbox_to_anchor=(0,1), bbox_transform=self.ax2.transAxes)
            self.subplot1.set_xticks([250*i for i in range(-1,19,1)],[2004+i for i in range(20)])
            self.subplot1.set_title(a + " & " + b + " compare ",fontsize=22)
            self.canvas.draw()
        except:
            self.canvas.draw()
        

        
        


app = USfinance()

app.mainloop()
