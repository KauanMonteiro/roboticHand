#include <Servo.h>

Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;

void setup() {
  // Inicializa os servos nos pinos correspondentes
  servo1.attach(2);
  servo2.attach(3);
  servo3.attach(4);
  servo4.attach(5);
  servo5.attach(6);

  // Inicia a comunicação serial
  Serial.begin(9600);
}

void loop() {
  // Verifica se há dados disponíveis para leitura na porta serial
  if (Serial.available() > 0) {
    String comando = Serial.readStringUntil('\n');  // Lê o comando enviado pelo Python
    int pino = comando.substring(0, comando.indexOf(':')).toInt();  // Pino
    int estado = comando.substring(comando.indexOf(':') + 1).toInt();  // Estado (0 ou 1)

    // Controle dos servos baseado no comando recebido
    if (pino == 6) {
      if (estado == 1) servo1.write(180);  // Abrir
      else servo1.write(0);  // Fechar
    } else if (pino == 7) {
      if (estado == 1) servo2.write(180);  // Abrir
      else servo2.write(0);  // Fechar
    } else if (pino == 8) {
      if (estado == 1) servo3.write(180);  // Abrir
      else servo3.write(0);  // Fechar
    } else if (pino == 9) {
      if (estado == 1) servo4.write(180);  // Abrir
      else servo4.write(0);  // Fechar
    } else if (pino == 10) {
      if (estado == 1) servo5.write(180);  // Abrir
      else servo5.write(0);  // Fechar
    }
  }
}

