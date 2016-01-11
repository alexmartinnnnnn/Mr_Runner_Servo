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

#serial port for botboard communication
bb = serial.Serial('/dev/rfcomm0', 115200)	
print(bb.name)

#start the oscillator timer
start_time = time.time() 			

#function to obtain current time
def get_time():					      
  return time.time()


########################################################################################################################
###########################################             GUI            #################################################
########################################################################################################################

class App:
  def __init__(self, master):
    #oscillator control variables
    self.phase = 0					
    self.afreq = 0					  
    self.amp = 0					
    self.gait = 0  
    self.knee_amp = 0
    self.gselector = 0

    #front and back joint offsets
    self.fk_offset = 0
    self.bk_offset = 0
    self.f_offset = 0					
    self.b_offset = 0

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
    self.s_phase = Scale(
      master, from_=0, to=3.14, orient=HORIZONTAL, resolution=0.01, sliderlength=50,  length=200, label="Phase", command=self.set_phase)
    self.s_phase.set(3.14)
    self.s_phase.pack()

    self.s_amp = Scale(
      master, from_=0, to=300, orient=HORIZONTAL, sliderlength=50,  length=200, label="Hip Amplitude", command=self.set_amp)
    self.s_amp.set(150)
    self.s_amp.pack()

    self.s_knee_amp = Scale(
      master, from_=0, to=4, orient=HORIZONTAL, sliderlength=50, length=200, resolution=0.01, label= "Knee Amplitude", command=self.set_knee_amp)
    self.s_knee_amp.set(1)
    self.s_knee_amp.pack()

    self.s_afreq = Scale(
      master, from_=0, to=20, orient=HORIZONTAL, sliderlength=50, length=200, label="Angular Frequency", command=self.set_afreq)
    self.s_afreq.set(1)
    self.s_afreq.pack()

    self.s_fkoffset = Scale(
      master, from_=-400, to=400, orient=HORIZONTAL, sliderlength=50, length=200, label="Front Knee Offset", command=self.set_fkoffset)
    self.s_fkoffset.set(0)
    self.s_fkoffset.pack()

    self.s_bkoffset = Scale(
      master, from_=-400, to=400, orient=HORIZONTAL, sliderlength=50, length=200, label="Back Knee Offset", command=self.set_bkoffset)
    self.s_bkoffset.set(0)
    self.s_bkoffset.pack()

    self.s_foffset = Scale(
      master, from_=-400, to=400, orient=HORIZONTAL, sliderlength=50, length=200, label="Front Offset", command=self.set_foffset)
    self.s_foffset.set(232)
    self.s_foffset.pack()

    self.s_boffset = Scale(
      master, from_=-400, to=400, orient=HORIZONTAL, sliderlength=50, length=200, label="Rear Offset", command=self.set_boffset)
    self.s_boffset.set(108)
    self.s_boffset.pack()
    
  #change "gait" variable based on button selected from the gui
  def walk_button(self, event):
    self.gait = PI/2

  def trot_button(self, event):
    self.gait = -PI

  def pace_button(self, event):
    self.gait = 0

  #functions to obtain values returned from gui sliders
  def set_phase(self, event):
    self.phase = event

  def set_amp(self, event):
    self.amp = event

  def set_afreq(self, event):
    self.afreq = event

  def set_fkoffset(self, event):
    self.fk_offset = event

  def set_bkoffset(self, event):
    self.bk_offset = event

  def set_foffset(self, event):
    self.f_offset = event

  def set_boffset(self, event):
    self.b_offset = event

  def set_knee_amp(self, event):
    self.knee_amp = event

  def oscillate(self):
    #variables for timer, will be added to the class soon
    global t, start_time, elapsed_time

    #array to hold the servo positions
    #positions = [SB,SF,HB,HF,EB,EF,KB,KF]
    pos = [0,1,2,3,4,5,6,7]

    #sine waves generate servo positions for each joint of the robot
    pos[0] = (int(self.amp) * math.sin(int(self.afreq)*t)) + 1500 + int(self.f_offset)
    pos[1] = (int(self.amp) * math.sin(int(self.afreq)*t)) + 1522 - int(self.f_offset)
    pos[2] = (int(self.amp) * math.sin(int(self.afreq)*t + gait)) + 1500 + int(self.b_offset)
    pos[3] = (int(self.amp) * math.sin(int(self.afreq)*t + gait)) + 1446 - int(self.b_offset)
 
    pos[4] = (int(self.amp)*float(self.knee_amp) * math.sin(int(self.afreq)*t + float(self.phase))) + 1500 + int(self.fk_offset)
    pos[5] = (int(self.amp)*float(self.knee_amp) * math.sin(int(self.afreq)*t + float(self.phase))) + 1581 - int(self.fk_offset)
    pos[6] = (int(self.amp)*float(self.knee_amp) * math.sin(int(self.afreq)*t + gait + float(self.phase))) + 1500 + int(self.bk_offset)
    pos[7] = (int(self.amp)*float(self.knee_amp) * math.sin(int(self.afreq)*t + gait + float(self.phase))) + 1538 - int(self.bk_offset)
  
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
       
    root.after(int(sine_time*1000),self.oscillate)
    

#########################################################################################################################
#######################################               MAIN PROGRAM             ##########################################
#########################################################################################################################
   
root = Tk()

app = App(root)

root.after(0,app.oscillate)
root.mainloop()
