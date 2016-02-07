#!/usr/bin/env python

#This is a program which allows the user to modify the parameters of 8 sine waves with a graphical interface. These
#parameters are then formatted and written to the specified serial port.

from Tkinter import *
import serial
import time
import math

###############################################################################################################################
###########################################           MR RUNNER CLASS            ##############################################
###############################################################################################################################

class Mr_Runner:
  def __init__(self, master):
    #serial port for botboard communication
    self.bb = serial.Serial('/dev/rfcomm0', 115200)	
    print(self.bb.name)

    #serial port for treadmill communication
    self.tm = serial.Serial('/dev/rfcomm1', 115200)
    print(self.tm.name)

    #serial string
    self.pos = [0,1,2,3,4,5,6,7,8]
    self.pos_old = [0,1,2,3,4,5,6,7,8]

    #set initial gait to "walk"
    self.pos[4] = '1.571'
    
    #timer control
    self.t_time = 0.05 

    #for treadmill control
    self.set_speed = 0
    self.set_speed_old = 0
 
    #create parameter change flags
    self.bb_flag = 0

    #create GUI
    self.frame = Frame(master)
    self.frame.pack()

    #walk button
    self.walk = Button(self.frame, text="Walk")
    self.walk.pack(side=LEFT)
    self.walk.bind("1", self.walk_button)
    self.walk.invoke()

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

    self.s_afreq = Scale(master, from_=0, to=3, orient=HORIZONTAL, sliderlength=50, length=200, resolution=0.01, label="Angular Frequency", command=self.set_afreq)
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
    
    #treadmill buttons
    self.increase = Button(master, text="Faster", command=self.increase_speed)
    self.increase.pack()
    
    self.decrease = Button(master, text="Slower", command=self.decrease_speed)
    self.decrease.pack()
    
  #change "gait" variable based on button selected from the gui
  def walk_button(self, event):
    self.pos[4] = '1.571'

  def trot_button(self, event):
    self.pos[4] = '-3.14'

  def pace_button(self, event):
    self.pos[4] = '00000'

  #functions to obtain values returned from gui sliders
  def set_phase(self, event):
    self.pos[3] = event

  def set_amp(self, event):
    self.pos[0] = event

  def set_afreq(self, event):
    self.pos[2] = event

  def set_fkoffset(self, event):
    self.pos[7] = event

  def set_bkoffset(self, event):
    self.pos[8] = event

  def set_foffset(self, event):
    self.pos[5] = event

  def set_boffset(self, event):
    self.pos[6] = event

  def set_knee_amp(self, event):
    self.pos[1] = event
    
  def increase_speed(self, event):
    self.set_speed += 1
    
  def decrease_speed(self, event):
    self.set_speed -= 1

  #format and transmit serial data
  def transmit(self):
    for i in range(0, 9):
      if (self.pos[i] != self.pos_old[i]):
        self.bb_flag = 1

    if (self.bb_flag == 1):
      self.pos[0] = int(self.pos[0])
      self.pos[5] = int(self.pos[5]) 
      self.pos[6] = int(self.pos[6])
      self.pos[7] = int(self.pos[7])
      self.pos[8] = int(self.pos[8])

      #amplitude
      if (self.pos[0] < 100 and self.pos[0] >= 10):
        self.pos[0] = '0' + str(int(self.pos[0])) 
       
      elif (self.pos[0] < 10):
        self.pos[0] = '00' + str(int(self.pos[0]))
    
      else:
        self.pos[0] = str(int(self.pos[0]))
   
      #floating point numbers
      for i in range (1, 4):
        if (len(str(self.pos[i])) == 3):
          self.pos[i] = str(self.pos[i]) + '0' 

      #joint offsets  
      for i in range (5, 9):
        if (self.pos[i] >= 100):
          self.pos[i] = '0' + str(int(self.pos[i])) 
      
        elif (self.pos[i] < 100 and self.pos[i] > 10):
          self.pos[i] = '00' + str(int(self.pos[i]))
      
        elif (self.pos[i] < 10 and self.pos[i] >= 0):
          self.pos[i] = '000' + str(int(self.pos[i]))
    
        elif (self.pos[i] < 0 and self.pos[i] > -10):
          self.pos[i] = '-00' + str(abs(int(self.pos[i])))
       
        elif (self.pos[i] <= -10 and self.pos[i] > -100):
          self.pos[i] = '-0' + str(abs(int(self.pos[i])))
    	  
        else:
          self.pos[i] = str(int(self.pos[i]))

        #store old sine parameters for comparison next loop
        for i in range(0, 9):
          self.pos_old[i] = self.pos[i]

        #reset flag
        self.bb_flag = 0      
     
      #print sine parameters to console
      #transmit sine parameters over serial connection
      #bb.write('%s%s%s%s%s%s%s%s%s\n' % (hip_amp, knee_amp, afreq, phase, gait, f_offset, b_offset, fk_offset, bk_offset))
      print('%s %s %s %s %s %s %s %s %s\n' % (self.pos[0],self.pos[1],self.pos[2],self.pos[3],self.pos[4],self.pos[5],self.pos[6],self.pos[7],self.pos[8]))
      self.bb.write('%s%s%s%s%s%s%s%s%s\n' % (self.pos[0],self.pos[1],self.pos[2],self.pos[3],self.pos[4],self.pos[5],self.pos[6],self.pos[7],self.pos[8]))
      
    if (self.set_speed != self.set_speed_old):
      self.tm.write('%s' % self.set_speed)
      self.set_speed_old = self.set_speed
       
    root.after(int(self.t_time*1000),self.transmit)
    
##############################################################################################################################
########################################                MAIN PROGRAM             #############################################
##############################################################################################################################
   
root = Tk()
root.wm_title("Gait Generator")

version1 = Mr_Runner(root)

root.after(0,version1.transmit)
root.mainloop()
