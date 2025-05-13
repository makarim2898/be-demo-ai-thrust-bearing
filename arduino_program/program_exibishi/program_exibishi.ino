#include <Adafruit_NeoPixel.h>

#define PIN        A0      // Pin yang terhubung ke DIN LED strip
#define NUMPIXELS  9     // Jumlah LED di strip-mu, ubah sesuai kebutuhan

Adafruit_NeoPixel strip(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

//inisaialisasi input
//modifikasi hanya kirim sinyal trigger saja
#define start_trigger  9//diff down di plc karena pc delay
#define reset_trigger 10 //diff up di plc biar continous loop di python

//inisialisasi output  
#define ok_trigger 5 //untuk trigger plc

void matikan_lampu(int pin_out = -1){
    // matikan semua output
    if (pin_out == -1){
        digitalWrite(ok_trigger, HIGH);
      }
    else{
        digitalWrite(pin_out, HIGH);
      }
}

void setup() {
  // definisi pin INPUT
  pinMode(reset_trigger, INPUT_PULLUP);
  pinMode(start_trigger, INPUT_PULLUP);

  //definisi pin output
  pinMode(ok_trigger, OUTPUT);
  
  strip.begin();           
  strip.show();            // Matikan semua LED awalnya
  strip.fill(strip.Color(255, 255, 255)); // Putih
  strip.show();            // Tampilkan warna
  // inisialisasi serial
  Serial.begin(115200);

  //tungggu hingga serial terhubung, berkedip jika belum terhubung
  while(!Serial){
    blink_output(LED_BUILTIN, 3, 5);
  }

  // matikan semua output
  matikan_lampu();
}

void loop() {
  read_data_python();
  read_pin_input();
}
//****************** ini yang kirim serial ke python ***************************
void read_pin_input() {
  if (digitalRead(start_trigger)) {
    Serial.println("start_scan");
    delay(100);
  } 
  //bagian reset didalamnya di tambahkan lagi kondisi bypass dan trigger karena biar gak ngunci loop nya
  else if(not digitalRead(reset_trigger)){
      Serial.println("reset_scan");
      matikan_lampu();
      delay(100);
  }

  else {
    Serial.println("no_trigger");
    delay(100);
  }
}

//****************** ini yang baca dari python ***************************
void read_data_python() {
  //jika ada data di serial lakukan pembacaan
  if (Serial.available() > 0) {
      // Membaca data yang masuk
      String data = Serial.readString();
      data.trim();
      if(data == "out_ok"){
        digitalWrite(ok_trigger, LOW);
        Serial.println("hasil nya oke");
//        delay(2000);
        }
      else if(data == "out_ng"){
        digitalWrite(ok_trigger, HIGH);
        Serial.println("hasil nya jelek");
        }
      // Mengembalikan data yang diterima ke port serial
      Serial.print("Pesan yang diterima arduino: ");
      Serial.println(data);
    }
}

void blink_output(int pin_out, int repetisi, int interval) {
  interval = interval * 100;
  for (int i = 0; i < repetisi; i++) {
    digitalWrite(pin_out, HIGH);
    delay(interval);
    digitalWrite(pin_out, LOW);
    delay(interval);
  }
}
