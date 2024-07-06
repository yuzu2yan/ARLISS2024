#include <Wire.h>
#include <SoftwareSerial.h>

#define IM920_RX_PIN 10
#define IM920_TX_PIN 11

SoftwareSerial IM920Serial(IM920_RX_PIN, IM920_TX_PIN);

void setup() {
  IM920Serial.begin(9600);
  Wire.begin(0x04);  // I2Cアドレスを0x08に設定
  Wire.onReceive(receiveEvent);  // データ受信時のイベントハンドラを設定
  Serial.begin(9600);  // シリアル通信を初期化
  IM920Serial.print("ECIO");
}

void loop() {
  // メインループは空でもOK
  delay(100);
}

void receiveEvent(int howMany) {
  char data[howMany + 1];
  for (int i = 0; i < howMany; i++) {
    data[i] = Wire.read();  // I2Cデータを読み取る
  }
  data[howMany] = '\0';  // 文字列の終端を設定
  Serial.println(data);  // シリアルモニタに表示
  String dataStr = String(data);
  IM920Serial.print("TXDA" + dataStr + "\r\n");  // IM920にデータを送信
}
