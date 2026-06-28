// Scout motor controller firmware — Arduino/ESP32
// Serial protocol: STOP | GOTO <name> | COME | PING
// Wire L298N: IN1-4, ENA, ENB per robot/docs/hardware.md

#define IN1 5
#define IN2 6
#define IN3 9
#define IN4 10
#define ENA 3
#define ENB 11

const int SPEED = 180;  // PWM 0-255 — tune down for indoor use

void setup() {
  Serial.begin(115200);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);
  stopMotors();
}

void loop() {
  if (!Serial.available()) return;
  String line = Serial.readStringUntil('\n');
  line.trim();
  if (line == "PING") {
    Serial.println("PONG");
  } else if (line == "STOP") {
    stopMotors();
    Serial.println("OK");
  } else if (line == "COME") {
  driveForward(1500);
    Serial.println("DONE");
  } else if (line.startsWith("GOTO ")) {
    String dest = line.substring(5);
    if (dest == "kitchen") driveForward(3000);
    else if (dest == "desk") driveForward(1500);
    else if (dest == "bedroom") driveForward(4000);
    else driveForward(2000);
    Serial.println("DONE");
  }
}

void driveForward(unsigned long ms) {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, SPEED);
  analogWrite(ENB, SPEED);
  delay(ms);
  stopMotors();
}

void stopMotors() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
}
