#!/usr/bin/env python

from Tkinter import *
import serial
import time
import math

PI = 3.14159265359

#independant variable for sine waves
t = 0

#time in seconds for oscillators to wait before transmitting current positions
sine_time = 0.05 		
elapsed_time = 0

#oscillator control variables
phase = 0					
afreq = 0					  
amp = 0					
gait = 0  
knee_amp = 0

#front and back joint offsets
fk_offset = 0
bk_offset = 0
f_offset = 0					
b_offset = 0

#serial port for botboard communication
bb = serial.Serial('/dev/rfcomm0', 115200)	
print(bb.name)

#start the oscillator timer
start_time = time.time() 			

#function to obtain current time
def get_time():					      
  return time.time()

###########################################################################################################################
###################################                 OSCILLATORS                   #########################################
###########################################################################################################################

def oscillate(gselector):
  #variables which allow sine wave parameters to be changed via a gui interface
  global t, start_time, elapsed_time, f_offset, b_offset, amp, knee_amp, afreq, phase, bk_offset, fk_offset

  #array to hold the servo positions
  #positions = [SB,SF,HB,HF,EB,EF,KB,KF]
  pos = [0,1,2,3,4,5,6,7]

  #sine waves generate servo positions for each joint of the robot
  pos[0] = (int(amp) * math.sin(int(afreq)*t)) + 1500 + int(f_offset)
  pos[1] = (int(amp) * math.sin(int(afreq)*t)) + 1522 - int(f_offset)
  pos[2] = (int(amp) * math.sin(int(afreq)*t + gselector)) + 1500 + int(b_offset)
  pos[3] = (int(amp) * math.sin(int(afreq)*t + gselector)) + 1446 - int(b_offset)
 
  pos[4] = (int(amp)*float(knee_amp) * math.sin(int(afreq)*t + float(phase))) + 1500 + int(fk_offset)
  pos[5] = (int(amp)*float(knee_amp) * math.sin(int(afreq)*t + float(phase))) + 1581 - int(fk_offset)
  pos[6] = (int(amp)*float(knee_amp) * math.sin(int(afreq)*t + gselector + float(phase))) + 1500 + int(bk_offset)
  pos[7] = (int(amp)*float(knee_amp) * math.sin(int(afreq)*t + gselector + float(phase))) + 1538 - int(bk_offset)
  
  #get current time
  elapsed_time = get_time()
  
  if (elapsed_time - start_time >= sine_time):
     print ('time difference: %s' % (elapsed_time - start_time))
     start_time = elapsed_time
     t += 1

     #format servo positions properly
     for i in range(len(pos)):
       if (pos[i] < 1000):
	 pos[i] = '0' + str(int(pos[i]))

       else:
	 pos[i] = str(int(pos[i]))
     
     #transmit servo positions over serial connection
     #bb.write('%d%d%d%d%d%d%d%d\n' % (SB,SF,HB,HF,EB,EF,KB,KF))
     print('%s%s%s%s%s%s%s%s\n' % (pos[0],pos[1],pos[2],pos[3],pos[4],pos[5],pos[6],pos[7]))
     bb.write('%s%s%s%s%s%s%s%s\n' % (pos[0],pos[1],pos[2],pos[3],pos[4],pos[5],pos[6],pos[7]))
     

######################################################################################################################
##########################################        INTERMEDIATES         ##############################################
######################################################################################################################
  
#main execution loop of the program, choose gait based on number
def loop():				
  global gait
  if (gait == 1):
    gselector = PI/2
    oscillate(gselector)

  elif (gait == 2):
    gselector = -PI
    oscillate(gselector)

  elif (gait == 3):
    gselector = 0
    oscillate(gselector)
  
  root.after(int(sine_time*1000),loop)

########################################################################################################################
###########################################             GUI            #################################################
########################################################################################################################

class App:
  def __init__(self, master):
    self.frame = Frame(master)
    self.frame.pack()

    #walk button
    self.walk = Button(self.frame, text="Walk")
    self.walk.pack(side=LEFT)
    self.walk.bind("1", self.walk_button)

    #trot button
    self.trot = Button(self.frame, text="Trot")
    self.trot.bind("2", self.trot_button)
    self.trot.pack(side=LEFT)

    #pace button
    self.pace = Button(self.frame, text="Pace")
    self.pace.bind("3", self.pace_button)
    self.pace.pack(side=LEFT)
    
    #various sliders to control sine waves
    self.phase = Scale(
      master, from_=0, to=3.14, orient=HORIZONTAL, resolution=0.01, sliderlength=50,  length=200, label="Phase", command=self.set_phase)
    self.phase.set(3.14)
    self.phase.pack()

    self.amp = Scale(
      master, from_=0, to=300, orient=HORIZONTAL, sliderlength=50,  length=200, label="Hip Amplitude", command=self.set_amp)
    self.amp.set(150)
    self.amp.pack()

    self.knee_amp = Scale(
      master, from_=0, to=4, orient=HORIZONTAL, sliderlength=50, length=200, resolution=0.01, label= "Knee Amplitude", command=self.set_knee_amp)
    self.knee_amp.set(1)
    self.knee_amp.pack()

    self.afreq = Scale(
      master, from_=0, to=20, orient=HORIZONTAL, sliderlength=50, length=200, label="Angular Frequency", command=self.set_afreq)
    self.afreq.set(1)
    self.afreq.pack()

    self.fkoffset = Scale(
      master, from_=-400, to=400, orient=HORIZONTAL, sliderlength=50, length=200, label="Front Knee Offset", command=self.set_fkoffset)
    self.fkoffset.set(0)
    self.fkoffset.pack()

    self.bkoffset = Scale(
      master, from_=-400, to=400, orient=HORIZONTAL, sliderlength=50, length=200, label="Back Knee Offset", command=self.set_bkoffset)
    self.bkoffset.set(0)
    self.bkoffset.pack()

    self.foffset = Scale(
      master, from_=-400, to=400, orient=HORIZONTAL, sliderlength=50, length=200, label="Front Offset", command=self.set_foffset)
    self.foffset.set(232)
    self.foffset.pack()

    self.boffset = Scale(
      master, from_=-400, to=400, orient=HORIZONTAL, sliderlength=50, length=200, label="Rear Offset", command=self.set_boffset)
    self.boffset.set(108)
    self.boffset.pack()
    
  #change "gait" variable based on button selected from the gui
  def walk_button(self, event):
    global gait
    gait = 1

  def trot_button(self, event):
    global gait
    gait = 2

  def pace_button(self, event):
    global gait
    gait = 3

  #functions to obtain values returned from gui sliders
  def set_phase(self, event):
    global phase
    phase = event

  def set_amp(self, event):
    global amp
    amp = event

  def set_afreq(self, event):
    global afreq
    afreq = event

  def set_fkoffset(self, event):
    global fk_offset
    fk_offset = event

  def set_bkoffset(self, event):
    global bk_offset
    bk_offset = event

  def set_foffset(self, event):
    global f_offset
    f_offset = event

  def set_boffset(self, event):
    global b_offset
    b_offset = val

  def set_knee_amp(self, event):
    global knee_amp
    knee_amp = val

    

#########################################################################################################################
#######################################               MAIN PROGRAM             ##########################################
#########################################################################################################################
   
root = Tk()

app = App(root)

root.after(0,loop)
root.mainloop()
