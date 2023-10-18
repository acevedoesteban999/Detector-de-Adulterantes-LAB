#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>
#include "_htmls.h"
#ifndef _LIB
    #define _LIB
    #include "_wifi.h"
    #include "_download.h"
    #include"_as7265x.h"
    #include "_model_.h"
    #include "_spiffs.h"
#endif
class Web
{
    private:
        AsyncWebServer*server;

    public:
        Wifi*wifi;
        Download*download;
        As7265x*as7265x;
        Model*model;
        Spiffs*spiffs;
        Web()
        {
            server=new AsyncWebServer(80);
        }
        ~Web()
        {
            delete server;
        }
        void init(Download*download,As7265x*as7265x,Model*model,Spiffs*spiffs,Wifi*wifi)
        {
            this->wifi=wifi;
            this->download=download;
            this->as7265x=as7265x;
            this->model=model;
            this->spiffs=spiffs;
        }
        static String processor(const String& var)
        {
            if(var == "HELLO_FROM_TEMPLATE")
                return F("Hello world!");
            return String();
        }
        static void notFound(AsyncWebServerRequest *request) {
            request->send(404, "text/plain", "Not found");
        }
        bool start()
        {
            server->on("/", HTTP_GET, [](AsyncWebServerRequest *request)
            {
                request->send_P(200, "text/html", index_html, processor);
            });
            server->on("/download", HTTP_GET, [](AsyncWebServerRequest *request)
            {
                request->send_P(200, "text/html", download_html, processor);
            });
            server->on("/post/download", HTTP_POST, [&,this](AsyncWebServerRequest *request)
            {
                String str="Error0";
                if(request->hasParam("action", true) && request->getParam("action", true)->value()=="download")
                {                 
                    if(request->hasParam("model", true)&&request->hasParam("ssid", true)&&request->hasParam("pass", true))
                    {
                        String _url="https://raw.githubusercontent.com/Esteban1914/files/tesis/";
                        String model_name=request->getParam("model",true)->value();
                        _url+=model_name;
                        _url+=".edbm";
                        Object obj;
                        if(this->download->download(_url,obj))
                        {
                            if(this->spiffs->save_data("/model",obj) && this->spiffs->save_data("/model_name",model_name))
                                if(this->model->start(obj))
                                    str="OK";
                                else
                                    str="Error3";
                            else
                                str="Error2";
                            
                        }
                        else
                            str="Error1";
                    }
                }
                
                AsyncWebServerResponse *response = request->beginResponse(200, "text/plain", str);
                request->send(response);
                
            });
            server->on("/predict", HTTP_GET, [](AsyncWebServerRequest *request)
            {
                request->send_P(200, "text/html", predict_html, processor);
            });
            
            server->on("/post/predict", HTTP_POST, [&,this](AsyncWebServerRequest *request)
            {
                String str="Error0";
                if(request->hasParam("action", true) && request->getParam("action", true)->value()=="predict")
                {
                    str="OK";
                }
                
                AsyncWebServerResponse *response = request->beginResponse(200, "text/plain", str);
                request->send(response);
                
            });
            server->onNotFound(notFound);
            server->begin();
            return true;
        }
};