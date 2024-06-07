#include <SoftwareSerial.h>
#define IM920_BUFFER_SIZE 80

SoftwareSerial IM920Serial(10, 11); // RX, TX


class IM920Driver {
  public:
    char read();
    IM920Driver(SoftwareSerial *ser);


  private:
    uint8_t _line1[IM920_BUFFER_SIZE];
    uint8_t _line2[IM920_BUFFER_SIZE];
    uint8_t *_current_line = _line1;
    uint8_t *_last_line = _line2;
    uint16_t _idx = 0;
    uint16_t _line_length = 0;
    bool _line_changed = false;
}

int n;
char c = 0;
char buff[IM920_BUFFER_SIZE];

void setup() {
  Serial.begin(19200);
  IM920Serial.begin(9600);
}

void loop() {
  if (IM920Serial.available()) {
      c = IM920Serial.read();
      _idx = min(IM920_BUFFER_SIZE, _idx);
      _current_line[_idx] = c;
      _idx++;

      if (c == '\n') {
          _current_line[_idx] = '\0';

          uint8_t *tmp = _current_line;
          _current_line = _last_line;
          _last_line = tmp;

          _line_length = _idx;
          _idx = 0;
          _line_changed = true;
      }
  }

  if (_line_changed) {
    _line_changed = false;
    for (int i = 0; i < _line_length; i++) {
      buff[i] = _last_line[i];
    }
    buff[_line_length] = '\0';

    if (strcmp(buff, "OK\r\n") != 0 && strcmp(buff, "NG\r\n") != 0) {
      Serial.println(buff);
    }

  }

  delay(1000);
}

char IM920Driver::read() {
  for (int i= 0; i < 10; i++) 
}
