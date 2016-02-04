#include <Servo.h>

Servo SB, SF, HB, HF, EB, EF, KB, KF;

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
  char c, buffer[10], pos[] = {0,1,2,3,4,5,6,7,8};
  int iAmp, iF_offset, iB_offset, iFk_offset, iBk_offset;
  float fKnee_amp, fAfreq, fPhase, fGait;
  String readString, amp, knee_amp, afreq, gait, phase, f_offset, b_offset, fk_offset, bk_offset;
  unsigned long previousMillis = 0;
  unsigned int sine_time = 0.05, t = 0;
    
  while (Serial.available() && readString.length() < 38){
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
    amp = readString.substring(0, 3);
    knee_amp = readString.substring(3, 7); 
    afreq = readString.substring(7, 11); 
    phase = readString.substring(12, 16); 
    gait = readString.substring(16, 21); 
    f_offset = readString.substring(21, 25); 
    b_offset = readString.substring(25, 29); 
    fk_offset = readString.substring(29, 33); 
    bk_offset = readString.substring(33, 37);
    
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
    */
    
    iAmp = amp.toInt();
  
    knee_amp.toCharArray(buffer, 10);
    fKnee_amp = atof(buffer);
    memset(buffer, 0, sizeof(buffer));
  
    afreq.toCharArray(buffer, 10);
    fAfreq = atof(buffer);
    memset(buffer, 0, sizeof(buffer));
  
    phase.toCharArray(buffer, 10);
    fPhase = atof(buffer);
    memset(buffer, 0, sizeof(buffer));
  
    gait.toCharArray(buffer, 10);
    fGait = atof(buffer);
    memset(buffer, 0, sizeof(buffer));
  
    iF_offset = f_offset.toInt();
    iB_offset = b_offset.toInt();
    iFk_offset = fk_offset.toInt();
    iBk_offset = bk_offset.toInt();
    
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
  }
  
  //determine joint positions
  pos[0] = iAmp * sin(fAfreq*t) + 1500 + iF_offset;
  pos[1] = iAmp * sin(fAfreq*t) + 1522 - iF_offset;
  pos[2] = iAmp * sin(fAfreq*t + fGait) + 1500 + iB_offset;
  pos[3] = iAmp * sin(fAfreq*t + fGait) + 1446 - iB_offset;
 
  pos[4] = iAmp*fKnee_amp * sin(fAfreq*t + fPhase) + 1500 + iFk_offset;
  pos[5] = iAmp*fKnee_amp * sin(fAfreq*t + fPhase) + 1581 - iFk_offset;
  pos[6] = iAmp*fKnee_amp * sin(fAfreq*t + fGait + fPhase) + 1500 + iBk_offset;
  pos[7] = iAmp*fKnee_amp * sin(fAfreq*t + fGait + fPhase) + 1538 - iBk_offset;
  
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
