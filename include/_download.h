#include "HTTPClient.h"
class Download_Model
{
    private:
        HTTPClient http;
    public:
    Download_Model()
    {}
    ~Download_Model()
    {}
    bool download(String url)
    {
        http.begin(url);
        int httpCode = http.GET();
        int len = http.getSize();
        WiFiClient * stream = http.getStreamPtr();
        while(http.connected() && (len > 0 || len == -1)) 
        {
            size_t size = stream->available();
            
            if(size) 
            {
                uint8_t buff[128] = { 0 };
                int c = stream->readBytes(buff, ((size > sizeof(buff)) ? sizeof(buff) : size));
                
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
