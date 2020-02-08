#include <Servo.h>

#define INITIAL_STATE 10
#define PUSH_STATE -10

Servo myservo;
int incomingBytes;

void setup() {
  myservo.attach(9);
  Serial.begin(9600);

  myservo.write(INITIAL_STATE);
}

void loop() {
  if  (Serial.available() > 0) {
    incomingBytes = Serial.read();

    myservo.write(PUSH_STATE);
    delay(80);
    myservo.write(INITIAL_STATE);
  }
}
