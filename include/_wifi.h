#include <WiFi.h>

class Wifi
{
    public:
        Wifi()
        {}
        ~Wifi()
        {}
        bool start()
        {
            WiFi.mode(WIFI_STA);
            WiFi.disconnect();
            WiFi.begin("iPhone 6 Plus", "melon123445");
            Serial.print("Connecting to WiFi ..");
            int count=0;
            while (WiFi.status() != WL_CONNECTED)
            {
                Serial.print('.');  
                if(count++==10)
                    return false;
                delay(1000);
            }
            Serial.println(WiFi.localIP());
            return true;
        }
};