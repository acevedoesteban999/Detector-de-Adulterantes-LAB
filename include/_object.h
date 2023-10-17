class Object
{
    private:
        unsigned char * data;
        unsigned count;
        unsigned max; 
        void resize()
        {
            max+=1000;
            unsigned char*new_data=new unsigned char[max];
            for(int i=0;i<count;i++)
                new_data[i]=data[i];
            delete data;
            data=new_data;
        }
    public:
        Object()
        {         
            max=1000;
            count=0;
            data=new unsigned char[max];
        }
        ~Object()
        {
            delete data;
        }
        
        void append(unsigned char value)
        {
            if (count>=max)
            {
                resize();
                return append(value);
            } 
            data[count++]=value;
        }
        void append(unsigned char*values,int len)
        {
            if(count+len>=max)
            {
                resize();
                return append(values,len);
            } 
            for(int i=0;i<len;i++)
            {
                data[count++]=values[i];
            }
        }
        void clear()
        {
            delete data;
            count=0;
            max=1000;
            data=new unsigned char[max];
        }
        int get_count()
        {
            return count;
        }
        unsigned char* get_data()
        {
            return data;
        }
        void print()
        {
            for(int i=0;i<count;i++)
                Serial.print(data[i]);
        }
};