#include <WiFi.h>
#include <ESPmDNS.h>
#ifndef OBJ_LIB
    #define OBJ_LIB
    #include "_object.h"
#endif
#ifndef SPIF_LIB
    #define SPIF_LIB
    #include "_spiffs.h"
#endif
class Wifi
{
    private:
        bool active;
        bool update;
        
        String state;
        String ssid,pass,ssid_ap,pass_ap;
        Spiffs*spiffs;
    public:
        Wifi()
        {
            active=false;
            update=false;
        }
        ~Wifi()
        {}
        void init(Spiffs*spiffs)
        {
            this->spiffs=spiffs;
        }
        bool create_ap()
        { 
            Object obj;
            if(spiffs->exist("/ap_ssid")&&spiffs->exist("/ap_pass"))
            {
                spiffs->load_data("/ap_ssid",obj);
                ssid_ap=obj.get_data_str();
                spiffs->load_data("/ap_pass",obj);
                pass_ap=obj.get_data_str();
            }
            else
            {
                ssid_ap="ESP32_AP";
                pass_ap="ESP32_PASS";
                spiffs->save_data("/ap_ssid",ssid);
                spiffs->save_data("/ap_pass",pass);
            }
            WiFi.disconnect();
            WiFi.mode(WIFI_AP);
            // if (!WiFi.config(ip, gateway, subnet,primaryDNS,secondaryDNS)) 
            //     return false;
            
            WiFi.softAP(ssid_ap, pass_ap);
            //if (!MDNS.begin(hostname))
            //   return false;
            //WiFi.setHostname(hostname.c_str());
            return true;
        }
        void set_update()
        {
            update=true;
        }
        void reset_update()
        {
            update=false;
        }
        bool get_update()
        {
            return update;
        }
        bool connect_wifi(String ssid,String pass)
        {
            WiFi.disconnect();
            WiFi.mode(WIFI_STA);
            WiFi.begin(ssid, pass);
            int count=0;
            while (WiFi.status() != WL_CONNECTED)
            {
                if(count++==10)
                    return false;
                delay(1000);
            }
            return true;
        }
        bool start()
        {
            active=create_ap();
            //active=connect_wifi("iPhone 6 Plus","melon123445");
            return active;
            
        }
        void set_ssid_pass(String ssid,String pass)
        {
            this->ssid=ssid;
            this->pass=pass;
        }
        String get_ssid()
        {
            return ssid;
        }
        String get_pass()
        {
            return pass;
        }
        String get_ssid_ap()
        {
            return ssid_ap;
        }
        String get_pass_ap()
        {
            return pass_ap;
        }
        
        void set_state(String s)
        {
            state=s;
        }
        String get_state()
        {
            return state;
        }
        String get_state_str()
        {
            if(state=="OK")
                return "Actulizado Modelo Correctamente";
            else if(state=="E1")
                return "Error al Descargar Modelo";
            else if(state=="E2")
                return "Error al Salvar Modelo en Memoria";
            else if(state=="E3")
                return "Error al Cargar Modelo";
            else if(state=="E4")
                return "Error al Conectar a Wifi";
            else if(state=="E5")
                return "Error al Salvar datos Wifi";
            else if(state=="E6")
                return "Error en Memoria, Modelo Incorrecto";
            else if(state=="E7")
                return "Error en Descarga, Modelo Incorrecto";
            else
                return "Error";
        }
        String get_ip()
        {
            return WiFi.localIP().toString();
        }
        String get_ip_ap()
        {
            return WiFi.softAPIP().toString();
        }
};