import tkinter as tk
from tkinter import ttk
from datetime import datetime

''' TODO: Implement reading channels and programs from a database, parsing them into timeslots '''

channels = []

programs = [[1, "Prevue First!"], [1, "Prevue First!"]]
channels.append(["2\nPREVUE", programs])

programs = [[3, "The Weather Channel"]]
channels.append(["3\nWEATHER", programs])

programs = [[1, "CBS News"], [1, "The Late\nShow"], [1, "Andy\nGriffith"]]
channels.append(["4\nCBS", programs])

programs = [[1, "NBC Nightly\nNews"]]
channels.append(["5\nNBC", programs])

programs = [[2, "Connections"], [2, "Doctor Who"]]
channels.append(["7\nPBS", programs])

rowcount = len(channels)

scrollspeed = 60
scrollindex = 0
thistimeslot = 0

class Prevue(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.currenttime = tk.StringVar()
        self.currenttime.set("00:00:00")

        self.nowstr = tk.StringVar()
        self.nextstr = tk.StringVar()
        self.futurestr = tk.StringVar()
        self.lastnowstr = tk.StringVar()
        self.lastnextstr = tk.StringVar()
        self.lastfuturestr = tk.StringVar()
        self.datestr = tk.StringVar()

        self.updateTimeSlots()
        self.copyTimeSlots()

        self.mainframe = ttk.Frame(root, padding=(0), borderwidth=0, width=720, height=480)
        self.mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.columnconfigure('all', weight=0)
        self.rowconfigure('all', weight=0)

        self.header = ttk.Frame(self.mainframe, borderwidth=0, height=220, style='Header.TFrame')
        self.header.grid(column=0, row=0, columnspan=6, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.header.columnconfigure(0, weight=0, minsize=720)
        self.header.rowconfigure(0, weight=0, minsize=220)

        self.leftpad = ttk.Frame(self.mainframe, width=30)
        self.leftpad.grid(column=0, row=1, rowspan=2)

        self.timecur = ttk.Frame(self.mainframe, borderwidth=5, relief='raised', width=144, height=41, style='Clock.TFrame')
        self.timecur.grid(column=1, row=1, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.timecur.columnconfigure(0, weight=0, minsize=134)
        self.timecur.rowconfigure(0, weight=0, minsize=31)
        self.timecur.label = ttk.Label(self.timecur, textvariable=self.currenttime, padding=(0,0,5,0), style='Now.TLabel', borderwidth=0)
        self.timecur.label.grid(column=0, row=0, sticky=(tk.E, tk.S))

        self.timecanvas = tk.Canvas(self.mainframe, borderwidth=0, highlightthickness=0, yscrollincrement=1, relief='flat', width=516, height=41)
        self.timecanvas.grid(column=2, row=1, columnspan=3, sticky=(tk.N, tk.W, tk.E, tk.S))

        self.timeframe = ttk.Frame(self.timecanvas, padding=0, borderwidth=0, width=516, height=82)
        self.timeframe.columnconfigure(0, weight=0, minsize=172)
        self.timeframe.columnconfigure(1, weight=0, minsize=172)
        self.timeframe.columnconfigure(2, weight=0, minsize=172)
        self.timecanvas.create_window((0, 0), window=self.timeframe, anchor="nw", tags="self.timeframe")
        self.timeframe.bind("<Configure>", self.onFrameConfigure)

        self.lastnow = ttk.Frame(self.timeframe, borderwidth=5, relief='raised', width=172, height=41, style='Clock.TFrame')
        self.lastnow.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.lastnow.columnconfigure(0, weight=0, minsize=162)
        self.lastnow.rowconfigure(0, weight=0, minsize=31)
        self.lastnow.label = ttk.Label(self.lastnow, textvariable=self.lastnowstr, style='Clock.TLabel', borderwidth=0)
        self.lastnow.label.grid(column=0, row=0, sticky=(tk.S))

        self.lastnxt = ttk.Frame(self.timeframe, borderwidth=5, relief='raised', width=172, height=41, style='Clock.TFrame')
        self.lastnxt.grid(column=1, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.lastnxt.columnconfigure(0, weight=0, minsize=162)
        self.lastnxt.rowconfigure(0, weight=0, minsize=31)
        self.lastnxt.label = ttk.Label(self.lastnxt, textvariable=self.lastnextstr, style='Clock.TLabel', borderwidth=0)
        self.lastnxt.label.grid(column=0, row=0, sticky=(tk.S))

        self.lastfut = ttk.Frame(self.timeframe, borderwidth=5, relief='raised', width=172, height=41, style='Clock.TFrame')
        self.lastfut.grid(column=2, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.lastfut.columnconfigure(0, weight=0, minsize=162)
        self.lastfut.rowconfigure(0, weight=0, minsize=31)
        self.lastfut.label = ttk.Label(self.lastfut, textvariable=self.lastfuturestr, style='Clock.TLabel', borderwidth=0)
        self.lastfut.label.grid(column=0, row=0, sticky=(tk.S))

        self.nextnow = ttk.Frame(self.timeframe, borderwidth=5, relief='raised', width=172, height=41, style='Clock.TFrame')
        self.nextnow.grid(column=0, row=1, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.nextnow.columnconfigure(0, weight=0, minsize=162)
        self.nextnow.rowconfigure(0, weight=0, minsize=31)
        self.nextnow.label = ttk.Label(self.nextnow, textvariable=self.nowstr, style='Clock.TLabel', borderwidth=0)
        self.nextnow.label.grid(column=0, row=0, sticky=(tk.S))

        self.nextnxt = ttk.Frame(self.timeframe, borderwidth=5, relief='raised', width=172, height=41, style='Clock.TFrame')
        self.nextnxt.grid(column=1, row=1, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.nextnxt.columnconfigure(0, weight=0, minsize=162)
        self.nextnxt.rowconfigure(0, weight=0, minsize=31)
        self.nextnxt.label = ttk.Label(self.nextnxt, textvariable=self.nextstr, style='Clock.TLabel', borderwidth=0)
        self.nextnxt.label.grid(column=0, row=0, sticky=(tk.S))

        self.nextfut = ttk.Frame(self.timeframe, borderwidth=5, relief='raised', width=172, height=41, style='Clock.TFrame')
        self.nextfut.grid(column=2, row=1, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.nextfut.columnconfigure(0, weight=0, minsize=162)
        self.nextfut.rowconfigure(0, weight=0, minsize=31)
        self.nextfut.label = ttk.Label(self.nextfut, textvariable=self.futurestr, style='Clock.TLabel', borderwidth=0)
        self.nextfut.label.grid(column=0, row=0, sticky=(tk.S))

        self.rightpad = ttk.Frame(self.mainframe, width=30)
        self.rightpad.grid(column=5, row=1, rowspan=2)

        self.scrollcanvas = tk.Canvas(self.mainframe, borderwidth=0, highlightthickness=0, yscrollincrement=1, relief='flat', width=660, height=220)
        self.scrollcanvas.grid(column=1, row=2, columnspan=4, sticky=(tk.N, tk.W, tk.E, tk.S))

        self.scrollframe = ttk.Frame(self.scrollcanvas, padding=0, borderwidth=0, width=660, height=220+41+41+220+60*rowcount)
        self.scrollframe.columnconfigure(0, weight=0, minsize=144)
        self.scrollframe.columnconfigure(1, weight=0, minsize=172)
        self.scrollframe.columnconfigure(2, weight=0, minsize=172)
        self.scrollframe.columnconfigure(3, weight=0, minsize=172)
        self.scrollcanvas.create_window((0, 0), window=self.scrollframe, anchor="nw", tags="self.scrollframe")
        self.scrollframe.bind("<Configure>", self.onFrameConfigure)

        self.populate()
        self.onScrollTimer()
        self.onSecondTimer()

    def populate(self):
        self.bannerimg = tk.PhotoImage(file='prevuebanner.png')
        self.scrollbanner = ttk.Label(self.scrollframe, image=self.bannerimg, borderwidth=0)
        self.scrollbanner.grid(column=0, row=0, columnspan=4)

        self.leftnow = ttk.Frame(self.scrollframe, borderwidth=5, relief='raised', width=144, height=41, style='Clock.TFrame')
        self.leftnow.grid(column=0, row=1, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.leftnow.columnconfigure(0, weight=0, minsize=134)
        self.leftnow.rowconfigure(0, weight=0, minsize=31)

        self.listnow = ttk.Frame(self.scrollframe, borderwidth=5, relief='raised', width=172, height=41, style='Clock.TFrame')
        self.listnow.grid(column=1, row=1, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.listnow.columnconfigure(0, weight=0, minsize=162)
        self.listnow.rowconfigure(0, weight=0, minsize=31)
        self.listnow.label = ttk.Label(self.listnow, textvariable=self.nowstr, style='Clock.TLabel', borderwidth=0)
        self.listnow.label.grid(column=0, row=0, sticky=(tk.S))

        self.listnxt = ttk.Frame(self.scrollframe, borderwidth=5, relief='raised', width=172, height=41, style='Clock.TFrame')
        self.listnxt.grid(column=2, row=1, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.listnxt.columnconfigure(0, weight=0, minsize=162)
        self.listnxt.rowconfigure(0, weight=0, minsize=31)
        self.listnxt.label = ttk.Label(self.listnxt, textvariable=self.nextstr, style='Clock.TLabel', borderwidth=0)
        self.listnxt.label.grid(column=0, row=0, sticky=(tk.S))

        self.listfut = ttk.Frame(self.scrollframe, borderwidth=5, relief='raised', width=172, height=41, style='Clock.TFrame')
        self.listfut.grid(column=3, row=1, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.listfut.columnconfigure(0, weight=0, minsize=162)
        self.listfut.rowconfigure(0, weight=0, minsize=31)
        self.listfut.label = ttk.Label(self.listfut, textvariable=self.futurestr, style='Clock.TLabel', borderwidth=0)
        self.listfut.label.grid(column=0, row=0, sticky=(tk.S))

        self.leftdate = ttk.Frame(self.scrollframe, borderwidth=5, relief='raised', width=144, height=41, style='Date.TFrame')
        self.leftdate.grid(column=0, row=2, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.leftdate.columnconfigure(0, weight=0, minsize=134)
        self.leftdate.rowconfigure(0, weight=0, minsize=31)

        self.listdate = ttk.Frame(self.scrollframe, borderwidth=5, relief='raised', width=516, height=41, style='Date.TFrame')
        self.listdate.grid(column=1, row=2, columnspan=3, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.listdate.columnconfigure(0, weight=0, minsize=506)
        self.listdate.rowconfigure(0, weight=0, minsize=31)
        self.listdate.label = ttk.Label(self.listdate, textvariable=self.datestr, style='Date.TLabel', borderwidth=0)
        self.listdate.label.grid(column=0, row=0, sticky=(tk.S))

        channelrow = 3
        for channel in channels:
            channelframe = ttk.Frame(self.scrollframe, padding=0, borderwidth=5, relief='raised', width=144, height=60, style='Channel.TFrame')
            channelframe.grid(column=0, row=channelrow, sticky=(tk.N, tk.W, tk.E, tk.S))
            channelframe.columnconfigure(0, weight=0, minsize=134)
            channelframe.rowconfigure(0, weight=0, minsize=50)
            ttk.Label(channelframe, text=channel[0], justify='center', style='Channel.TLabel', padding=5).grid(row=0, column=0)

            programcolumn = 1
            programs = channel[1]
            for program in programs:
                if (programcolumn > 3):
                    break

                programwidth = program[0]

                if ((programwidth + programcolumn) > 4):
                   programwidth = 4 - programcolumn

                programframe = ttk.Frame(self.scrollframe, padding=0, borderwidth=5, relief='raised', style='Program.TFrame')
                programframe.grid(column=programcolumn, row=channelrow, columnspan=programwidth, sticky=(tk.N, tk.W, tk.E, tk.S))
                programframe.columnconfigure(0, weight=0, minsize=((programwidth*172) - 10))
                programframe.rowconfigure(0, weight=0, minsize=60)

                ttk.Label(programframe, text=program[1], style='Program.TLabel', padding=5).grid(row=0, column=0, sticky=(tk.N, tk.W))
                programcolumn += programwidth

            while (programcolumn < 4):
                programframe = ttk.Frame(self.scrollframe, padding=0, borderwidth=5, relief='raised', style='Program.TFrame')
                programframe.grid(column=programcolumn, row=channelrow, columnspan=1, sticky=(tk.N, tk.W, tk.E, tk.S))
                programframe.columnconfigure(0, weight=0, minsize=162)
                programframe.rowconfigure(0, weight=0, minsize=60)

                ttk.Label(programframe, text="No Data", style='Program.TLabel', padding=5).grid(row=0, column=0, sticky=(tk.N, tk.W))
                programcolumn += 1

            channelrow += 1

        self.listend = ttk.Frame(self.scrollframe, borderwidth=5, relief='raised', width=516, height=41, style='Footer.TFrame')
        self.listend.grid(column=0, row=channelrow, columnspan=4, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.listend.columnconfigure(0, weight=0, minsize=650)
        self.listend.rowconfigure(0, weight=0, minsize=31)
        self.listend.label = ttk.Label(self.listend, text="python prevue simulator", style='Footer.TLabel', borderwidth=0)
        self.listend.label.grid(column=0, row=0, sticky=(tk.S))

        channelrow += 1

        self.scrollbanner = ttk.Label(self.scrollframe, image=self.bannerimg, borderwidth=0)
        self.scrollbanner.grid(column=0, row=channelrow, columnspan=4)

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.scrollcanvas.configure(scrollregion=self.scrollcanvas.bbox("all"))

    def copyTimeSlots(self):
        now = datetime.now()
        timeslot = ((now.hour * 2) + int(now.minute / 30))
        thistimeslot = timeslot
        cur = datetime(year = now.year, month = now.month, day = now.day, hour = int(timeslot / 2) % 24, minute = (timeslot % 2) * 30, second = 0)
        self.lastnowstr.set(cur.strftime("%-I:%M %p"))
        timeslot += 1
        next = datetime(year = now.year, month = now.month, day = now.day, hour = int(timeslot / 2) % 24, minute = (timeslot % 2) * 30, second = 0)
        self.lastnextstr.set(next.strftime("%-I:%M %p"))
        timeslot += 1
        future = datetime(year = now.year, month = now.month, day = now.day, hour = int(timeslot / 2) % 24, minute = (timeslot % 2) * 30, second = 0)
        self.lastfuturestr.set(future.strftime("%-I:%M %p"))

    def updateTimeSlots(self):
        now = datetime.now()
        self.datestr.set(now.strftime("%A %B %-d %Y"))
        timeslot = ((now.hour * 2) + int(now.minute / 30))
        cur = datetime(year = now.year, month = now.month, day = now.day, hour = int(timeslot / 2) % 24, minute = (timeslot % 2) * 30, second = 0)
        self.nowstr.set(cur.strftime("%-I:%M %p"))
        timeslot += 1
        next = datetime(year = now.year, month = now.month, day = now.day, hour = int(timeslot / 2) % 24, minute = (timeslot % 2) * 30, second = 0)
        self.nextstr.set(next.strftime("%-I:%M %p"))
        timeslot += 1
        future = datetime(year = now.year, month = now.month, day = now.day, hour = int(timeslot / 2) % 24, minute = (timeslot % 2) * 30, second = 0)
        self.futurestr.set(future.strftime("%-I:%M %p"))

    def onScrollTimer(self):
        global scrollindex
        yvalue = self.scrollcanvas.yview()
        if (yvalue[1] == 1.0):
            self.timecanvas.yview_moveto(0.0)
            self.scrollcanvas.yview_moveto(0.0)
            scrollindex = 0

            now = datetime.now()
            timeslot = ((now.hour * 2) + int(now.minute / 30))

            if (timeslot != thistimeslot):
                self.updateTimeSlots()
        else:
            self.scrollcanvas.yview_scroll(1, "units")
            scrollindex += 1
            if ((scrollindex > 220) and (scrollindex < 220+42)):
                self.timecanvas.yview_scroll(1, "units")
            if (scrollindex == 220+42):
                self.copyTimeSlots()

        self.after(scrollspeed, self.onScrollTimer)

    def onSecondTimer(self):
        now = datetime.now()

        self.currenttime.set(now.strftime("%-I:%M:%S"))

        self.after(1000, self.onSecondTimer)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("prevue")
    root.geometry('720x480')
    root.resizable(False,False)

    s = ttk.Style()
    s.configure('TCanvas', background="#000055")
    s.configure('TFrame', background="#000055")
    s.configure('TLabel', background="#223388", font="Helvetica 18 bold")

    s.configure('Header.TFrame', background="#000000")

    s.configure('Channel.TFrame', background="#000055")
    s.configure('Channel.TLabel', background="#000055", foreground="#cccc00")

    s.configure('Program.TFrame', background="#000055")
    s.configure('Program.TLabel', background="#000055", foreground="#aaaaaa")

    s.configure('Clock.TFrame', background="#223388")
    s.configure('Clock.TLabel', background="#223388", foreground="#cccc00")

    s.configure('Date.TFrame', background="#000055")
    s.configure('Date.TLabel', background="#000055", foreground="#cccc00")

    s.configure('Footer.TFrame', background="#222222")
    s.configure('Footer.TLabel', background="#222222", foreground="#cccccc")

    s.configure('Now.TLabel', background="#223388", foreground="#aaaaaa")

    prevue = Prevue(root)

    root.mainloop()
