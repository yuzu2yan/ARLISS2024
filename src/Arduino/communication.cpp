#include <Wire.h>
#include <SoftwareSerial.h>

#define IM920_RX_PIN 10
#define IM920_TX_PIN 11

SoftwareSerial IM920Serial(IM920_RX_PIN, IM920_TX_PIN);

void setup() {
  IM920Serial.begin(9600);
  Wire.begin(0x08);
  Serial.begin(9600);
  IM920Serial.print("ECIO");
  delay(1000);
}

void loop() {
  IM920Serial.print("TXDATes\r\n");
  delay(1000);
}
