#include <Servo.h>

//Servo SB, SF, HB, HF, EB, EF, KB, KF; 
Servo myservo1, myservo2, myservo3, myservo4, myservo5, myservo6, myservo7, myservo8;

String readString, servo1, servo2, servo3, servo4, servo5, servo6, servo7, servo8;

void setup() {
  Serial.begin(115200);
  
  myservo1.attach(2);
  myservo2.attach(3);
  myservo3.attach(4);
  myservo4.attach(5);
  myservo5.attach(6);
  myservo6.attach(7);
  myservo7.attach(8);
  myservo8.attach(9);
  
  delay(3000);
}

void loop() {
  int i = 1;
  char c;
    
  while (Serial.available() && readString.length() < 33) {
    delayMicroseconds(150);  //delay to allow buffer to fill
    //delay(1);
    if (Serial.available() > 0) {
      char c = Serial.read();  //gets one byte from serial buffer
      readString += c; //makes the string readString
    }
  }

  if (readString.length() > 0){
    Serial.println("The string is: " + readString); //see what was received
    Serial.println(readString.length()); 
    
    servo1 = readString.substring(0, 4); //get the first four characters
    servo2 = readString.substring(4, 8); 
    servo3 = readString.substring(8, 12); 
    servo4 = readString.substring(12, 16); 
    servo5 = readString.substring(16, 20); 
    servo6 = readString.substring(20, 24); 
    servo7 = readString.substring(24, 28); 
    servo8 = readString.substring(28, 32); 
    
    /* 
    Serial.print(servo1);  //print to serial monitor to see parsed results
    Serial.print(servo2);
    Serial.print(servo3);  
    Serial.print(servo4);
    Serial.print(servo5); 
    Serial.print(servo6);
    Serial.print(servo7);  
    Serial.println(servo8);
    */
    
    int n1 = servo1.toInt();
    int n2 = servo2.toInt();
    int n3 = servo3.toInt();
    int n4 = servo4.toInt();
    int n5 = servo5.toInt();
    int n6 = servo6.toInt();
    int n7 = servo7.toInt();
    int n8 = servo8.toInt();
           
    myservo1.writeMicroseconds(n3); //set servo positions
    myservo2.writeMicroseconds(n7);
    myservo3.writeMicroseconds(n1); 
    myservo4.writeMicroseconds(n5);
    myservo5.writeMicroseconds(n4); 
    myservo6.writeMicroseconds(n8);
    myservo7.writeMicroseconds(n2); 
    myservo8.writeMicroseconds(n6);
      
    readString=""; //clear strings
    servo1="";
    servo2="";
    servo3="";
    servo4="";
    servo5="";
    servo6="";
    servo7="";
    servo8="";
  }
}
