//Se implementan las librerias correspondientes para el funcionamiento del control remoto
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>


//Se especifica la cantidad de informacion enviada por cada paquete. 6 Bytes de 8 bits
const uint64_t pipeOut = 0xE8E8F0F0E1LL; //IMPORTANT: The same as in the receiver

//Se especifica los pines a utilizar para la antena NRF24
RF24 radio(9, 10); // select  CSN  pin

// Se especifica la estructura/bus de datos que se enviara por la antena NRF24
struct MyData {
  byte throttle;
  byte yaw;
  byte pitch;
  byte roll;
  byte AUX1;
  byte AUX2;
};

//Se inicializa una variable MyData, el cual contendra la informacion de las rotaciones del dron
MyData data;

//Metodo que permite resetear los valores de la variable inicializada anteriormente
void resetData() 
{    
  data.throttle = 0;
  data.yaw = 127;
  data.pitch = 127;
  data.roll = 127;
  data.AUX1 = 0;
  data.AUX2 = 0;
}


//Metodo Setup, que inicializa la comunicacion de la antena NRF24
void setup()
{
  Serial.begin(250000);
  Serial.print("Iniciando Control");     Serial.print("\n");
  radio.begin();//Se iniciliza la comunicacion
  radio.setAutoAck(false);
  radio.setDataRate(RF24_250KBPS);//Se setea la velocidad de envio de informacion
  radio.openWritingPipe(pipeOut);//Se especifica la cantidad de informacion enviada por cada paquete
  resetData();

}


//Metodo que permite mapear la posicion de un Joystick, retorna los valores correspondiente.
int mapJoystickValues(int val, int lower, int middle, int upper, bool reverse)
{
  val = constrain(val, lower, upper);
  if ( val < middle )
    val = map(val, lower, middle, 0, 128);
  else
    val = map(val, middle, upper, 128, 255);
  return ( reverse ? 255 - val : val );
}


//Metodo Loop, el cual lee la informacion de los joystick, aplica el filtro del metodo mapJoystickValues y envia el paquete de dato.
void loop()
{
  Serial.print("Leyendo Joystick \n");
  data.throttle = mapJoystickValues( analogRead(A0), 13, 524, 1015, true );
  data.yaw      = mapJoystickValues( analogRead(A1),  1, 505, 1020, true );
  data.pitch    = mapJoystickValues( analogRead(A2), 12, 544, 1021, true );
  data.roll     = mapJoystickValues( analogRead(A3), 34, 522, 1020, true );
  data.AUX1     = digitalRead(4); //The 2 toggle switches
  data.AUX2     = digitalRead(5);
  
  radio.write(&data, sizeof(MyData));
}
