#include <SoftwareSerial.h>
#include <AFMotor.h>

SoftwareSerial mySerial(10, 11);
char receivedData;

AF_DCMotor motor1(1);
AF_DCMotor motor2(2);

void setup() {
  motor1.setSpeed(150);
  motor2.setSpeed(150);

  Serial.begin(9600);
  mySerial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    receivedData = Serial.read();

    if (receivedData == 'F') {
      forward();
      delay(2000);
    } else if (receivedData == 'B') {
      backward();
      delay(2000);
    } else if (receivedData == 'S') {
      stop();
    }
  }
}



void stop() {
  motor1.run(RELEASE);
  motor2.run(RELEASE);
}

void forward() {
  motor1.run(FORWARD);
  motor2.run(FORWARD);
}

void backward() {
  motor1.run(BACKWARD);
  motor2.run(BACKWARD);
}
