//#include <Adafruit_NeoPixel.h>
//
//#define PIN        A1      // Pin yang terhubung ke DIN LED strip
//#define NUMPIXELS  15     // Jumlah LED di strip-mu, ubah sesuai kebutuhan
//
//Adafruit_NeoPixel strip(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);
//
//void setup() {
//  strip.begin();           
//  strip.show();            // Matikan semua LED awalnya
//  strip.fill(strip.Color(255, 255, 255)); // Putih
//  strip.show();            // Tampilkan warna
//}
//
//void loop() {
//  // Tidak ada yang perlu dilakukan di loop
//}

#include <Adafruit_NeoPixel.h>

#define PIN        A1      // Pin yang terhubung ke DIN LED strip
#define NUMPIXELS  15     // Jumlah LED di strip-mu

Adafruit_NeoPixel strip(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  strip.begin();           
  strip.show();            // Matikan semua LED awalnya
}

void loop() {
  for (int i = 0; i < NUMPIXELS; i++) {
//    strip.clear();
    strip.setPixelColor(i, strip.Color(255, 0, 255)); // Putih
    strip.show();
    delay(100); // Kecepatan gerakan
  }

  strip.clear();
}
