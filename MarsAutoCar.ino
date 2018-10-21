#include <Wire.h>
#include <Adafruit_MotorShield.h>

//#define DEBUG

Adafruit_MotorShield AFMS = Adafruit_MotorShield();

Adafruit_DCMotor *motorRF = AFMS.getMotor(1);
Adafruit_DCMotor *motorRB = AFMS.getMotor(2);
Adafruit_DCMotor *motorLF = AFMS.getMotor(3);
Adafruit_DCMotor *motorLB = AFMS.getMotor(4);

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(10);
  AFMS.begin();

  setLeft(40);
  setRight(40);
}

void loop() {
  static float X, Z;

  static unsigned long lastSensedTime = millis();

  unsigned long currentTime = millis();

  if(currentTime - lastSensedTime > 500){
    setLeft(40);
    setRight(40);
    lastSensedTime = currentTime;
    return;
  }
  
  if(!getCoords(X,Z)) return;

  

  lastSensedTime = currentTime;

  #define RANGE 38

  if(X < RANGE && X >= 0){
    int turningSpeed = map(Z, 1, 1500, 100, 80);
    setLeft(map(Z, 1, 1500, -100, -80));
    setRight(turningSpeed);
  }
  else if(X > -RANGE && X <= 0){
    int turningSpeed = map(Z, 1, 1500, 100, 80);
    setLeft(turningSpeed);
    setRight(map(Z, 1, 1500, -100, -80));
  }
  else{
    setLeft(40);
    setRight(40);
  }
}

void setLeft(int spd){
  motorLF->setSpeed(abs(spd));
  motorLB->setSpeed(abs(spd));
  motorLF->run((spd >= 0 ? BACKWARD : FORWARD));
  motorLB->run((spd >= 0 ? BACKWARD : FORWARD));
}

void setRight(int spd){
  motorRF->setSpeed(abs(spd));
  motorRB->setSpeed(abs(spd));
  motorRF->run((spd >= 0 ? BACKWARD : FORWARD));
  motorRB->run((spd >= 0 ? BACKWARD : FORWARD));
}

bool getCoords(float& X, float& Z){

  if(!Serial.available()) return false;

  String data = Serial.readString();
  
  int commaIndex = data.indexOf(',');
  X = data.substring(0,commaIndex).toFloat();
  Z = data.substring(commaIndex + 1, data.length()).toFloat();

  #ifdef DEBUG
  Serial.println(data);
  Serial.println(X);
  Serial.println(Z);
  #endif
  
  return true;
}
