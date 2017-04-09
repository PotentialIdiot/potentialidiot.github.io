//prototype 3, clean up
#include <Servo.h>
#include <Adafruit_NeoPixel.h>

#define PIN 13
Adafruit_NeoPixel strip = Adafruit_NeoPixel(4, PIN, NEO_GRB + NEO_KHZ800);

Servo myservo;
int angle = 0;
int newAngle = 0;
const int MaxChars = 4;
char strValue[MaxChars + 1];
int index = 0;
int phase = 0;

void setup()
{
  Serial.begin(9600);
  myservo.attach(9);
  angle = 45;
  Serial.write('1');

  strip.begin();
  strip.show(); // Initialize all pixels to 'off'
  strip.setBrightness(32);
}
void loop()
{}

void serialEvent()
{
  while (Serial.available())
  {
    char ch = Serial.read();
    Serial.write(ch);
    if (index < MaxChars && isDigit(ch))
    {
      strValue[index++] = ch;
    }
    else
    {
      // parse data
      strValue[index] = 0;
      newAngle = atoi(strValue);

      // 101 means phase 2
      if (newAngle == 101)
      {
        phase = 10;
        strip.setPixelColor(2, 0, 0, 255);
        strip.show();
      }
      
      if (newAngle == 102)
      {
        phase = 20;
        strip.setPixelColor(1, 0, 0, 255);
        strip.show();
      }

      if (newAngle == 103)
      {
        phase = 30;
        strip.setPixelColor(0, 0, 0, 255);
        strip.show();
      }

      if (newAngle == 104) //win
      {
        myservo.write(100);
        strip.setPixelColor(0, 0, 255, 0);
        strip.setPixelColor(1, 0, 255, 0);
        strip.setPixelColor(2, 0, 255, 0);
        strip.setPixelColor(3, 0, 255, 0);
        strip.show();
      }

      if (newAngle == 106) // First start
      {
        strip.setPixelColor(3, 0, 0, 255);
        strip.show();
      }
      
      // boundary check
      if (newAngle >= 0 && newAngle <= 100) {

        if (newAngle >= phase) {
          if (newAngle > angle)
          {
            for (; angle < newAngle; angle += 1) {
              myservo.write(angle);
              //delay(20);
            }
          }
          else
          {
            for (; angle >= newAngle; angle -= 1) {
              myservo.write(angle);
              //delay(20);
            }
          }
        }
        else
        {
          myservo.write(0);
          strip.setPixelColor(0, 255, 0, 0);
          strip.setPixelColor(1, 255, 0, 0);
          strip.setPixelColor(2, 255, 0, 0);
          strip.setPixelColor(3, 255, 0, 0);
          strip.show();
        }
        
      //strValue;
      //index = 0;
      angle = newAngle;
      }
      strValue;
      index = 0;
    }
  }
}
