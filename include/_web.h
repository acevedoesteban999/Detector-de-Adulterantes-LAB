#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>
//#include "_htmls.h"
#include <esp_system.h>
#ifndef _LIB
    #define _LIB
    #include "_wifi.h"
    #include "_download.h"
    #include"_as7265x.h"
#endif
#ifndef SPIF_LIB
    #define SPIF_LIB
    #include "_spiffs.h"
#endif
#ifndef MODEL_LIB
    #define MODEL_LIB
    #include "_model.h"
#endif
#ifndef MUTEX_LIB
    #define MUTEX_LIB
    #include "mutex"
#endif
Wifi*_wifi;
Download*_download;
As7265x*_as7265x;
Model*_model;
Spiffs*_spiffs;
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
        void init(Download*download,As7265x*as7265x,Model*model,Spiffs*spiffs,Wifi*wifi)
        {
            _wifi=wifi;
            _model=model;
            _as7265x=as7265x;
            _download=download;
            _spiffs=spiffs;
        }
        static String processor(const String& var)
        {
            if(var == "MODEL_NAME")
                return F(_model->get_name().c_str());
            else if(var=="DATA_ICON")
            {
                if(_wifi->get_update())
                    if(_wifi->get_state_str()=="OK")
                        return F(R"rawliteral(
                            <span class="badge bg-success rounded-circle">
                                <svg width="100" height="100" fill="currentColor" class="bi bi-check2-all" viewBox="0 0 16 16">
                                    <path d="M12.354 4.354a.5.5 0 0 0-.708-.708L5 10.293 1.854 7.146a.5.5 0 1 0-.708.708l3.5 3.5a.5.5 0 0 0 .708 0l7-7zm-4.208 7-.896-.897.707-.707.543.543 6.646-6.647a.5.5 0 0 1 .708.708l-7 7a.5.5 0 0 1-.708 0z"/>
                                    <path d="m5.354 7.146.896.897-.707.707-.897-.896a.5.5 0 1 1 .708-.708z"/>
                                </svg>
                            </span>
                        )rawliteral");
                    else
                        return F(R"rawliteral(
                            <span class="badge bg-danger rounded-circle">
                                <svg width="100" height="100" fill="currentColor" class="bi bi-exclamation-circle-fill" viewBox="0 0 16 16">
                                    <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8 4a.905.905 0 0 0-.9.995l.35 3.507a.552.552 0 0 0 1.1 0l.35-3.507A.905.905 0 0 0 8 4zm.002 6a1 1 0 1 0 0 2 1 1 0 0 0 0-2z"/>
                                </svg>
                            </span>
                        )rawliteral");
            }

            else if(var=="SENSOR_ICON")
            {
                if(_as7265x->get_active())
                    return F(R"rawliteral(
                        <a href="?rs=1" class="btn btn-success">
                            <svg width="25" height="25" fill="currentColor" class="bi bi-check-circle-fill" viewBox="0 0 16 16">
                                <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>
                            </svg>
                        </a>
                    )rawliteral");
                return F(R"rawliteral(
                        <a href="?rs=1" class="btn btn-danger">
                            <svg width="25" height="25" fill="currentColor" class="bi bi-x-circle-fill" viewBox="0 0 16 16">
                                <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293 5.354 4.646z"/>
                            </svg>
                        </a>
                    )rawliteral");
            }
            else if(var == "MESSAGE_BOOL")
            {
                return F(_wifi->get_update()==true?"1":"0");
            }
            else if(var == "H5_DATA")
            {
                if(_wifi->get_update())
                    return F(_wifi->get_state_str().c_str());
            }
            else if(var == "SSID")
            {
                return F(_wifi->get_ssid().c_str());
            }
            else if(var == "PASS")
                return F(_wifi->get_pass().c_str());
            else if(var == "SSID_AP")
            {
                return F(_wifi->get_ssid_ap().c_str());
            }
            else if(var == "PASS_AP")
                return F(_wifi->get_pass_ap().c_str());
            return String();
        }
        static void notFound(AsyncWebServerRequest *request) {
            request->send(404, "text/plain", "Not found");
        }
        
        void load_spiffs_params()
        {
            Object obj,obj1;
            if(_spiffs->load_data("/model_name",obj))
                _model->load_name(obj.get_data_str());
            if(_spiffs->load_data("/wifi_ssid",obj)&&_spiffs->load_data("/wifi_pass",obj1))
                _wifi->set_ssid_pass(obj.get_data_str(),obj1.get_data_str());
        }
        void _download_model()
        {
            //if(_wifi->get_flag_download())
            //{
            String state;
            if(_wifi->connect_wifi(_wifi->get_ssid(),_wifi->get_pass()))
            {
                if(_spiffs->save_data("/wifi_ssid",_wifi->get_ssid()) && _spiffs->save_data("/wifi_pass",_wifi->get_pass()))
                {
                    String _url="https://raw.githubusercontent.com/Esteban1914/files/tesis/";
                    String model_name=_model->get_name();
                    _url+=model_name;
                    Object obj;
                    _spiffs->save_data("/error_model","1");
                    if(_download->download(_url,obj))
                    {
                        _spiffs->save_data("/new_model",obj);
                        _spiffs->save_data("/new_model_name",model_name);
                        _spiffs->delete_data("/error_model");
                        esp_restart();
                    }
                    else
                        state="E1";
                    _spiffs->delete_data("/error_model");
                }
                else
                    state="E5";
            }
            else
                state="E4";
            _wifi->set_state(state);
            load_spiffs_params();
            _wifi->create_ap();
            //_wifi->reset_flag_download();
            //}

        }
        bool start()
        {
            server->on("/", HTTP_GET, [](AsyncWebServerRequest *request){
                if(request->hasParam("rs"))
                    _as7265x->start();
                request->send(SPIFFS, "/static/main.html", "text/html",false,processor);
            });
            server->on("/post/download", HTTP_POST, [this](AsyncWebServerRequest *request)
            {
                
                if(request->hasParam("action", true) && request->getParam("action", true)->value()=="download")
                {
                    if(request->hasParam("model", true)&&request->hasParam("ssid", true)&&request->hasParam("pass", true))
                    {
                        AsyncWebServerResponse *response = request->beginResponse(200, "text/plain", "OK");
                        request->send(response);
                        _wifi->set_flag_downalod(request->getParam("ssid",true)->value(),request->getParam("pass",true)->value(),request->getParam("model",true)->value());
                        return;
                    }
                }
                AsyncWebServerResponse *response = request->beginResponse(200, "text/plain", "<div style='color: red;'>Error<div>");
                request->send(response);
                
            });
            server->on("/post/predict", HTTP_POST, [](AsyncWebServerRequest *request)
            {
                String state="Error0";
                String resp="";
                String list_data="";
                _2data _2d;
                if(request->hasParam("action", true) && request->getParam("action", true)->value()=="predict")
                {
                    if(_model->get_active())
                    {
                        if (_as7265x->get_active())
                        {
                            _18float data=_as7265x->get_datas();
                            if(data.complete())
                            {
                                _model->set_datas(data);
                                //_2d=_model->predict();
                                list_data=_model->get_list_data();
                                _wifi->set_flag_predict();
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
                String _r="state="+state+"&list_data="+list_data;//"state="+state+"&predict_class="+String(_2d._i)+"&predict_data="+String(_2d._f)+"&list_data="+list_data;
                AsyncWebServerResponse *response = request->beginResponse(200, "text/plain", _r);
                request->send(response);
                
            });
            server->on("/post/config", HTTP_POST, [](AsyncWebServerRequest *request)
            {
                
                if(request->hasParam("action", true) && request->getParam("action", true)->value()=="config")
                {
                    if(request->hasParam("ssid", true)&&request->hasParam("pass", true))
                    {
                        AsyncWebServerResponse *response = request->beginResponse(200, "text/plain", " ");
                        request->send(response);
                        _spiffs->save_data("/ap_ssid",request->getParam("ssid",true)->value());
                        _spiffs->save_data("/ap_pass",request->getParam("pass",true)->value());
                        _wifi->create_ap();
                    }
                }
                

            });
            server->on("/post/reset_update", HTTP_POST, [](AsyncWebServerRequest *request)
            {
                
                _wifi->reset_update();
                
            });
            server->serveStatic("/", SPIFFS, "/static").setCacheControl("max-age=600");
            server->onNotFound(notFound);
            server->begin();
            return true;
        }
        void start_data()
        {
            server=new AsyncWebServer(80);
            start();
        }
        void clear_data()
        {
            server->reset();
            server->end();
            delete server;
        }
};