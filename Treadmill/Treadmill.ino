int set_speed = 0, set_speed_old = 0;

void setup(){
  Serial.begin(115200);
  
  pinMode(CS, OUTPUT);
  pinMode(UD, OUTPUT);
  pinMode(CLK, OUTPUT);
  
  //hold current pot resistance
  digitalWrite(CS, HIGH);
  digitalWrite(CLK, HIGH);
}

void loop(){
  if (Serial.available() > 0){
    char c = Serial.read();
    //convert char to int
    set_speed = c - '0';
  }
  
  if (set_speed > set_speed_old){
    digitalWrite(CS, LOW);
    digitalWrite(UD, LOW);
    digitalWrite(CLK, LOW);
    digitalWrite(CLK, HIGH);
    
    set_speed_old = set_speed;
  }
  
  else if(set_speed < set_speed_old){
    digitalWrite(CS, LOW);
    digitalWrite(UD, HIGH);
    digitalWrite(CLK, LOW);
    digitalWrite(CLK, HIGH);
    
    set_speed_old = set_speed;
  }
    
  else {
    digitalWrite(CS, HIGH);
  }
}
