#include <Wire.h>
#include <SoftwareSerial.h>

#define IM920_RX_PIN 10
#define IM920_TX_PIN 11

SoftwareSerial IM920Serial(IM920_RX_PIN, IM920_TX_PIN);

void setup() {
  IM920Serial.begin(9600);
  Wire.begin(0x04);  
  Wire.onReceive(receiveEvent);  
  Serial.begin(9600);  
  IM920Serial.print("ECIO");
}

void loop() {
  delay(100);
}

void receiveEvent(int howMany) {
  char data[howMany + 1];
  for (int i = 0; i < howMany; i++) {
    data[i] = Wire.read();  
  }
  data[howMany] = '\0';  
  Serial.println(data);  
  String dataStr = String(data);
  IM920Serial.print("TXDA" + dataStr + "\r\n");  
}
