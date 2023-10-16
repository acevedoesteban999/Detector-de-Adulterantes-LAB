#include "SPIFFS.h"

class Spiffs
{
    private:
        bool active;
    public:
        Spiffs()
        {
            active=false;
        }
        ~Spiffs()
        {}
        bool start()
        {
            if(!SPIFFS.begin(true))
            {
                Serial.println("An Error has occurred while mounting SPIFFS");
                active=false;
                return false;
            }
            active=true;
            Serial.println("Files:");
            File root=SPIFFS.open("/");
            File file=root.openNextFile();
            while(file)
            {
                Serial.println(file.name());
                file=root.openNextFile();
            }
            return true;
        }
        bool save_model()
        {
            if(active==true)
            {	
                File file = SPIFFS.open("/a.txt", "w");
                int bytesWritten = file.print("TEST SPIFFS");
                file.close();
            }
            return true;
        }
};