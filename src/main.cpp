#include <Arduino.h>
#include "_web.h"
#include <esp_task_wdt.h>
#include <esp_heap_caps.h>
#ifndef _LIB
    #define _LIB
    #include "_wifi.h"
    #include "_download.h"
    #include"_as7265x.h"
    #include "_model_.h"
#endif
#ifndef SPIF_LIB
    #define SPIF_LIB
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
    esp_task_wdt_init(100, true);
    pinMode(LED_PIN, OUTPUT);
    spiffs.start();
    web.init(&download,&as7265x,&model,&spiffs,&wifi);
    as7265x.start();
    wifi.init(&spiffs);
    wifi.start();
    web.start();
    //spiffs.load_data("/static/index.js",obj);
    obj.print_str();
    //spiffs.print_files();
    if(spiffs.exist("/error_model"))
    {
        spiffs.load_data("/error_model",obj);
        if(obj.get_data_str()=="0")
        {
            wifi.set_state("E6");
            spiffs.delete_data("/model");
            spiffs.delete_data("/model_name");
        }
        else
            wifi.set_state("E7");
        spiffs.delete_data("/error_model");
    }
    if(spiffs.exist("/new_model"))
    {
        String state;
        spiffs.load_data("/new_model",obj);
        spiffs.delete_data("/new_model");
        if(model.start(obj))
        {
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
        
        wifi.set_update();
    }
    else if(spiffs.exist("/model") || true)
    {
        spiffs.save_data("/error_model","0");
        
        spiffs.load_data("/model",obj);
        
        model.start(obj);
        spiffs.delete_data("/error_model");        
    }
    
    obj.clear();
    web.load_spiffs_params();
    //model.set_datas(as7265x.get_datas());
    //model.predict().print();
}


void loop() {
    delay(1000);
    model.set_datas(as7265x.get_datas());
    model.predict().print();

    if(web.get_flag_download())
        web._download();
    digitalWrite(LED_PIN,HIGH);
    delay(500);
    digitalWrite(LED_PIN,LOW);
    delay(500);

}




