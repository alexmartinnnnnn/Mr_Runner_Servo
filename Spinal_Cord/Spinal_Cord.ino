/*
This is a program that recieves sine wave parameters from a serial connection in a single string.
The string is parsed and converted into numbers, which are plugged into 8 sine equations to generate
positions for each joint of the robot.
*/

#include <Servo.h>

Servo SB, SF, HB, HF, EB, EF, KB, KF;
int iAmp, iF_offset, iB_offset, iFk_offset, iBk_offset, pos[] = {0,1,2,3,4,5,6,7};
unsigned int t = 0;
unsigned long previousMillis = 0;
float fKnee_amp, fAfreq, fPhase, fGait;

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
  char c, buffer[10];
  String readString, amp, knee_amp, afreq, gait, phase, f_offset, b_offset, fk_offset, bk_offset;
  unsigned int sine_time = 0.05;
    
  while (Serial.available() && readString.length() < 37){
    //delay to allow buffer to fill
    delayMicroseconds(100);
    if (Serial.available() > 0){
      //get one byte from serial buffer
      char c = Serial.read();
      //creates the string "readString"
      readString += c;
    }
  }

  if (readString.length() > 36){
    //see what was received
    Serial.println("The string is: " + readString);
    Serial.println(readString.length()); 
    
    //parse serial string into separate parameters
    amp = readString.substring(0, 3);
    knee_amp = readString.substring(3, 7); 
    afreq = readString.substring(7, 11); 
    phase = readString.substring(11, 15); 
    gait = readString.substring(15, 20); 
    f_offset = readString.substring(20, 24); 
    b_offset = readString.substring(24, 28); 
    fk_offset = readString.substring(28, 32); 
    bk_offset = readString.substring(32, 36);
    /*
    //Print to serial monitor to see parsed results
    Serial.println("Hip Amp: " + amp); 
    Serial.println("Knee Amp: " + knee_amp); 
    Serial.println("Afreq: " + afreq); 
    Serial.println("Gait: " + gait);
    Serial.println("Phase: " + phase);
    Serial.println("F Offset: " + f_offset);
    Serial.println("B Offset: " + b_offset);  
    Serial.println("Fk Offset: " + fk_offset);
    Serial.println("Bk Offset: " + bk_offset + "\n");
    */
    //convert string values to numbers
    iAmp = amp.toInt();
  
    knee_amp.toCharArray(buffer, 10);
    fKnee_amp = atof(buffer);
    memset(buffer, 0, sizeof(buffer));
  
    afreq.toCharArray(buffer, 10);
    fAfreq = atof(buffer)/100;
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
  
  //if the joints should be oscillating
  if (fAfreq > 0){
    //determine joint positions
    pos[0] = iAmp * sin(fAfreq*t) + 1500 + iF_offset;
    pos[1] = iAmp * sin(fAfreq*t) + 1522 - iF_offset;
    pos[2] = iAmp * sin(fAfreq*t + fGait) + 1500 + iB_offset;
    pos[3] = iAmp * sin(fAfreq*t + fGait) + 1446 - iB_offset;
 
    pos[4] = iAmp*fKnee_amp * sin(fAfreq*t + fPhase) + 1500 + iFk_offset;
    pos[5] = iAmp*fKnee_amp * sin(fAfreq*t + fPhase) + 1581 - iFk_offset;
    pos[6] = iAmp*fKnee_amp * sin(fAfreq*t + fGait + fPhase) + 1500 + iBk_offset;
    pos[7] = iAmp*fKnee_amp * sin(fAfreq*t + fGait + fPhase) + 1538 - iBk_offset;
    /*
    //print parameter variables
    Serial.println(iAmp); 
    Serial.println(fKnee_amp); 
    Serial.println(fAfreq); 
    Serial.println(fGait);
    Serial.println(fPhase);
    Serial.println(iF_offset);
    Serial.println(iB_offset);  
    Serial.println(iFk_offset);
    Serial.println(iBk_offset);
    
    //print servo positions
    Serial.println(pos[0]);
    Serial.println(pos[1]);
    Serial.println(pos[2]);
    Serial.println(pos[3]);
    Serial.println(pos[4]);
    Serial.println(pos[5]);
    Serial.println(pos[6]);
    Serial.println(pos[7]);
    */
    //get time in milliseconds
    unsigned long currentMillis = millis();
  
    //if the time threshold has been passed
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
}
