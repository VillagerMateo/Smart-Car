#include <AFMotor.h>

AF_DCMotor motor1(1);
AF_DCMotor motor2(2);

void setup() {
  // put your setup code here, to run once:
  motor1.setSpeed(200);
  motor1.run(RELEASE);

  // dodanie connection
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  uint8_t speed = 255;
  uint8_t turning_power = 255;

  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    if (data == "W") {
      motor2.run(RELEASE);
      motor1.run(BACKWARD);
      motor1.setSpeed(speed);
      delay(50);
    }

    if (data == "S") {
      motor2.run(RELEASE);
      motor1.run(FORWARD);
      motor1.setSpeed(speed);
      delay(100);
    }

    if (data == "A") {
      motor2.run(FORWARD);
      motor2.setSpeed(turning_power);
      delay(100);
    }

    if (data == "D") {
      motor2.run(BACKWARD);
      motor2.setSpeed(turning_power);
      delay(100);
    }

    if (data == "Q") {
      motor1.run(BACKWARD);
      motor1.setSpeed(speed);
      motor2.run(FORWARD);
      motor2.setSpeed(turning_power);
      delay(100);
    }

    if (data == "E") {
      motor1.run(BACKWARD);
      motor1.setSpeed(speed);
      motor2.run(BACKWARD);
      motor2.setSpeed(turning_power);
      delay(100);
    }

    if (data == "O") {
      motor1.run(RELEASE);
      motor2.run(RELEASE);
    }
      
    
  // Now turn off motor
  //motor1.run(RELEASE);
  //delay(1000);
  }}
