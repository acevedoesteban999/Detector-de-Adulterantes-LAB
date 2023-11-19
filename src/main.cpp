#include <Arduino.h>
#include "_web.h"
#include <ESP.h>
#include <esp_task_wdt.h>
#include <esp_heap_caps.h>
#include "_wifi.h"
#include "_download.h"
#include"_as7265x.h"
#include "_spiffs.h"
#include "_object.h"
#include "_model.h"

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
    esp_get_free_heap_size();
    pinMode(LED_PIN, OUTPUT);
    spiffs.start();
    as7265x.start();
    wifi.init(&spiffs,&model);
    wifi.start();
    model.init(&spiffs);
    if(spiffs.exist("/error_model"))
    {
        spiffs.load_data("/error_model",obj);
        String _error=obj.get_data_str();
        if(_error =="0")
        {
            wifi.set_state("E6");
            spiffs.delete_data("/model");
            spiffs.delete_data("/model_name");
        }
        else if(_error == "1")
            wifi.set_state("E7");
        else
            wifi.set_state("E3");
    }
    if(spiffs.exist("/model"))
    {
        spiffs.save_data("/error_model","0");
        
        spiffs.load_data("/model",obj);
        model.start(obj);
        spiffs.delete_data("/error_model");        
    }
    web.init(&download,&as7265x,&model,&spiffs,&wifi);
    web.start();
    web.load_spiffs_params();
    obj.clear();
    
    
}


void loop() {
    // unsigned int freeRAM = ESP.getFreeHeap();

    // Serial.print("Memoria RAM libre: ");
    // Serial.print(freeRAM);
    // Serial.println(" bytes");

    if(wifi.get_flag_download())
        web._download_model();
    digitalWrite(LED_PIN,HIGH);
    delay(500);
    digitalWrite(LED_PIN,LOW);
    delay(500);

}




