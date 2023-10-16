#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>

class Web
{
    private:
        AsyncWebServer*server;
    public:
        Web()
        {
            server=new AsyncWebServer(80);
        }
        ~Web()
        {
            delete server;
        }
        bool start()
        {
            // server->on("/a", HTTP_GET, [](AsyncWebServerRequest *request){
            //     request->send(SPIFFS, "/index.html");
            // });
            // server->on("/hi", HTTP_GET, [](AsyncWebServerRequest *request)
            // {
            //     request->send(200, "text/plain", "Hello AsyncWebServer!");
            // });
            server->begin();
            return true;
        }
};