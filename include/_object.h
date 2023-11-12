
class Object
{
    private:
        const unsigned STEP=100;
        unsigned char * data;
        unsigned count;
        unsigned max; 
        void resize()
        {
            max+=STEP;
            unsigned char*new_data=new unsigned char[max];
            for(int i=0;i<count;i++)
                new_data[i]=data[i];
            delete data;
            data=new_data;
        }
    public:
        Object()
        {         
            max=STEP;
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
            
            for(int i=0;i<len;i++)
                append(values[i]);
        }
        void clear()
        {
            delete data;
            count=0;
            max=STEP;
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
        String get_data_str()
        {
            String s;
            for(int i=0;i<count;i++)
                s+=String((char)data[i]);
            return s;
        }
        void print()
        {
            for(int i=0;i<count;i++)
                Serial.print(data[i]);
            Serial.println();
        }
        void print_str()
        {
            String s=get_data_str();
            Serial.print(s);
        }
};
struct _2data
{
    public:
        int _i;
        float _f;
        _2data(int i=-1,float f=-1)
        {
            this->_i=i;
            this->_f=f;
        }
        void print()
        {
            Serial.print("\n[ ");
            Serial.print(_i);
            Serial.print(" , ");
            Serial.print(_f);
            Serial.println(" ]");
        }

};

class _18float
    {
        private:
            float _18[18];
            unsigned count;
        public:
            _18float()
            {
                count=0;
            }
            bool complete()
            {
                return count==18?true :false;
            }
            float* get_18()
            {
                return _18;    
            }
            float get_data(unsigned i)
            {
                if(i>=18)
                    return 0;
                return _18[i];
            }
            void print()
            {
                for(int i=0;i<18;i++)
                    Serial.println(_18[i]);
            }
            // _18float(const _18float&_18)
            // {
            //     for(int i=0;i<18;i++)
            //         this->_18[i]=_18._18[i];
            //     count=18;
            // }
            void add(float data)
            {
                if(count>=18)
                    return;
                _18[count++]=data;
            }
            void reset_count()
            {
                count=0;
            }
            void add(int index,float data)
            {
                if(index<0||index>=18)
                    return;
                _18[index]=data;
            }
    };
