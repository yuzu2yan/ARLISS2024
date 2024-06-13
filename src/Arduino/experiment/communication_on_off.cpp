#include <SoftwareSerial.h>
#include "IM920Driver.h"

#define IM920_RX_PIN 10
#define IM920_TX_PIN 11

SoftwareSerial IM920Serial(IM920_RX_PIN, IM920_TX_PIN);
IM920Driver im920(&IM920Serial);

int _send_count = 0;
bool _send_flag = true;

void setup() {
  IM920Serial.begin(9600);
  Serial.begin(19200);

  // Set ECIO mode
  im920.send("ECIO");
  delay(1000);
}

void loop() {
  char buff[IM920_BUFFER_SIZE];
  while (im920.available()) {
    im920.read();

    // If there is a line break
    if (im920.get_line_changed()) {
      im920.get_last_line(buff);
      char signal[2];
      signal[0] = buff[11];
      signal[1] = buff[12];

      if (strcmp(signal, "FF") == 0) {
        im920.send("TXDA Stop Connection");
        Serial.println("TXDA Stop Connection");
        _send_flag = false;

        // Start after 10 seconds
        delay(10000);
        im920.send("TXDA Start Connection");
        Serial.println("TXDA Start Connection");
        _send_flag = true;
      } else if (strcmp(signal, "ON") == 0) {
        im920.send("TXDA Start Connection");
        Serial.println("TXDA Start Connection");
        _send_flag = true;
      }
      signal[0] = buff[11] = "N";
      signal[1] = buff[12] = "N";
    }
  }
  delay(50);

  _send_count++;
  if (_send_count >= 50 && _send_flag == true) {
    im920.send("TXDA Test");
    Serial.println("TXDA Test");
    _send_count = 0;
    delay(100);
  }
}