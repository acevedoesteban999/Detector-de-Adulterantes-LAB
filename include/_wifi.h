#include <WiFi.h>
#include <ESPmDNS.h>


class Wifi
{
    private:
        bool active;
        bool download;
        String state;
        String ssid,pass;
    public:
        Wifi()
        {
            active=false;
            download=false;
        }
        ~Wifi()
        {}
        bool create_ap(String ssid="Esp32_Tesis_EAS",String pass="Esp32Password_EAS",String hostname="esp32.dev",IPAddress ip=IPAddress(192, 168, 1, 1),IPAddress gateway=IPAddress(192, 168, 1, 1),IPAddress subnet=IPAddress(255, 255, 0, 0),IPAddress primaryDNS=IPAddress(192, 168, 1, 1),IPAddress secondaryDNS=IPAddress(0,0, 0, 0))
        { 
            WiFi.disconnect();
            WiFi.mode(WIFI_AP);
            // if (!WiFi.config(ip, gateway, subnet,primaryDNS,secondaryDNS)) 
            //     return false;
            
            WiFi.softAP(ssid, pass);
            //if (!MDNS.begin(hostname))
            //   return false;
            //WiFi.setHostname(hostname.c_str());
            return true;
        }
        void set_download()
        {
            download=true;
        }
        void reset_download()
        {
            download=false;
        }
        bool get_download()
        {
            return download;
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
            else if(state=="Error1")
                return "Error al Descargar Modelo";
            else if(state=="Error2")
                return "Error al Salvar Modelo en Memoria";
            else if(state=="Error3")
                return "Error al Cargar Modelo";
            else if(state=="Error4")
                return "Error al Conectar a Wifi";
            else if(state=="Error5")
                return "Error al Salvar datos Wifi";
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