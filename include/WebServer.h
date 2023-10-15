#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>
class WebServer
{
    private:
        AsyncWebServer * server;
    public:
        WebServer()
        {
            this->server=new AsyncWebServer(80);
            
            this->server->on("/hello_server", HTTP_GET, [](AsyncWebServerRequest *request)
            {
                request->send(200, "text/plain", "Hello AsyncWebServer!");
            });
            this->server->begin();
        }
        ~WebServer()
        {
            delete this->server;
        }

};