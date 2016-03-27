/* 
Program to control the AD5220 digipot via UART. The pot is initialized at max
resistance then controlled with the '+' and '-' characters.
*/

//control pins on AD5220
int CLK = 8, UD = 9, CS = 10;
//serial byte
char set_speed;
//parameter for counting time
unsigned long previousMillis = 0;
//to measure wiper voltage
float v_wiper;

void setup(){
  //pro mini bootloader communicates at 57600 baud
  Serial.begin(57600);
  
  pinMode(CS, OUTPUT);
  pinMode(UD, OUTPUT);
  pinMode(CLK, OUTPUT);
  
  //change pot wiper from middle to max resistance
  for (int i=0; i<20; i++){
    decrease_speed();
  }
  
  //hold current pot resistance
  digitalWrite(CS, HIGH);
  digitalWrite(CLK, HIGH);
}

void loop(){
  //get current time
  unsigned long currentMillis = millis();
  
  int wiper = analogRead(A0);
  v_wiper = wiper * (3.3 / 1023);
  
  //if 2000 msecs have passed
  if (currentMillis - previousMillis >= 2000){
    previousMillis = currentMillis;
    
    Serial.println(v_wiper);
  }
  
  //read serial data when it arrives
  if (Serial.available() > 0){
    set_speed = Serial.read();
  }
  
  //decrease speed
  if (set_speed == '-'){
    decrease_speed();
  }
  
  //increase speed
  else if (set_speed == '+'){
    increase_speed();
  }
  
  //get belt moving
  else if (set_speed == 's'){
    start();
  }
  
  //stop the belt
  else if (set_speed == 'e'){
    stop();
  }
  
  //hold pot resistance  
  else {
    digitalWrite(CS, HIGH);
  }
}

void decrease_speed(){
  digitalWrite(CS, LOW);
  digitalWrite(UD, LOW);
  digitalWrite(CLK, LOW);
  digitalWrite(CLK, HIGH);
    
  set_speed = '\0';
}

void increase_speed(){
  digitalWrite(CS, LOW);
  digitalWrite(UD, HIGH);
  digitalWrite(CLK, LOW);
  digitalWrite(CLK, HIGH);
    
  set_speed = '\0';
}

//increase wiper voltage to ~0.75V, when belt starts moving
void start(){
  for (int i = 0; i < 30; i++){
    digitalWrite(CS, LOW);
    digitalWrite(UD, HIGH);
    digitalWrite(CLK, LOW);
    digitalWrite(CLK, HIGH);
  }
  set_speed = '\0';
}

void stop(){
  while (v_wiper > 0.5){
    decrease_speed();
  }
}
