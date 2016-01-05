#!/usr/bin/env python

from Tkinter import *
import serial
import time
import math

PI = 3.14159265359

phase = 1.6					#variables that define starting values
afreq = 7					  #for oscillators
amp = 50					
gait = 0   					

t = 0						    #oscillator independant variable
sine_time = 0.05 		#time in seconds for oscillators to wait before transmitting current positions
elapsed_time = 0

bfk_offset = 0
bbk_offset = 0

bf_offset = 0					#front and back hip offsets for each gait
bb_offset = 0
tf_offset = 0
tb_offset = 0
wf_offset = 0
wb_offset = 0

bb = serial.Serial('/dev/rfcomm0', 115200)	#serial port for botboard communication
print(bb.name)

start_time = time.time() 			#start the oscillator timer

def get_time():					      #function to obtain current time
  return time.time()

#####################################################################################################################
#############################                  OSCILLATORS                   ########################################
#####################################################################################################################

def trot():
  #variables which allow sine wave parameters to be changed via a gui interface
  global t, PI, start_time, elapsed_time, bf_offset, bb_offset, amp, afreq, phase, bbk_offset, bfk_offset

  #array to hold the servo positions
  #positions = [SB,SF,HB,HF,EB,EF,KB,KF]
  pos = [0,1,2,3,4,5,6,7]

  #sine waves generate servo positions for each joint of the robot
  pos[0] = (int(amp) * math.sin(int(afreq)*t)) + 1500 + int(bf_offset)
  pos[1] = (int(amp) * math.sin(int(afreq)*t)) + 1522 - int(bf_offset)
  pos[2] = (int(amp) * math.sin(int(afreq)*t - PI)) + 1500 + int(bb_offset)
  pos[3] = (int(amp) * math.sin(int(afreq)*t - PI)) + 1446 - int(bb_offset)
 
  pos[4] = (int(amp) * math.sin(int(afreq)*t + float(phase))) + 1500 + int(bfk_offset)
  pos[5] = (int(amp) * math.sin(int(afreq)*t + float(phase))) + 1581 - int(bfk_offset)
  pos[6] = (int(amp) * math.sin(int(afreq)*t - PI + float(phase))) + 1500 + int(bbk_offset)
  pos[7] = (int(amp) * math.sin(int(afreq)*t - PI + float(phase))) + 1538 - int(bbk_offset)
  
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


def walk():
  global t, PI, afreq, start_time, elapsed_time, bf_offset, bb_offset, amp, phase, bfk_offset, bbk_offset

  #positions = [SB,SF,HB,HF,EB,EF,KB,KF]
  pos = [0,1,2,3,4,5,6,7]

  pos[0] = (int(amp) * math.sin(int(afreq)*t + PI)) + 1500 + int(bf_offset)
  pos[1] = (int(amp) * math.sin(int(afreq)*t + PI)) + 1522 - int(bf_offset)
  pos[2] = (int(amp) * math.sin(int(afreq)*t + PI/2)) + 1500 + int(bb_offset)
  pos[3] = (int(amp) * math.sin(int(afreq)*t + PI/2)) + 1446 - int(bb_offset)
  
  pos[4] = (int(amp) * math.sin(int(afreq)*t + PI - float(phase))) + 1500 + int(bfk_offset)
  pos[5] = (int(amp) * math.sin(int(afreq)*t + PI - float(phase))) + 1581 - int(bfk_offset)
  pos[6] = (int(amp) * math.sin(int(afreq)*t + PI/2 - float(phase))) + 1500 + int(bbk_offset)
  pos[7] = (int(amp) * math.sin(int(afreq)*t + PI/2 - float(phase))) + 1538 - int(bbk_offset)
  
  elapsed_time = get_time()
  
  if (elapsed_time - start_time >= sine_time):
     print ('time difference: %s' % (elapsed_time - start_time))
     start_time = elapsed_time
     t += 1

     for i in range(len(pos)):
       if (pos[i] < 1000):
	 pos[i] = '0' + str(int(pos[i]))

       else:
	 pos[i] = str(int(pos[i]))
     
     #bb.write('%d%d%d%d%d%d%d%d\n' % (SB,SF,HB,HF,EB,EF,KB,KF))
     print('%s%s%s%s%s%s%s%s\n' % (pos[0],pos[1],pos[2],pos[3],pos[4],pos[5],pos[6],pos[7]))
     bb.write('%s%s%s%s%s%s%s%s\n' % (pos[0],pos[1],pos[2],pos[3],pos[4],pos[5],pos[6],pos[7]))


def pace():
  global t, PI, afreq, start_time, elapsed_time, bf_offset, bb_offset, amp, phase, bfk_offset, bbk_offset

  #positions = [SB,SF,HB,HF,EB,EF,KB,KF]
  pos = [0,1,2,3,4,5,6,7]

  pos[0] = (int(amp) * math.sin(int(afreq)*t)) + 1500 + int(bf_offset)
  pos[1] = (int(amp) * math.sin(int(afreq)*t)) + 1522 - int(bf_offset)
  pos[2] = (int(amp) * math.sin(int(afreq)*t)) + 1500 + int(bb_offset)
  pos[3] = (int(amp) * math.sin(int(afreq)*t)) + 1446 - int(bb_offset)
  
  pos[4] = (int(amp) * math.sin(int(afreq)*t + float(phase))) + 1500 + int(bfk_offset)
  pos[5] = (int(amp) * math.sin(int(afreq)*t + float(phase))) + 1581 - int(bfk_offset)
  pos[6] = (int(amp) * math.sin(int(afreq)*t + float(phase))) + 1500 + int(bbk_offset)
  pos[7] = (int(amp) * math.sin(int(afreq)*t + float(phase))) + 1538 - int(bbk_offset)
  
  elapsed_time = get_time()
  
  if (elapsed_time - start_time >= sine_time):
     print ('time difference: %s' % (elapsed_time - start_time))
     start_time = elapsed_time
     t += 1

     for i in range(len(pos)):
       if (pos[i] < 1000):
	 pos[i] = '0' + str(int(pos[i]))

       else:
	 pos[i] = str(int(pos[i]))
     
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

def loop():				#main execution loop of the program, choose gait based on number
  global gait
  if (gait == 1):
    walk()

  elif (gait == 2):
    trot()

  elif (gait == 3):
    pace()
  
  root.after(int(sine_time*1000),loop) 


#functions to obtain values returned from gui sliders
def set_bound_phase(val):
  global phase
  phase = val

def set_bound_amp(val):
  global amp
  amp = val

def set_bound_afreq(val):
  global afreq
  afreq = val

def set_bound_fkoffset(val):
  global bfk_offset
  bfk_offset = val

def set_bound_bkoffset(val):
  global bbk_offset
  bbk_offset = val

def set_bound_foffset(val):
  global bf_offset
  bf_offset = val

def set_bound_boffset(val):
  global bb_offset
  bb_offset = val

def set_sine_time(val):
  global sine_time
  sine_time = val

########################################################################################################
#################################    	        GUI            ###########################################
########################################################################################################

class App:
  def __init__(self, master):
    frame = Frame(master)
    frame.pack()

    #############################               WALK           ##################################

    self.walk = Button(frame, text="Walk")
    self.walk.bind("1", walk_button)
    self.walk.pack(side=LEFT)

    ##############################              TROT           #################################

    self.trot = Button(frame, text="Trot")
    self.trot.bind("2", trot_button)
    self.trot.pack(side=LEFT)

    ###############################             BOUND           ################################
    global phase

    self.pace = Button(frame, text="Pace")
    self.pace.bind("3", pace_button)
    self.pace.pack(side=LEFT)

    bound_phase = Scale(
      master, from_=0, to=3.14, orient=HORIZONTAL, resolution=0.01, sliderlength=50,  length=200, label="Phase", command=set_bound_phase)
    bound_phase.set(3.14)
    bound_phase.pack()

    bound_amp = Scale(
      master, from_=0, to=300, orient=HORIZONTAL, sliderlength=50,  length=200, label="Amplitude", command=set_bound_amp)
    bound_amp.set(150)
    bound_amp.pack()

    bound_afreq = Scale(
      master, from_=0, to=20, orient=HORIZONTAL, sliderlength=50, length=200, label="Angular Frequency", command=set_bound_afreq)
    bound_afreq.set(1)
    bound_afreq.pack()

    bound_fkoffset = Scale(
      master, from_=-400, to=400, orient=HORIZONTAL, sliderlength=50, length=200, label="Front Knee Offset", command=set_bound_fkoffset)
    bound_fkoffset.set(-350)
    bound_fkoffset.pack()

    bound_bkoffset = Scale(
      master, from_=-400, to=400, orient=HORIZONTAL, sliderlength=50, length=200, label="Back Knee Offset", command=set_bound_bkoffset)
    bound_bkoffset.set(-350)
    bound_bkoffset.pack()

    bound_foffset = Scale(
      master, from_=-400, to=400, orient=HORIZONTAL, sliderlength=50, length=200, label="Front Offset", command=set_bound_foffset)
    bound_foffset.set(232)
    bound_foffset.pack()

    bound_boffset = Scale(
      master, from_=-400, to=400, orient=HORIZONTAL, sliderlength=50, length=200, label="Rear Offset", command=set_bound_boffset)
    bound_boffset.set(108)
    bound_boffset.pack()

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
