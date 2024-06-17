#include <Wire.h>

float latitude;
float longitude;

void setup() {
  Wire.begin(0x08);
  Wire.onReceive(receiveEvent);
  Serial.begin(9600);
}

void loop() {
  // Serial.print("Latitude: ");
  // Serial.println(latitude, 6);
  // Serial.print("Longitude: ");
  // Serial.println(longitude, 6);
  // delay(1000);  // wait for a second
}

void receiveEvent() {
  int i = 0;

  Wire.requestFrom(0x00, 16); // latitude
  while (Wire.available()) {
    char c = Wire.read();
    latitude[i++] = (float)c;
    Serial.print(c);
  }
  Serial.println();

  i = 0;
  Wire.requestFrom(0x01, 16); // longitude
  while (Wire.available()) {
    char c = Wire.read();
    longitude[i++] = (float)c;
    Serial.print(c);
  }
  Serial.println();
}
