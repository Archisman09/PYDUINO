#include <SoftwareSerial.h>
#include <Servo.h>
SoftwareSerial Blutooth(10,11);  // TX RX

int led1 = 2;
int led2 = 3;
int led3 = 4;
int led4 = 5; 
int led5 = 6;
int servo_pin = 7;
Servo servo1;

void setup() {
  Blutooth.begin(9600);
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);
  pinMode(led3, OUTPUT);
  pinMode(led4, OUTPUT);
  pinMode(led5, OUTPUT);
  servo1.attach(servo_pin);
}

void loop() {
  if (Blutooth.available()) {
    char receive = Blutooth.read(); // receive deta from python terminal
    if (receive == 'a') {
      digitalWrite(led1, HIGH);
      // Blutooth.println("hello");  // send deta in python terminal
    }
    if (receive == 'f') {
      digitalWrite(led1 ,LOW);
    }
    if (receive == 'b') {
      digitalWrite(led2, HIGH);
    }
    if (receive == 'g') {
      digitalWrite(led2 ,LOW);
    }
    if (receive == 'c') {
      digitalWrite(led3, HIGH);
    }
    if (receive == 'h') {
      digitalWrite(led3 ,LOW);
    }
    if (receive == 'd') {
      digitalWrite(led4, HIGH);
    }
    if (receive == 'i') {
      digitalWrite(led4 ,LOW);
    }
    if (receive == 'e') {
      digitalWrite(led5, HIGH);
    }
    if (receive == 'j') {
      digitalWrite(led5 ,LOW);
    }
    if (receive == '0') {
      servo1.write(2);
    }
    if (receive == '1') {
      servo1.write(24);
    }
    if (receive == '2') {
      servo1.write(46);
    }
    if (receive == '3') {
      servo1.write(68);
    }
    if (receive == '4') {
      servo1.write(90);
    }
    if (receive == '5') {
      servo1.write(112);
    }
    if (receive == '6') {
      servo1.write(134);
    }
    if (receive == '7') {
      servo1.write(156);
    }
    if (receive == '8') {
      servo1.write(178);
    }
    if (receive == '9') {
      servo1.write(200);
    }
  }
}
