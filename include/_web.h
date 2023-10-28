#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>
//#include "_htmls.h"
#include <esp_system.h>
#ifndef _LIB
    #define _LIB
    #include "_wifi.h"
    #include "_download.h"
    #include"_as7265x.h"
    #include "_model_.h"
    #include "_spiffs.h"
#endif
Wifi*_wifi;
Model*_model;
class Web
{
    private:
        AsyncWebServer*server;
        bool flag_download;
        bool flag_predict;
        Wifi*wifi;
        Download*download;
        As7265x*as7265x;
        Model*model;
        Spiffs*spiffs;
    public:
        
        Web()
        {
            server=new AsyncWebServer(80);
            flag_download=false;
            flag_predict=false;
        }
        ~Web()
        {
            delete server;
        }
        void init(Download*download,As7265x*as7265x,Model*model,Spiffs*spiffs,Wifi*wifi)
        {
            this->wifi=wifi;
            _wifi=wifi;
            _model=model;
            this->download=download;
            this->as7265x=as7265x;
            this->model=model;
            this->spiffs=spiffs;
        }
        static String processor(const String& var)
        {
            if(var == "HELLO_FROM_TEMPLATE")
                return F("Hello world!");
            else if(var == "MODEL_NAME")
                return F(_model->get_name().c_str());
            else if(var == "DISPLAY")
            {
                if(_wifi->get_download())
                    return F("block");
                else
                    return F("none");
            }
            else if(var == "COLOR")
            {
                if(_wifi->get_state()=="OK")
                    return F("green");
                else
                    return F("red");
            }
            else if(var == "H5_DATA")
            {
                if(_wifi->get_download())
                    return F(_wifi->get_state_str().c_str());
            }
            else if(var == "SSID")
            {
                return F(_wifi->get_ssid().c_str());
            }
            else if(var == "PASS")
                return F(_wifi->get_pass().c_str());
            return String();
        }
        static void notFound(AsyncWebServerRequest *request) {
            request->send(404, "text/plain", "Not found");
        }
        void set_flag_downalod(String ssid,String pass,String model_name)
        {
            flag_download=true;
            wifi->set_ssid_pass(ssid,pass);
            wifi->set_download();
            model->load_name(model_name);
            
        }
        bool get_flag_download()
        {
            return flag_download;
        }
        void load_spiffs_params()
        {
            Object obj,obj1;
            if(spiffs->load_data("/model_name",obj))
                model->load_name(obj.get_data_str());
            if(spiffs->load_data("/wifi_ssid",obj)&&spiffs->load_data("/wifi_pass",obj1))
                wifi->set_ssid_pass(obj.get_data_str(),obj1.get_data_str());
        }
        void _download()
        {
            if(flag_download)
            {
                String state;
                if(wifi->connect_wifi(wifi->get_ssid(),wifi->get_pass()))
                {   
                    if(spiffs->save_data("/wifi_ssid",wifi->get_ssid()) && spiffs->save_data("/wifi_pass",wifi->get_pass()))
                    {    
                        String _url="https://raw.githubusercontent.com/Esteban1914/files/tesis/";
                        String model_name=model->get_name();
                        _url+=model_name;
                        Object obj;
                        if(download->download(_url,obj))
                        {
                            spiffs->save_data("/new_model",obj);
                            spiffs->save_data("/new_model_name",model_name);
                            esp_restart();
                        }
                        else
                            state="E1";
                    }
                    else
                        state="E5";
                }
                else
                    state="E4";
                wifi->set_state(state);
                load_spiffs_params();
                wifi->create_ap();
                flag_download=false;
            }
            
        }
        bool start()
        {
            // server->on("/", HTTP_GET, [](AsyncWebServerRequest *request)
            // {
            //     request->send_P(200, "text/html", index_html, processor);
            // });
            // server->on("/download", HTTP_GET, [](AsyncWebServerRequest *request)
            // {
            //     request->send_P(200, "text/html", download_html, processor);
            //     _wifi->reset_download();
            // });
            // server->on("/styles.css", HTTP_GET, [](AsyncWebServerRequest *request)
            // {
            //     request->send_P(200, "text/css", styles_css);
            // });
            server->on("/post/download", HTTP_POST, [&,this](AsyncWebServerRequest *request)
            {
                if(request->hasParam("action", true) && request->getParam("action", true)->value()=="download")
                {
                    if(request->hasParam("model", true)&&request->hasParam("ssid", true)&&request->hasParam("pass", true))
                    {
                        AsyncWebServerResponse *response = request->beginResponse(200, "text/plain", "Iniciando Descarga...<br>Es necesario volver a conectarse al dsipositivo y refrescar la página");
                        request->send(response);             
                        this->set_flag_downalod(request->getParam("ssid",true)->value(),request->getParam("pass",true)->value(),request->getParam("model",true)->value());
                        return;    
                    }   
                }
                AsyncWebServerResponse *response = request->beginResponse(200, "text/plain", "<div style='color: red;'>Error<div>");
                request->send(response);
                
            });
            // server->on("/predict", HTTP_GET, [](AsyncWebServerRequest *request)
            // {
            //     request->send_P(200, "text/html", predict_html, processor);
            // });
            server->on("/", HTTP_GET, [](AsyncWebServerRequest *request){
                request->send(SPIFFS, "/static/main.html", "text/html",false,processor);
            });
            server->on("/download", HTTP_GET, [](AsyncWebServerRequest *request){
                request->send(SPIFFS, "/static/download.html", "text/html",false,processor);
                _wifi->reset_download();
            });
            server->on("/predict", HTTP_GET, [](AsyncWebServerRequest *request){
                request->send(SPIFFS, "/static/predict.html", "text/html",false,processor);
            });
            server->on("/post/predict", HTTP_POST, [&,this](AsyncWebServerRequest *request)
            {
                String state="Error0";
                String resp="";
                if(request->hasParam("action", true) && request->getParam("action", true)->value()=="predict")
                {
                    if(this->model->get_active())
                    {
                        if (this->as7265x->get_active())
                        {
                            _18float data=this->as7265x->get_datas();
                            if(data.complete())
                            {
                                resp=String(this->model->predict(data));
                                state="OK";
                            }
                            else
                                state="E2";
                        }
                        else
                            state="E1";
                    }
                    else
                        state="E3";    
                }
                String _r="state="+state+"&predict_data="+resp;
                AsyncWebServerResponse *response = request->beginResponse(200, "text/plain", _r);
                request->send(response);
                
            });
            server->serveStatic("/static", SPIFFS, "/static");
            server->onNotFound(notFound);
            server->begin();
            return true;
        }
};