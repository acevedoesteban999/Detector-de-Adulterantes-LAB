#pragma once
#include "HTTPClient.h"
#include "_object.h"
class Download
{
    private:
        HTTPClient http;
    public:
    Download()
    {}
    ~Download()
    {}
    bool download(String url,Object&obj)
    {
        http.begin(url);
        int httpCode = http.GET();
        int len = http.getSize();
        if (httpCode!=200)
            return false;
        WiFiClient * stream = http.getStreamPtr();
        obj.clear();
        while(http.connected() && (len > 0 || len == -1)) 
        {
            size_t size = stream->available();
            
            if(size) 
            {
                uint8_t buff[1024] = { 0 };
                int c = stream->readBytes(buff, ((size > sizeof(buff)) ? sizeof(buff) : size));
                obj.append(buff,c);
                if(len > 0) 
                {
                    len -= c;
                }
            }
            delay(1);
        }
    return true;
    }
};
