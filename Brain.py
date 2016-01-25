#!/usr/bin/env python

#This is a program which allows the user to modify the parameters of 8 sine waves with a graphical interface. The outputs
#of these sine waves are then formatted and written to the specified serial port.

from Tkinter import *
import serial
import time
import math

PI = 3.14159265359

#serial port for botboard communication
bb = serial.Serial('/dev/rfcomm0', 115200)	
print(bb.name)

########################################################################################################################
###########################################           MR RUNNER CLASS            #######################################
########################################################################################################################

class Mr_Runner:
  def __init__(self, master):
    #oscillator control variables
    self.phase = 0					
    self.afreq = 0					  
    self.amp = 0					
    self.gait = 0  
    self.knee_amp = 0

    #front and back joint offsets
    self.fk_offset = 0
    self.bk_offset = 0
    self.f_offset = 0					
    self.b_offset = 0
    
    #timer controls
    self.start_time = time.time() 
    self.elapsed_time = 0
    self.sine_time = 0.05 
    self.t = 0

    #create GUI
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
    self.s_phase = Scale(master, from_=0, to=3.14, orient=HORIZONTAL, resolution=0.01, sliderlength=50,  length=200, label="Phase", command=self.set_phase)
    self.s_phase.set(3.14)
    self.s_phase.pack()

    self.s_amp = Scale(master, from_=0, to=300, orient=HORIZONTAL, sliderlength=50,  length=200, label="Hip Amplitude", command=self.set_amp)
    self.s_amp.set(150)
    self.s_amp.pack()

    self.s_knee_amp = Scale(master, from_=0, to=4, orient=HORIZONTAL, sliderlength=50, length=200, resolution=0.01, label= "Knee Amplitude", command=self.set_knee_amp)
    self.s_knee_amp.set(1)
    self.s_knee_amp.pack()

    self.s_afreq = Scale(master, from_=0, to=2, orient=HORIZONTAL, sliderlength=50, length=200, resolution=0.01, label="Angular Frequency", command=self.set_afreq)
    self.s_afreq.set(0)
    self.s_afreq.pack()

    self.s_fkoffset = Scale(master, from_=-400, to=400, orient=HORIZONTAL, sliderlength=50, length=200, label="Front Knee Offset", command=self.set_fkoffset)
    self.s_fkoffset.set(0)
    self.s_fkoffset.pack()

    self.s_bkoffset = Scale(master, from_=-400, to=400, orient=HORIZONTAL, sliderlength=50, length=200, label="Back Knee Offset", command=self.set_bkoffset)
    self.s_bkoffset.set(0)
    self.s_bkoffset.pack()

    self.s_foffset = Scale(master, from_=-400, to=400, orient=HORIZONTAL, sliderlength=50, length=200, label="Front Hip Offset", command=self.set_foffset)
    self.s_foffset.set(232)
    self.s_foffset.pack()

    self.s_boffset = Scale(master, from_=-400, to=400, orient=HORIZONTAL, sliderlength=50, length=200, label="Rear Hip Offset", command=self.set_boffset)
    self.s_boffset.set(108)
    self.s_boffset.pack()
    
  #change "gait" variable based on button selected from the gui
  def walk_button(self, event):
    self.gait = '1.5708'

  def trot_button(self, event):
    self.gait = '-3.142'

  def pace_button(self, event):
    self.gait = '000000'

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
    
  #function to obtain current time
  def get_time(self):					      
    return time.time()

  def oscillate(self):
    #array to hold the servo positions
    #positions = [SB,SF,HB,HF,EB,EF,KB,KF]
    pos = [0,1,2,3,4,5,6,7,8]

    #sine wave parameters to determine shape
    pos[0] = self.amp
    pos[1] = self.knee_amp
    pos[2] = self.afreq
    pos[3] = self.gait
    pos[4] = self.phase
    pos[5] = self.f_offset
    pos[6] = self.b_offset
    pos[7] = self.fk_offset
    pos[8] = self.bk_offset
  
    if (pos[0] < 100):
      pos[0] = '0' + str(int(pos[0])) 
        if (pos[0] < 10):
	        pos[0] = '0' + str(int(pos[0]))
    
    else:
      pos[0] = str(int(pos[0]))
      
    for i in range (5, 9)  
      if (pos[i] < 100 and pos[i] > 0):
        pos[i] = '0' + str(int(pos[i]))
          if (pos[i] < 10):
            pos[i] = '0' + str(int(pos[i]))
    
      elif (pos[i] < 0 and pos[i] > -10):
        pos[i] = '-00' + str(abs(int(pos[i])))
       
      elif (pos[i] < -10):
    	  pos[i] = '-0' + str(abs(int(pos[i])))
    	  
    	else:
    	  pos[i] = str(int(pos[i]))
      
     
    #transmit servo positions over serial connection
    #bb.write('%d%d%d%d%d%d%d%d\n' % (SB,SF,HB,HF,EB,EF,KB,KF))
    print('%s%s%s%s%s%s%s%s%s\n' % (pos[0],pos[1],pos[2],pos[3],pos[4],pos[5],pos[6],pos[7],pos[8]))
    bb.write('%s%s%s%s%s%s%s%s%s\n' % (pos[0],pos[1],pos[2],pos[3],pos[4],pos[5],pos[6],pos[7],pos[8]))
       
    root.after(int(self.sine_time*1000),self.oscillate)
    

#########################################################################################################################
#######################################               MAIN PROGRAM             ##########################################
#########################################################################################################################
   
root = Tk()
root.wm_title("Gait Generator")

version1 = Mr_Runner(root)

root.after(0,version1.oscillate)
root.mainloop()
