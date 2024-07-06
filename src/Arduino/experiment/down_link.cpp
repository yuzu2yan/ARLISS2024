#include <Wire.h>

void setup() {
  Wire.begin(0x04);  // I2Cアドレスを0x08に設定
  Wire.onReceive(receiveEvent);  // データ受信時のイベントハンドラを設定
  Serial.begin(9600);  // シリアル通信を初期化
}

void loop() {
  // メインループは空でもOK
  delay(100);
}

void receiveEvent(int howMany) {
  while (Wire.available()) {
    char c = Wire.read();  // I2Cデータを読み取る
    Serial.print(c);  // シリアルモニターに表示
  }
  Serial.println();
}
