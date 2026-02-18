// Estrutura: [0:pino buzzer, 1:estado luz, 2:buzzer on, 3:tempo, 4:pino ldr, 5:frequencia, 6:THRESHOLD INDIVIDUAL]
int b1[7] = {16, 0, 0, 0, 26, 262 * 2, 1700};  // Threshold 2000 para LDR1
int b2[7] = {17, 0, 0, 0, 25, 294 * 2, 1700}; // Threshold 1800 para LDR2
int b3[7] = {5, 0, 0, 0, 33, 331 * 2, 1700};  // Threshold 2200 para LDR3
int b4[7] = {18, 0, 0, 0, 32, 349 * 2, 1700}; // Threshold 1900 para LDR4
int b5[7] = {19, 0, 0, 0, 35, 392 * 2, 1900}; // Threshold 2100 para LDR5
int b6[7] = {12, 0, 0, 0, 34, 440 * 2, 1700}; // Threshold 1700 para LDR6

#include <WiFi.h>
#include "esp_wifi.h"
#include "esp_bt.h"

void setup() {
  Serial.begin(9600);
  delay(1000);

  // --- Desativa WiFi e Bluetooth ---
  WiFi.mode(WIFI_OFF);
  esp_wifi_stop();
  esp_wifi_deinit();
  esp_bt_controller_disable();

  // Configura os pinos dos buzzers com PWM
  ledcAttach(b1[0], b1[5], 8);
  ledcAttach(b2[0], b2[5], 8);
  ledcAttach(b3[0], b3[5], 8);
  ledcAttach(b4[0], b4[5], 8);
  ledcAttach(b5[0], b5[5], 8);
  ledcAttach(b6[0], b6[5], 8);
  
  Serial.println("Sistema iniciado!");
  Serial.println("Monitorando LDRs com thresholds individuais:");
  Serial.println("B1:2000 | B2:1800 | B3:2200 | B4:1900 | B5:2100 | B6:1700");
}

void loop() {
  control_buzzer(b1);
  control_buzzer(b2);
  control_buzzer(b3);
  control_buzzer(b4);
  control_buzzer(b5);
  control_buzzer(b6);
  
  delay(10); // Pequeno delay para estabilidade

}


// Função modificada para usar threshold individual
bool isLight(int pin, int threshold) {
  int leitura = analogRead(pin);
  return leitura < threshold; // Usa o threshold específico deste LDR
}

void control_buzzer(int buzzer[7]) {
  bool is_light = isLight(buzzer[4], buzzer[6]); // Passa o threshold individual
  
  // Mostra leitura no Serial Monitor (opcional - comentar se quiser)
  // Serial.print("LDR pino "); Serial.print(buzzer[4]);
  // Serial.print(": "); Serial.print(analogRead(buzzer[4]));
  // Serial.print(" | Threshold: "); Serial.println(buzzer[6]);
  
  if (!is_light && !buzzer[1]) {
    buzzer[1] = !buzzer[1];
  } else if (is_light && buzzer[1]) {
    buzzer[1] = !buzzer[1];
    
    Serial.print("Tocando buzzer no pino: ");
    Serial.println(buzzer[0]);
    
    ledcWriteTone(buzzer[0], buzzer[5]);
    buzzer[2] = true;
    buzzer[3] = millis();
  }

  if (buzzer[2] && (millis() - buzzer[3] > 600)) {
    ledcWriteTone(buzzer[0], 0);
    buzzer[2] = false;
    // Serial.print("Parando buzzer pino: ");
    // Serial.println(buzzer[0]);
  }
}

