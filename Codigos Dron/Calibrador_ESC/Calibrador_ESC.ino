//Se incluyen las librerias necesarias para la calibracion del regulador de voltaje
#include <Servo.h>

//Se define alguno parametros, tales como el maximo y minimo de la señal, el pin donde se conectara el regulador y el tiempo de espera de 1 seg.
#define MAX_SIGNAL 2000
#define MIN_SIGNAL 1000
#define MOTOR_PIN 9
int DELAY = 1000;

//Se inicializa la variable motor
Servo motor;

void setup() {
  Serial.begin(9600);//Se inicializa la ventana de comando con una frecuencia de 9600 MHz
  Serial.println("Bienvenido al calibrador del regulador de velocidad ESC.");
  Serial.println(" ");
  delay(1000);
  Serial.println("Iniciando Calibración...");
  Serial.println("Encienda la fuente y espere 2 seg");
  
  motor.attach(MOTOR_PIN);
  motor.writeMicroseconds(MAX_SIGNAL);
  motor.writeMicroseconds(MIN_SIGNAL);
  

  Serial.println("\n");  
  Serial.println("El regulador fue calibrado");
  Serial.println("--------------------------------");
  Serial.println("Tipee un valor entre 1000 y 2000 para variar la velocidad del motor");

}

void loop() {
   
  if (Serial.available() > 0)
  {
    int DELAY = Serial.parseInt();
    if (DELAY > 999)
    {
      
      motor.writeMicroseconds(DELAY);
      float SPEED = (DELAY-1000)/10;
      Serial.print("\n");
      Serial.println("Velocidad del motor:"); Serial.print("  "); Serial.print(SPEED); Serial.print("%"); 
    }     
  }
}
 
