import tkinter as tk

running = False
hours, minutes, seconds, milliseconds = 0, 0, 0, 0

def start():
    global running
    if not running:
        update()
        running = True

def lap():
    global running
    if not running:
        update()
        running = True
        
def pause():
    global running
    if running:
        stopwatch_label.after_cancel(update_time)
        running = False

def reset():
    global running
    if running:
        stopwatch_label.after_cancel(update_time)
        running = False
    global hours, minutes, seconds, milliseconds
    hours, minutes, seconds, milliseconds = 0, 0, 0, 0
    stopwatch_label.config(text='00:00:00:00')

def update():
    global hours, minutes, seconds, milliseconds
    milliseconds += 1
    if milliseconds == 100:
        seconds += 1
        milliseconds = 0
    if seconds == 60:
        minutes += 1
        seconds = 0
    if minutes == 60:
        hours += 1
        minutes = 0
    hours_string = f'{hours}' if hours > 9 else f'0{hours}'
    minutes_string = f'{minutes}' if minutes > 9 else f'0{minutes}'
    seconds_string = f'{seconds}' if seconds > 9 else f'0{seconds}'
    milliseconds_string = f'{milliseconds}' if milliseconds > 9 else f'0{milliseconds}'
    stopwatch_label.config(text=hours_string + ':' + minutes_string + ':' + seconds_string + ':' + milliseconds_string)
    global update_time
    update_time = stopwatch_label.after(8, update)

root = tk.Tk()
root.geometry('485x220')
root.title('Stopwatch')
from tkinter import *
import time

class StopWatch(Frame):  
    """ Implements a stop watch frame widget. """                                                                
    def __init__(self, parent=None, **kw):        
        Frame.__init__(self, parent, kw)
        self.saved = [ ]
        self._start = 0.0        
        self._elapsedtime = 0.0
        self._running = 0
        self.timestr = StringVar()
        #self.lapstr = StringVar()
        self.e = 0
        self.m = 0
        self.makeWidgets()
        self.laps = []
        n = 0
        self.lapmod2 = 0
        self.today = time.strftime("%d %b %Y %H-%M-%S", time.localtime())
        
    def makeWidgets(self):                         
        """ Make the time label. """
        l1 = Label(self, text='----File Name----')
        l1.pack(fill=X, expand=NO, pady=1, padx=2)

        self.e = Entry(self)
        self.e.pack(pady=2, padx=2)
        
        l = Label(self, textvariable=self.timestr)
        self._setTime(self._elapsedtime)
        l.pack(fill=X, expand=NO, pady=3, padx=2)

        l2 = Label(self, text='----Laps----')
        l2.pack(fill=X, expand=NO, pady=4, padx=2)

        scrollbar = Scrollbar(self, orient=VERTICAL)
        self.m = Listbox(self,selectmode=EXTENDED, height = 5,
                         yscrollcommand=scrollbar.set)
        self.m.pack(side=LEFT, fill=BOTH, expand=1, pady=5, padx=2)
        scrollbar.config(command=self.m.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
   
    def _update(self): 
        """ Update the label with elapsed time. """
        self._elapsedtime = time.time() - self._start
        self._setTime(self._elapsedtime)
        self._timer = self.after(50, self._update)
    
    def _setTime(self, elap):
        """ Set the time string to Minutes:Seconds:Hundreths """
        minutes = int(elap/60)
        seconds = int(elap - minutes*60.0)
        hseconds = int((elap - minutes*60.0 - seconds)*100)                
        self.timestr.set('%02d:%02d:%02d' % (minutes, seconds, hseconds))

    def _setLapTime(self, elap):
        """ Set the time string to Minutes:Seconds:Hundreths """
        self.saved.append(self.timestr)
        num = len(self.saved)
        minutes = int(elap/60)
        seconds = int(elap - minutes*60.0)
        hseconds = int((elap - minutes*60.0 - seconds)*100)            
        return f'T#{num} - ' + '%02d:%02d:%02d' % (minutes, seconds, hseconds) + ' +%02d:%02d:%02d' % (minutes, seconds, hseconds)
        
        
    def Start(self):                                                     
        if not self._running:            
            self._start = time.time() - self._elapsedtime
            self._update()
            self._running = 1        
    
    def Stop(self):                                    
        if self._running:
            self.after_cancel(self._timer)            
            self._elapsedtime = time.time() - self._start    
            self._setTime(self._elapsedtime)
            self._running = 0
    
    def Reset(self):                                  
        self._start = time.time 
        self._elapsedtime = 0.0
        self.laps = []
        self.lapmod2 = self._elapsedtime
        self._setTime(self._elapsedtime)

    def Lap(self):
        tempo = self._elapsedtime - self.lapmod2
        if self._running:
            self.laps.append(self._setLapTime(tempo))
            self.m.insert(END, self.laps[-1])
            self.m.yview_moveto(1)
            self.lapmod2 = self._elapsedtime
       
    def GravaCSV(self):
        arquivo = str(self.e.get()) + ' - '
        with open(arquivo + self.today + '.txt', 'wb') as lapfile:
            for lap in self.laps:
                lapfile.write((bytes(str(lap) + '\n', 'utf-8')))
            
def main():
    root = Tk()
    root.wm_attributes("-topmost", 1)     
    sw = StopWatch(root)
    sw.pack(side=TOP)

    Button(root, text='Lap', command=sw.Lap).pack(side=LEFT)
    Button(root, text='Start', command=sw.Start).pack(side=LEFT)
    Button(root, text='Stop', command=sw.Stop).pack(side=LEFT)
    Button(root, text='Reset', command=sw.Reset).pack(side=LEFT)
    Button(root, text='Save', command=sw.GravaCSV).pack(side=LEFT)
    Button(root, text='Quit', command=root.quit).pack(side=LEFT)    
    
    root.mainloop()

if __name__ == '__main__':
    main()
stopwatch_label = tk.Label(text='00:00:00:00', font=('Arial', 60))
stopwatch_label.pack()

start_button = tk.Button(text='start', height=2, width=6,font=('Arial', 16), command=start)
start_button.pack(side=tk.LEFT)
pause_button = tk.Button(text='pause', height=2, width=6, font=('Arial', 16), command=pause)
pause_button.pack(side=tk.LEFT)
lap_button = tk.Button(text='lap', height=2, width=6, font=('Arial', 16), command=lap)
lap_button.pack(side=tk.LEFT)
reset_button = tk.Button(text='reset', height=2, width=6, font=('Arial', 16), command=reset)
reset_button.pack(side=tk.LEFT)
quit_button = tk.Button(text='quit', height=2, width=6, font=('Arial', 16), command=root.quit)
quit_button.pack(side=tk.LEFT)

root.mainloop()
