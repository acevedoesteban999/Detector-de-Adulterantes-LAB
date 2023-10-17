#include <Arduino.h>
#include"_as7265x.h"
#include "_model_.h"
#include "_download.h"
#include "_wifi.h"
#include "_web.h"
#ifndef OBJ_LIB
    #define OBJ_LIB
    #include "_object.h"
#endif
#include "_spiffs.h"
#define LED_PIN 2

Web web;
Model model;
As7265x as7265x;
Download_Model download_model;
Wifi wifi;
Spiffs spiffs;
Object obj;
void setup() {
    Serial.begin(115200);
    pinMode(LED_PIN, OUTPUT);

    spiffs.start();
    wifi.start();
    web.start();
    as7265x.start();
    //model.predict();
    if(download_model.download("https://raw.githubusercontent.com/Esteban1914/files/tesis/asmcas.edbm",obj)) 
    {
        Serial.println("Download model");
        if(spiffs.save_data("/model",obj))
        {
            Serial.println("Saved model");
        }

    }
    if(spiffs.load_data("/model",obj))
    {
        Serial.println("Load model");
        if(model.start(obj))
        {
            Serial.println("Start model");
            obj.clear();
            float*datas=as7265x.get_datas();
            if (datas!=nullptr)
                model.predict(datas);
            else
                Serial.println("No Datas");
        }
        
    }
    
    //WiFi.disconnect()
    // server.on("/a", HTTP_GET, [](AsyncWebServerRequest *request){
    //     request->send(SPIFFS, "/index.html");
    // });
    // server.on("/hi", HTTP_GET, [](AsyncWebServerRequest *request)
    // {
    //     request->send(200, "text/plain", "Hello AsyncWebServer!");
    // });
    // server.begin();
    ////////////////////////AP//////////////////////////
    //WiFi.mode(WIFI_AP)
    //WiFi.softAP("ESP32", "ESP32");
    ////////////////////////SCAN//////////////////////////
    // Serial.println("scan start");
    // WiFi.scanNetworks will return the number of networks found
    //   int n = WiFi.scanNetworks();
    //   Serial.println("scan done");
    //   if (n == 0) {
    //       Serial.println("no networks found");
    //   } else {
    //     Serial.print(n);
    //     Serial.println(" networks found");
    //     for (int i = 0; i < n; ++i) {
    //       // Print SSID and RSSI for each network found
    //       Serial.print(i + 1);
    //       Serial.print(": ");
    //       Serial.print(WiFi.SSID(i));
    //       Serial.print(" (");
    //       Serial.print(WiFi.RSSI(i));
    //       Serial.print(")");
    //       Serial.println((WiFi.encryptionType(i) == WIFI_AUTH_OPEN)?" ":"*");
    //       delay(10);
    //     }
    //   }
    //   Serial.println("");
    //   // Wait a bit before scanning again
    //   delay(5000);
    /////////////////////////CONNECT///////////////////////
    
    
}

void loop() {
    digitalWrite(LED_PIN,HIGH);
    delay(1000);
    digitalWrite(LED_PIN,LOW);
    delay(1000);
}




