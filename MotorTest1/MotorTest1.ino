//String InBytes;
#include <AFMotor.h>

AF_DCMotor motor1(1);
AF_DCMotor motor2(2);


void setup() {
  Serial.begin(9600);           // set up Serial library at 9600 bps
  //Serial.println("Motor test!");

  // turn on motor
  motor1.setSpeed(255);
//  motor1.run(RELEASE);

  motor2.setSpeed(255);
//  motor2.run(RELEASE);
}


void loop() {
  
  //Serial.print("tick");

  if (Serial.available() > 0) {
    String msg = Serial.readString();

    
    if (msg == "s") {
      motor1.setSpeed(speed(40));
      motor1.run(FORWARD);
      delay(3000);
      motor1.run(RELEASE);
      Serial.print("Go forward");
    }
    
    else if (msg == "w") {
      motor1.setSpeed(speed(45));
      motor1.run(BACKWARD);
      delay(3000);
      motor1.run(RELEASE);
      Serial.print("Go backward");
    }
    
    else if (msg == "d") {
      motor1.setSpeed(speed(50));
      motor1.run(BACKWARD);
      motor2.run(FORWARD);
      delay(3000);
      motor2.run(RELEASE);
      motor1.run(RELEASE);
      Serial.print("Go right");
    }
    
    else if (msg == "a") {
      motor1.setSpeed(speed(50));
      motor1.run(BACKWARD);
      motor2.run(BACKWARD);
      delay(3000);
      motor2.run(RELEASE);
      motor1.run(RELEASE);
      Serial.print("Go left");
    }
    
  }
  
  //motor1.run(FORWARD);
  //motor2.run(FORWARD);
  //delay(3000);

  // motor1.run(RELEASE);
  // motor2.run(RELEASE);
  // delay(3000);

  //motor1.run(BACKWARD);
  //motor2.run(BACKWARD);
  //delay(3000); 
}

int speed(int percent) {
  return map(percent, 0, 100, 0, 255);
}
