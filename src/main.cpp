#include <Arduino.h>
#include "_web.h"
#ifndef _LIB
    #define _LIB
    #include "_wifi.h"
    #include "_download.h"
    #include"_as7265x.h"
    #include "_model_.h"
    #include "_spiffs.h"
#endif
#ifndef OBJ_LIB
    #define OBJ_LIB
    #include "_object.h"
#endif
#define LED_PIN 2

Web web;
Model model;
As7265x as7265x;
Download download;
Wifi wifi;
Spiffs spiffs;
Object obj;
Object obj1;
void setup() {
    Serial.begin(115200);
    pinMode(LED_PIN, OUTPUT);
    spiffs.start();
    //spiffs.print_files();
    web.init(&download,&as7265x,&model,&spiffs,&wifi);
    as7265x.start();
    wifi.start();
    web.start();
    web.load_spiffs_params();
}

void loop() {
    if(web.get_flag_download())
        web._download();
    digitalWrite(LED_PIN,HIGH);
    delay(500);
    digitalWrite(LED_PIN,LOW);
    delay(500);
}




