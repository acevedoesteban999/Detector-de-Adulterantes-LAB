#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>
class ESPAsyncWebServer
{
    private:
        AsyncWebServer server(80);
    public:
    ESPAsyncWebServer()
    {
        server.on("/hello_server", HTTP_GET, [](AsyncWebServerRequest *request)
        {
        request->send(200, "text/plain", "Hello AsyncWebServer!");
        });
        server.begin()
    }
    ~ESPAsyncWebServer(){}
};