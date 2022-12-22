//cons
/*  
 * Check:  http://www.electronoobs.com/eng_robotica_tut5_2_1.php
 * 
 * 
A basic receiver test for the nRF24L01 module to receive 6 channels send a ppm sum
with all of them on digital pin D2.
Install NRF24 library before you compile
Please, like, share and subscribe on my https://www.youtube.com/c/ELECTRONOOBS
 */

#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

#include <SFE_BMP180.h>
#include <Wire.h>

SFE_BMP180 bmp180;
int pinLed = 2;
int altura = 0;
double alturaFinalMin = 7.8;
double alturaFinalMax = 8.5;
double alturaActual = 0;


bool bmpIniciado = false;

double PresionNivelMar=1013.25; //presion sobre el nibel del mar en mbar





////////////////////// PPM CONFIGURATION//////////////////////////
#define channel_number 6  //set the number of channels
#define sigPin 2  //set PPM signal output pin on the arduino
#define PPM_FrLen 27000  //set the PPM frame length in microseconds (1ms = 1000µs)
#define PPM_PulseLen 400  //set the pulse length
//////////////////////////////////////////////////////////////////

int ppm[channel_number];

const uint64_t pipeIn =  0xE8E8F0F0E1LL;

RF24 radio(9, 10);

// The sizeof this struct should not exceed 32 bytes
struct MyData {
  byte throttle;
  byte yaw;
  byte pitch;
  byte roll;
  byte AUX1;
  byte AUX2;
};

MyData data;

void resetData() 
{
  // 'safe' values to use when no radio input is detected
  data.throttle = 0;
  data.yaw = 127;
  data.pitch = 127;
  data.roll = 127;
  data.AUX1 = 0;
  data.AUX2= 0;
  
  setPPMValuesFromData();
}

void getAltitude()
{
  altura = data.AUX2;
}

void setPPMValuesFromData()
{
  ppm[0] = map(data.throttle, 0, 255, 1000, 2000);
  ppm[1] = map(data.yaw,      0, 255, 1000, 2000);
  ppm[2] = map(data.pitch,    0, 255, 1000, 2000);
  ppm[3] = map(data.roll,     0, 255, 1000, 2000);
  ppm[4] = map(data.AUX1,     0, 1, 1000, 2000);
  ppm[5] = map(data.AUX2,     0, 1, 1000, 2000);  
  }

/**************************************************/

void setupPPM() {
  pinMode(sigPin, OUTPUT);
  digitalWrite(sigPin, 0);  //set the PPM signal pin to the default state (off)

  cli();
  TCCR1A = 0; // set entire TCCR1 register to 0
  TCCR1B = 0;

  OCR1A = 100;  // compare match register (not very important, sets the timeout for the first interrupt)
  TCCR1B |= (1 << WGM12);  // turn on CTC mode
  TCCR1B |= (1 << CS11);  // 8 prescaler: 0,5 microseconds at 16mhz
  TIMSK1 |= (1 << OCIE1A); // enable timer compare interrupt
  sei();
}

void setup()
{  

  pinMode(pinLed, OUTPUT);
  if (bmp180.begin())
    bmpIniciado = true;

  
  resetData();
  setupPPM();
  
  // Set up radio module
  radio.begin();
  radio.setDataRate(RF24_250KBPS); // Both endpoints must have this set the same
  radio.setAutoAck(false);

  radio.openReadingPipe(1,pipeIn);
  radio.startListening();
}

/**************************************************/

unsigned long lastRecvTime = 0;

void recvData()
{  
  while ( radio.available() ) {        
    radio.read(&data, sizeof(MyData));
    lastRecvTime = millis();
  }
}

void setDato(int numero){
  if(numero == 1){
    data.throttle = 255; 
  }else{
    data.throttle = 0;
  }
  data.yaw = 127;
  data.pitch = 127;
  data.roll = 127;
  data.AUX1 = 1;
  data.AUX2= 0;
}

/**************************************************/

void loop()
{
  if (bmpIniciado) {
    
    recvData();
    unsigned long now = millis();
    if ( now - lastRecvTime > 1000 ) {
    // signal lost?
    resetData();
    }
    if(altura == 1){
      char status;
      double T,P,A;
      while(alturaFinalMax < alturaActual || alturaFinalMin > alturaActual){
        status = bmp180.startTemperature();//Inicio de lectura de temperatura
        if (status != 0)
        {   
          delay(status); //Pausa para que finalice la lectura
          status = bmp180.getTemperature(T); //Obtener la temperatura
      
          if (status != 0)
          {
            status = bmp180.startPressure(3);//Inicio lectura de presión
            if (status != 0)
            {        
              delay(status);//Pausa para que finalice la lectura        
              status = bmp180.getPressure(P,T);//Obtenemos la presión
              if (status != 0)
              { 
                alturaActual= bmp180.altitude(P,PresionNivelMar);
              }      
            }      
          }   
        }

        if(alturaFinalMin > alturaActual){
          setDato(1);
        }
        else{
          setDato(0);
        }
        setPPMValuesFromData();
      }
    }else{
      setPPMValuesFromData();
    }
  
  }else{
    recvData();

    unsigned long now = millis();
    if ( now - lastRecvTime > 1000 ) {
    // signal lost?
    resetData();
    }
  
    setPPMValuesFromData();
  }
}

/**************************************************/

//#error Delete this line befor you cahnge the value (clockMultiplier) below
#define clockMultiplier 2 // set this to 2 if you are using a 16MHz arduino, leave as 1 for an 8MHz arduino

ISR(TIMER1_COMPA_vect){
  static boolean state = true;

  TCNT1 = 0;

  if ( state ) {
    //end pulse
    PORTD = PORTD & ~B00000100; // turn pin 2 off. Could also use: digitalWrite(sigPin,0)
    OCR1A = PPM_PulseLen * clockMultiplier;
    state = false;
  }
  else {
    //start pulse
    static byte cur_chan_numb;
    static unsigned int calc_rest;

    PORTD = PORTD | B00000100; // turn pin 2 on. Could also use: digitalWrite(sigPin,1)
    state = true;

    if(cur_chan_numb >= channel_number) {
      cur_chan_numb = 0;
      calc_rest += PPM_PulseLen;
      OCR1A = (PPM_FrLen - calc_rest) * clockMultiplier;
      calc_rest = 0;
    }
    else {
      OCR1A = (ppm[cur_chan_numb] - PPM_PulseLen) * clockMultiplier;
      calc_rest += ppm[cur_chan_numb];
      cur_chan_numb++;
    }     
  }
}
