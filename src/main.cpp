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
void setup() {
    Serial.begin(115200);
    pinMode(LED_PIN, OUTPUT);
    spiffs.start();
    web.init(&download,&as7265x,&model,&spiffs,&wifi);
    
    as7265x.start();
    wifi.start();
    web.start();
    if(spiffs.exist("/error_model"))
    {
        wifi.set_state("E6");
    }
    if(spiffs.exist("/new_model"))
    {
        String state;
        spiffs.load_data("/new_model",obj);
        spiffs.delete_data("/new_model");
        spiffs.save_data("/error_model","_");
        if(model.start(obj))
        {
            spiffs.delete_data("/error_model");
            if(spiffs.save_data("/model",obj))
            {
                spiffs.load_data("/new_model_name",obj);
                spiffs.delete_data("/new_model_name");
                spiffs.save_data("/model_name",obj);
                state="OK";
            }
            else
                state="E2";
        }
        else
            state="E3";
        wifi.set_state(state);
        
        wifi.set_download();
    }
    else
    {
        spiffs.load_data("/model",obj);
        model.start(obj);
    }
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




