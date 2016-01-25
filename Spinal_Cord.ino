#include <Servo.h>

Servo SB, SF, HB, HF, EB, EF, KB, KF;
String readString, amp, knee_amp, afreq, gait, phase, f_offset, b_offset, fk_offset, bf_offset;

unsigned long previousMillis = 0;
unsigned int sine_time = 0.05;
unsigned int t = 0;

void setup(){
  //Start serial stream at 115200 baud
  Serial.begin(115200);
  
  //Connect servos to Arduino
  HB.attach(2);
  KF.attach(3);
  SB.attach(4); 
  EB.attach(5);
  HF.attach(6); 
  KB.attach(7);
  SF.attach(8); 
  EF.attach(9);
  
  delay(3000);
}

void loop(){
  char c;
    
  while (Serial.available() && readString.length() < 33){
    //delay to allow buffer to fill
    delayMicroseconds(150);
    if (Serial.available() > 0){
      //get one byte from serial buffer
      char c = Serial.read();
      //creates the string "readString"
      readString += c;
    }
  }

  if (readString.length() > 0){
    //See what was received
    Serial.println("The string is: " + readString);
    Serial.println(readString.length()); 
    
    //Parse serial string into separate parameters
    amp = readString.substring(0, 4);
    knee_amp = readString.substring(4, 8); 
    afreq = readString.substring(8, 12); 
    gait = readString.substring(12, 16); 
    phase = readString.substring(16, 20); 
    f_offset = readString.substring(20, 24); 
    b_offset = readString.substring(24, 28); 
    fk_offset = readString.substring(28, 32); 
    bk_offset = readString.substring(32, 36);
    
    /*
    //Print to serial monitor to see parsed results
    Serial.print(amp); 
    Serial.print(knee_amp); 
    Serial.print(afreq); 
    Serial.print(gait);
    Serial.print(phase);
    Serial.print(f_offset);
    Serial.print(b_offset);  
    Serial.print(fk_offset);
    Serial.println(bk_offset);
  
    //clear strings
    readString="";
    amp="";
    knee_amp="";
    afreq="";
    gait="";
    phase="";
    f_offset="";
    b_offset="";
    fk_offset="";
    bk_offset="";
    */
  }
  //determine joint positions
  pos[0] = int(amp) * sin(float(afreq)*t) + 1500 + int(f_offset)
  pos[1] = int(amp) * sin(float(afreq)*t) + 1522 - int(f_offset)
  pos[2] = int(amp) * sin(float(afreq)*t + float(gait)) + 1500 + int(b_offset)
  pos[3] = int(amp) * sin(float(afreq)*t + float(gait)) + 1446 - int(b_offset)
 
  pos[4] = int(amp)*float(knee_amp) * sin(float(afreq)*t + float(phase)) + 1500 + int(fk_offset)
  pos[5] = int(amp)*float(knee_amp) * sin(float(afreq)*t + float(phase)) + 1581 - int(fk_offset)
  pos[6] = int(amp)*float(knee_amp) * sin(float(afreq)*t + float(gait) + float(phase)) + 1500 + int(bk_offset)
  pos[7] = int(amp)*float(knee_amp) * sin(float(afreq)*t + float(gait) + float(phase)) + 1538 - int(bk_offset)
  
  //get time in milliseconds
  unsigned long currentMillis = millis();
  
  //if the time threshold has been passed...
  if(currentMillis - previousMillis >= sine_time){
    previousMillis = currentMillis;
    
    //write servo positions
    HB.writeMicroseconds(pos[2]);
    KF.writeMicroseconds(pos[6]);
    SB.writeMicroseconds(pos[0]); 
    EB.writeMicroseconds(pos[4]);
    HF.writeMicroseconds(pos[3]); 
    KB.writeMicroseconds(pos[7]);
    SF.writeMicroseconds(pos[1]); 
    EF.writeMicroseconds(pos[5]);
    
    //increment time parameter
    t+=1;
  }
}
