#include <WiFi.h>

class Wifi
{
    private:
        bool active;
    public:
        Wifi()
        {
            active=false;
        }
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
            active=true;
            return true;
        }
        String get_ip()
        {
            if(!active)
                return String();
            Serial.println(WiFi.localIP());
            Serial.println(String(WiFi.localIP().toString()));
            return WiFi.localIP().toString();
        }
};