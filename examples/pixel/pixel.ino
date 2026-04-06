#include <ArduinoJson.h>
#include <Adafruit_NeoPixel.h>

const int pixelPin = 6;
const int pixelCount = 4;

Adafruit_NeoPixel pixels(pixelCount, pixelPin, NEO_GRB + NEO_KHZ800);

void setup() {
  Serial.begin(115200);
  
  pixels.begin();
  pixels.setBrightness(15);
  pixels.clear();
}

void setColor(int r, int g, int b) {
  pixels.clear();

  pixels.fill(pixels.Color(r, g, b), 0, pixelCount);

  pixels.show();
}

void loop() {

  if (Serial.available()) {
    JsonDocument doc;
    DeserializationError error = deserializeJson(doc, Serial);

    if (!error) {
      String type = doc["type"];
      
      if(type == "pixel") {
        int r = doc["r"];
        int g = doc["g"];
        int b = doc["b"];

        setColor(r, g, b);
      }
    }
  }
}
