from tkinter import *
from tkinter import font as tkFont
from datetime import datetime
from datetime import timedelta


class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.theCanvas = Canvas(self, width=1300,height=700, bg="#AAAAFF") 
        self.theCanvas.grid(row=0, column=0, rowspan=2, columnspan=2)   
        self.bigFont = tkFont.Font(family = "Helvetica",size = 80,weight = "bold")
        self.examtitle = tkFont.Font(family = "Helvetica",size = 40,weight = "bold")
        self.examfont = tkFont.Font(family = "Helvetica",size = 22)

        self.readTimes()
        # self.exams.append(["Test", "23/05/2022 20:00:00", "23/5/2022 20:55:00"])
        # self.exams.append(["Latin", "24/05/2022 09:55:00", "24/5/2022 10:55:00"])
        # self.exams.append(["Computer Science", "24/05/2022 11:20:00", "24/5/2022 12:05:00"])
        # self.exams.append(["French Listening", "24/05/2022 12:25:00", "24/5/2022 12:55:00"])
        # self.exams.append(["Physics", "24/05/2022 14:55:00", "24/5/2022 15:55:00"])
        # self.exams.append(["Maths", "25/05/2022 09:25:00", "25/5/2022 10:55:00"])
        # self.exams.append(["History", "25/05/2022 11:40:00", "25/5/2022 12:55:00"])
        # self.exams.append(["English", "25/05/2022 14:25:00", "25/5/2022 15:55:00"])
        # self.exams.append(["Art", "26/05/2022 11:55:00", "26/5/2022 12:55:00"])
        # self.exams.append(["Biology", "26/05/2022 14:55:00", "26/5/2022 15:55:00"])
        # self.exams.append(["French Reading", "27/05/2022 09:45:00", "27/5/2022 10:10:00"])
        # self.exams.append(["French Grammar", "27/05/2022 10:20:00", "27/5/2022 10:55:00"])


        self.columnconfigure(0,minsize=600)
        self.columnconfigure(1,minsize=700)
        self.rowconfigure(0,minsize=300)
        self.adjustFrame = Frame(self, bg="#ddddff")
        #self.adjustFrame.grid(row=1, column=1, sticky="NSEW")
        self.adjustlabel = Label(self.adjustFrame, text="Adjust start time")
        self.adjustlabel.grid(row=0, column=0, sticky="EW")
        self.editing = None
        self.update()
        self.mainloop() # this is needed to start checking for clicks

    def update(self):
        self.theCanvas.delete(ALL)
        now = datetime.now()
        # current time
        self.theCanvas.create_text(290,350,text = now.strftime("%H:%M:%S"), font=self.bigFont)
        self.after(300, self.update)

        # right pane
        self.theCanvas.create_rectangle(580,0,1300,700, fill="#FFFFFF") 
        self.theCanvas.create_text(940,50,text = "Exams", font=self.examtitle)
        days = ["Mon", "Tue","Wed","Thu","Fri","Sat"]
        examnamexpos = 610
        examtimexpos = 920
        ypos = 200
        for examnum in range(len(self.exams)):
            e = self.exams[examnum]
            examstart =  datetime.strptime(e[1],"%d/%m/%Y %H:%M:%S")
            examend = datetime.strptime(e[2],"%d/%m/%Y %H:%M:%S")
            if examend + timedelta(minutes=5) < now : # finished
                continue
            elif examstart > now: # not started
                starttime = ""
                if examstart.weekday() != now.weekday():
                    starttime += days[examstart.weekday()] + " "
                starttime += str(examstart.hour) + ":" + str(examstart.minute)
                self.theCanvas.create_text(examnamexpos, ypos, text = e[0], anchor="nw", font = self.examfont)
                self.theCanvas.tag_bind(self.theCanvas.create_text(examtimexpos, ypos, text = "starts " + starttime, anchor="nw", font = self.examfont), "<Button-1>", lambda event,x=examnum: self.adjust(x))
                
            else:
                self.theCanvas.create_text(examnamexpos, ypos, text = e[0], anchor="nw", font = self.examfont)
                if examend < now:
                    hoursleft = 0
                    minsleft = 0
                else:
                    hoursleft = (examend - now).seconds//3600
                    minsleft = ((examend - now).seconds%3600)//60
            
                timeleft = "Time left: "
                if hoursleft >0:
                    timeleft += str(hoursleft) + " hour"
                    if hoursleft >1:
                        timeleft += "s"
                    timeleft += ", "
                timeleft += str(minsleft) + " min"
                if minsleft >1 or minsleft ==0:
                    timeleft +="s"
                if hoursleft ==0 and minsleft < 5:
                   textcolour = "#FF0000"
                else:
                    textcolour = "#000000"
                if hoursleft ==0 and minsleft ==0:
                    if examend < now:
                        timeleft = "ended "
                    else:
                        timeleft = "ending "
                    timeleft += str(examend.hour) + ":" + "{:02d}".format(examend.minute)
 
                self.theCanvas.tag_bind(self.theCanvas.create_text(examtimexpos, ypos, text = timeleft, anchor="nw", font = self.examfont, fill=textcolour), "<Button-1>", lambda event,x=examnum: self.adjust(x))
            ypos += 100
            if self.editing is not None:
                self.theCanvas.create_rectangle(0,500,580,700, fill="yellow")
                self.theCanvas.create_text(10,550, text="Adusting " + self.exams[self.editing][0], font = self.examfont, anchor="nw")
                self.theCanvas.create_text(10,600, text="Current Start: " + self.exams[self.editing][1], font = self.examfont, anchor="nw")
                self.theCanvas.tag_bind(self.theCanvas.create_text(200,650, text="  +  ", font = self.examtitle, anchor="nw"),"<Button-1>", self.addtime)
                self.theCanvas.tag_bind(self.theCanvas.create_text(100,650, text="  -  ", font = self.examtitle, anchor="nw"),"<Button-1>", self.removetime)
                self.theCanvas.tag_bind(self.theCanvas.create_text(300,650, text="DONE", font = self.examtitle, anchor="nw"),"<Button-1>", self.stopadjusting)

    def addtime(self,e):
        examstart =  datetime.strptime(self.exams[self.editing][1],"%d/%m/%Y %H:%M:%S")
        examend =  datetime.strptime(self.exams[self.editing][2],"%d/%m/%Y %H:%M:%S")
        examend += timedelta(minutes=1)
        examstart += timedelta(minutes=1)
        self.exams[self.editing][1] = datetime.strftime(examstart, "%d/%m/%Y %H:%M:%S" )       
        self.exams[self.editing][2] = datetime.strftime(examend, "%d/%m/%Y %H:%M:%S" )       

    def removetime(self,e):
        examstart =  datetime.strptime(self.exams[self.editing][1],"%d/%m/%Y %H:%M:%S")
        examend =  datetime.strptime(self.exams[self.editing][2],"%d/%m/%Y %H:%M:%S")
        examend -= timedelta(minutes=1)
        examstart -= timedelta(minutes=1)
        self.exams[self.editing][1] = datetime.strftime(examstart, "%d/%m/%Y %H:%M:%S" )       
        self.exams[self.editing][2] = datetime.strftime(examend, "%d/%m/%Y %H:%M:%S" )       

    def stopadjusting(self,e):
        self.editing = None
        self.writeTimes()

    def adjust(self,examnum):
        self.editing = examnum

    def writeTimes(self):
        f = open("examtimes.txt","w")
        for e in self.exams:
            f.write(e[0]+"-"+e[1]+"-"+e[2]+"\n")
        f.close()

    def readTimes(self):
        f = open("examtimes.txt","r")
        self.exams = []
        for line in f:
            self.exams.append(line.strip().split("-"))
        f.close()


if __name__ == "__main__":
    app = App()