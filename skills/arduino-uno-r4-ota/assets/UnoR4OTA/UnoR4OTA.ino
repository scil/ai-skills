#include <WiFiS3.h>
#include <ArduinoOTA.h>
#include "arduino_secrets.h"

char ssid[] = SECRET_SSID;
char wifiPassword[] = SECRET_WIFI_PASSWORD;
const unsigned long blinkInterval = 200;
unsigned long lastBlink = 0;
bool ledState = false;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(115200);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.println("Connecting to WiFi...");
    WiFi.begin(ssid, wifiPassword);
    delay(5000);
  }
  ArduinoOTA.begin(WiFi.localIP(), "uno-r4-wifi", SECRET_OTA_PASSWORD,
                   InternalStorage);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  Serial.print("Maximum OTA binary size: ");
  Serial.println(InternalStorage.maxSize());
  Serial.println("OTA ready");
}

void loop() {
  ArduinoOTA.poll();
  const unsigned long now = millis();
  if (now - lastBlink >= blinkInterval) {
    lastBlink = now;
    ledState = !ledState;
    digitalWrite(LED_BUILTIN, ledState);
  }
}
