#pragma once
#include "SPIFFS.h"
#include "_object.h"

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
            return true;
        }
        void print_files(bool path=false)
        {
            Serial.println("Files:");
            File root=SPIFFS.open("/");
            File file=root.openNextFile();
            while(file)
            {
                
                if(path)
                    Serial.println(file.path());
                else
                    Serial.println(file.name());
                
                file=root.openNextFile();
            }
        }
        bool save_data(String dir,Object&obj)
        {
            if(active==false)
                return false;
            File file = SPIFFS.open(dir, "w");
            if(!file)
                return false;
            //int bytesWritten = file.print("TEST SPIFFS");
            int bytesWritten=file.write(obj.get_data(),obj.get_count());
            file.close();
            
            return true;
        }
        bool exist(String dir)
        {
            return SPIFFS.exists(dir);
        }
        bool save_data(String dir,String str)
        {
            if(active==false)
                return false;
            File file = SPIFFS.open(dir, "w");
            int bytesWritten = file.print(str);
            file.close();
            return true;
        }
        
        bool load_data(String dir,Object&obj)
        {
            if(active==false)
                return false;
            obj.clear();
            if(!SPIFFS.exists(dir))
                return false; 
            File file = SPIFFS.open(dir, "r");
            while(file.available())
            {
                size_t size = file.available();
                uint8_t buff[1024];
                int c=file.read(buff, ((size > sizeof(buff)) ? sizeof(buff) : size));
                obj.append(buff,c);
            }
            file.close();
            return true;
        }
        bool delete_data(String dir)
		{
            if(exist(dir))
			    return SPIFFS.remove(dir);
            return true;
		}
};