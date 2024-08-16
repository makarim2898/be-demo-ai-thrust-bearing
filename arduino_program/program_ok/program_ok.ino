//inisaialisasi input
#define input_trigger 7
#define reset_trigger 8

//inisialisasi output  
#define out_ok 13
#define out_ng 12

void matikan_lampu(int pin_out = -1){
    // matikan semua output
    if (pin_out == -1){
        digitalWrite(out_ok, HIGH);
        digitalWrite(out_ng, HIGH);
      }
    else{
        digitalWrite(pin_out, HIGH);
      }
}

void setup() {
  // definisi pin INPUT
  pinMode(reset_trigger, INPUT_PULLUP);
  pinMode(input_trigger, INPUT_PULLUP);

  //definisi pin output
  pinMode(out_ok, OUTPUT);
  pinMode(out_ng, OUTPUT);

  // inisialisasi serial
  Serial.begin(115200);

  //tungggu hingga serial terhubung, berkedip jika belum terhubung
  while(!Serial){
    blink_output(out_ok, 3, 5);
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
  if (digitalRead(input_trigger) == LOW) {
    Serial.println("start_scan");
    delay(100);
  } 
  else if(digitalRead(reset_trigger) == LOW){
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
      if(data == "out_ok"){
        digitalWrite(out_ok, LOW);
        }
      else if(data == "out_ng"){
        blink_output(out_ng, 3, 5);
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
