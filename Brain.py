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

#####################################################################################################################
#############################                  OSCILLATORS                   ########################################
#####################################################################################################################

def oscillate(gselector):
  #variables which allow sine wave parameters to be changed via a gui interface
  global t, start_time, elapsed_time, f_offset, b_offset, amp, afreq, phase, bk_offset, fk_offset

  #array to hold the servo positions
  #positions = [SB,SF,HB,HF,EB,EF,KB,KF]
  pos = [0,1,2,3,4,5,6,7]

  #sine waves generate servo positions for each joint of the robot
  pos[0] = (int(amp) * math.sin(int(afreq)*t)) + 1500 + int(f_offset)
  pos[1] = (int(amp) * math.sin(int(afreq)*t)) + 1522 - int(f_offset)
  pos[2] = (int(amp) * math.sin(int(afreq)*t + gselector)) + 1500 + int(b_offset)
  pos[3] = (int(amp) * math.sin(int(afreq)*t + gselector)) + 1446 - int(b_offset)
 
  pos[4] = (int(amp) * math.sin(int(afreq)*t + float(phase))) + 1500 + int(fk_offset)
  pos[5] = (int(amp) * math.sin(int(afreq)*t + float(phase))) + 1581 - int(fk_offset)
  pos[6] = (int(amp) * math.sin(int(afreq)*t + gselector + float(phase))) + 1500 + int(bk_offset)
  pos[7] = (int(amp) * math.sin(int(afreq)*t + gselector + float(phase))) + 1538 - int(bk_offset)
  
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
     

############################################################################################################
################################        INTERMEDIATES         ##############################################
############################################################################################################

#change "gait" variable based on button selected from the gui
def walk_button(event):
  global gait
  gait = 1
  return 1

def trot_button(event):
  global gait
  gait = 2
  return 2

def pace_button(event):
  global gait
  gait = 3
  return 3

#functions to obtain values returned from gui sliders
def set_phase(val):
  global phase
  phase = val

def set_amp(val):
  global amp
  amp = val

def set_afreq(val):
  global afreq
  afreq = val

def set_fkoffset(val):
  global fk_offset
  fk_offset = val

def set_bkoffset(val):
  global bk_offset
  bk_offset = val

def set_foffset(val):
  global f_offset
  f_offset = val

def set_boffset(val):
  global b_offset
  b_offset = val

#def set_sine_time(val):
#  global sine_time
#  sine_time = val
  
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

########################################################################################################
#################################    	        GUI            ###########################################
########################################################################################################

class App:
  def __init__(self, master):
    frame = Frame(master)
    frame.pack()

    #walk button
    self.walk = Button(frame, text="Walk")
    self.walk.bind("1", walk_button)
    self.walk.pack(side=LEFT)
    
    #trot button
    self.trot = Button(frame, text="Trot")
    self.trot.bind("2", trot_button)
    self.trot.pack(side=LEFT)

    #pace button
    self.pace = Button(frame, text="Pace")
    self.pace.bind("3", pace_button)
    self.pace.pack(side=LEFT)
    
    #various sliders to control sine waves
    self.phase = Scale(
      master, from_=0, to=3.14, orient=HORIZONTAL, resolution=0.01, sliderlength=50,  length=200, label="Phase", command=set_phase)
    self.phase.set(3.14)
    self.phase.pack()

    self.amp = Scale(
      master, from_=0, to=300, orient=HORIZONTAL, sliderlength=50,  length=200, label="Amplitude", command=set_amp)
    self.amp.set(150)
    self.amp.pack()

    self.afreq = Scale(
      master, from_=0, to=20, orient=HORIZONTAL, sliderlength=50, length=200, label="Angular Frequency", command=set_afreq)
    self.afreq.set(1)
    self.afreq.pack()

    self.fkoffset = Scale(
      master, from_=-400, to=400, orient=HORIZONTAL, sliderlength=50, length=200, label="Front Knee Offset", command=set_fkoffset)
    self.fkoffset.set(-350)
    self.fkoffset.pack()

    self.bkoffset = Scale(
      master, from_=-400, to=400, orient=HORIZONTAL, sliderlength=50, length=200, label="Back Knee Offset", command=set_bkoffset)
    self.bkoffset.set(-350)
    selfbkoffset.pack()

    self.foffset = Scale(
      master, from_=-400, to=400, orient=HORIZONTAL, sliderlength=50, length=200, label="Front Offset", command=set_foffset)
    self.foffset.set(232)
    self.foffset.pack()

    self.boffset = Scale(
      master, from_=-400, to=400, orient=HORIZONTAL, sliderlength=50, length=200, label="Rear Offset", command=set_boffset)
    self.boffset.set(108)
    self.boffset.pack()

#    sine_btime = Scale(
#      master, from_=0, to=0.1, orient=HORIZONTAL, sliderlength=50, length=200, resolution=0.01, label= "Sine Time", command=set_sine_time)
#    sine_btime.set(0.08)
#    sine_btime.pack()

#########################################################################################################################
#######################################               MAIN PROGRAM             ##########################################
#########################################################################################################################
   
root = Tk()

app = App(root)

root.after(0,loop)
root.mainloop()
