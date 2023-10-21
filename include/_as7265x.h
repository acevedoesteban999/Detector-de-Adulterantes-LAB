#include <Wire.h>

#define I2C_ADDR  0x49

#define STATUS_REG  0x00
#define WRITE_REG  0x01
#define READ_REG  0x02
#define TX_VALID  0x02
#define RX_VALID  0x01

//Register addresses
#define HW_VERSION_HIGH  0x00
#define HW_VERSION_LOW  0x01
#define FW_VERSION_HIGH  0x02
#define FW_VERSION_LOW  0x03

#define CONFIG  0x04
#define INTEGRATION_TIME  0x05
#define DEVICE_TEMP  0x06
#define LED_CONFIG  0x07

//Raw channel registers
#define R_G_A  0x08
#define S_H_B  0x0a
#define T_I_C  0x0c
#define U_J_D  0x0e
#define V_K_E  0x10
#define W_L_F  0x12

//Calibrated channel registers
#define R_G_A_CAL  0x14
#define S_H_B_CAL  0x18
#define T_I_C_CAL  0x1c
#define U_J_D_CAL  0x20
#define V_K_E_CAL  0x24
#define W_L_F_CAL  0x28

#define DEV_SELECT_CONTROL  0x4F

#define COEF_DATA_0 = 0x50
#define COEF_DATA_1  0x51
#define COEF_DATA_2  0x52
#define COEF_DATA_3  0x52
#define COEF_DATA_READ  0x54
#define COEF_DATA_WRITE  0x55

//Settings
#define POLLING_DELAY  0.01*1000
#define NIR  0x00
#define VISIBLE 0x01
#define UV  0x02

#define LED_WHITE  0x00
#define LED_IR  0x01
#define LED_UV  0x02
#define LED_CURRENT_LIMIT_12_5MA  0b00
#define LED_CURRENT_LIMIT_25MA    0b01
#define LED_CURRENT_LIMIT_50MA    0b10
#define LED_CURRENT_LIMIT_100MA   0b11

#define INDICATOR_CURRENT_LIMIT_1MA  0b00
#define INDICATOR_CURRENT_LIMIT_2MA  0b01
#define INDICATOR_CURRENT_LIMIT_4MA  0b10
#define INDICATOR_CURRENT_LIMIT_8MA  0b11

#define GAIN_1X  0b00
#define GAIN_37X  0b01
#define GAIN_16X  0b10
#define GAIN_64X  0b11

#define MEASUREMENT_MODE_4CHAN  0b00
#define MEASUREMENT_MODE_4CHAN_2  0b01
#define MEASUREMENT_MODE_6CHAN_CONTINUOUS  0b10
#define MEASUREMENT_MODE_6CHAN_ONE_SHOT  0b11


class As7265x
{
    
    class AS7265X
    {
        public:
            AS7265X()
            {
                Wire.begin(18,19);
            }
            ~AS7265X()
            {
                Wire.end();
            }

        bool begin()
        {
            if (! this->isConnected())
                return false;
            int value = this->virtualReadRegister(DEV_SELECT_CONTROL);
            if ((value & 0b00110000) == 0)
                return false;
            this->setBulbCurrent(LED_CURRENT_LIMIT_12_5MA, LED_WHITE);
            this->setBulbCurrent(LED_CURRENT_LIMIT_12_5MA, LED_IR);
            this->setBulbCurrent(LED_CURRENT_LIMIT_12_5MA, LED_UV);

            this->disableBulb(LED_WHITE);
            this->disableBulb(LED_IR);
            this->disableBulb(LED_UV);

            this->setIndicatorCurrent(INDICATOR_CURRENT_LIMIT_8MA);
            this->enableIndicator();

            this->setIntegrationCycles(49); //50 * 2.8ms = 140ms.
            this->setGain(GAIN_64X);
            this->setMeasurementMode(MEASUREMENT_MODE_6CHAN_ONE_SHOT);
            this->enableInterrupt();
            return true;
        }
        
        int getDeviceType()
        {
            return this->virtualReadRegister(HW_VERSION_HIGH);
        }
        int getHardwareVersion()
        {
            return this->virtualReadRegister(HW_VERSION_LOW);
        }
        int getMajorFirmwareVersion()
        {
            this->virtualWriteRegister(FW_VERSION_HIGH, 0x01);
            this->virtualWriteRegister(FW_VERSION_LOW, 0x01);

            return this->virtualReadRegister(FW_VERSION_LOW);
        }
        int getPatchFirmwareVersion()
        {
            this->virtualWriteRegister(FW_VERSION_HIGH, 0x02);
            this->virtualWriteRegister(FW_VERSION_LOW, 0x02);

            return this->virtualReadRegister(FW_VERSION_LOW);
        }
        int getBuildFirmwareVersion()
        {
            this->virtualWriteRegister(FW_VERSION_HIGH, 0x03);
            this->virtualWriteRegister(FW_VERSION_LOW, 0x03);

            return this->virtualReadRegister(FW_VERSION_LOW);
        }
        bool isConnected()
        {
            Wire.beginTransmission(I2C_ADDR);
            if (Wire.endTransmission(true) != 0)
                    return false; 
            return true;
        }
        void takeMeasurements()
        {
            this->setMeasurementMode(MEASUREMENT_MODE_6CHAN_ONE_SHOT);
            
            while (! this->dataAvailable())
            {
                delay(POLLING_DELAY);
            }
        }
        void takeMeasurementsWithBulb()
        {
            this->enableBulb(LED_WHITE);
            this->enableBulb(LED_IR);
            this->enableBulb(LED_UV);

            this->takeMeasurements();

            this->disableBulb(LED_WHITE);
            this->disableBulb(LED_IR);
            this->disableBulb(LED_UV);
        }
        //Get the various color readings
        int getG()
        {
            return this->getChannel(R_G_A, VISIBLE);
        }
        int getH()
        {
            return this->getChannel(S_H_B, VISIBLE);
        }
        int getI()
        {
            return this->getChannel(T_I_C, VISIBLE);
        }
        int getJ()
        {
            return this->getChannel(U_J_D, VISIBLE);
        }
        int getK()
        {
            return this->getChannel(V_K_E, VISIBLE);
        }
        int getL()
        {
            return this->getChannel(W_L_F, VISIBLE);
        }
        //Get the various NIR readings
        int getR()
        {
            return this->getChannel(R_G_A, NIR);
        }
        int getS()
        {
            return this->getChannel(S_H_B, NIR);
        }
        int getT()
        {
            return this->getChannel(T_I_C, NIR);
        }
        int getU()
        {
            return this->getChannel(U_J_D, NIR);
        }
        int getV()
        {
            return this->getChannel(V_K_E, NIR);
        }
        int getW()
        {
            return this->getChannel(W_L_F, NIR);
        }
        //Get the various UV readings
        int getA()
        {
            return this->getChannel(R_G_A, UV);
        }
        int getB()
        {
            return this->getChannel(S_H_B, UV);
        }
        int getC()
        {
            return this->getChannel(T_I_C, UV);
        }
        int getD()
        {
            return this->getChannel(U_J_D, UV);
        }
        int getE()
        {
            return this->getChannel(V_K_E, UV);
        }
        int getF()
        {
            return this->getChannel(W_L_F, UV);
        }
        int getChannel(int channelRegister, int device)
        {
            this->selectDevice(device);
            int colorData = this->virtualReadRegister(channelRegister) << 8;
            colorData = colorData | this->virtualReadRegister(channelRegister + 1);
            return colorData;
        }
        _18float getCalibrateds()
        {
            _18float _18;
            _18.add(getCalibratedA());
            _18.add(getCalibratedB());
            _18.add(getCalibratedC());
            _18.add(getCalibratedD());
            _18.add(getCalibratedE());
            _18.add(getCalibratedF());
            _18.add(getCalibratedG());
            _18.add(getCalibratedH());
            _18.add(getCalibratedI());
            _18.add(getCalibratedJ());
            _18.add(getCalibratedK());
            _18.add(getCalibratedL());
            _18.add(getCalibratedR());
            _18.add(getCalibratedS());
            _18.add(getCalibratedT());
            _18.add(getCalibratedU());
            _18.add(getCalibratedV());
            _18.add(getCalibratedW());
            return _18;
        }
        //Returns the various calibration data
        float getCalibratedA()
        {
            return this->getCalibratedValue(R_G_A_CAL, UV);
        }
        float getCalibratedB()
        {
            return this->getCalibratedValue(S_H_B_CAL, UV);
        }
        float getCalibratedC()
        {
            return this->getCalibratedValue(T_I_C_CAL, UV);
        }
        float getCalibratedD()
        {
            return this->getCalibratedValue(U_J_D_CAL, UV);
        }
        float getCalibratedE()
        {
            return this->getCalibratedValue(V_K_E_CAL, UV);
        }
        float getCalibratedF()
        {
            return this->getCalibratedValue(W_L_F_CAL, UV);
        }
        //Returns the various calibration data
        float getCalibratedG()
        {
            return this->getCalibratedValue(R_G_A_CAL, VISIBLE);
        }
        float getCalibratedH()
        {
            return this->getCalibratedValue(S_H_B_CAL, VISIBLE);
        }
        float getCalibratedI()
        {
            return this->getCalibratedValue(T_I_C_CAL, VISIBLE);
        }
        float getCalibratedJ()
        {
            return this->getCalibratedValue(U_J_D_CAL, VISIBLE);
        }
        float getCalibratedK()
        {
            return this->getCalibratedValue(V_K_E_CAL, VISIBLE);
        }
        float getCalibratedL()
        {
            return this->getCalibratedValue(W_L_F_CAL, VISIBLE);
        }
        //Returns the various calibration data
        float getCalibratedR()
        {
            return this->getCalibratedValue(R_G_A_CAL, NIR);
        }
        float getCalibratedS()
        {
            return this->getCalibratedValue(S_H_B_CAL, NIR);
        }
        float getCalibratedT()
        {
            return this->getCalibratedValue(T_I_C_CAL, NIR);
        }
        float getCalibratedU()
        {
            return this->getCalibratedValue(U_J_D_CAL, NIR);
        }
        float getCalibratedV()
        {
            return this->getCalibratedValue(V_K_E_CAL, NIR);
        }
        float getCalibratedW()
        {
            return this->getCalibratedValue(W_L_F_CAL, NIR);
        }
        //Given an address, read four bytes and return the floating point calibrated value
        float getCalibratedValue(int calAddress, int device)
        {
            
            this->selectDevice(device);

            int b0 = this->virtualReadRegister(calAddress + 0);
            int b1 = this->virtualReadRegister(calAddress + 1);
            int b2 = this->virtualReadRegister(calAddress + 2);
            int b3 = this->virtualReadRegister(calAddress + 3);
            union as7265x_union
            {
                char _bytes[4];
                float _float;
                as7265x_union(int byte0,int byte1,int byte2,int byte3)
                {
                    this->_bytes[3]=byte0;
                    this->_bytes[2]=byte1;
                    this->_bytes[1]=byte2;
                    this->_bytes[0]=byte3;
                }
            };
            as7265x_union a_u(b0,b1,b2,b3);
            float calBytes=a_u._float;
            return calBytes;
        }
        // #Given 4 bytes returns the floating point value
        void setMeasurementMode(int mode)
        {
            mode = 0b11 ? mode > 0b11 : mode;

            int value = this->virtualReadRegister(CONFIG);
            value &= 0b11110011;
            value |= (mode << 2);
            this->virtualWriteRegister(CONFIG, value);
        }
        void setGain(int gain)
        {
            gain = 0b11 ? gain > 0b11 : gain;

            int value = this->virtualReadRegister(CONFIG);
            value &= 0b11001111;
            value |= (gain << 4);
            this->virtualWriteRegister(CONFIG, value);
        }
        void setIntegrationCycles(int cycleValue)
        {
            this->virtualWriteRegister(INTEGRATION_TIME, cycleValue);
        }
        void enableInterrupt()
        {
            int value = this->virtualReadRegister(CONFIG);
            value |= 0b01000000;
            this->virtualWriteRegister(CONFIG, value);
        }
        void disableInterrupt()
        {
            int value = this->virtualReadRegister(CONFIG);
            value &= 0b10111111;
            this->virtualWriteRegister(CONFIG, value);
        }
        int dataAvailable()
        {
            int value = this->virtualReadRegister(CONFIG);
            return value & 0x02;
        }
        void enableBulb(int device)
        {
            this->selectDevice(device);

            int value = this->virtualReadRegister(LED_CONFIG);
            value |= 0b00001000;
            this->virtualWriteRegister(LED_CONFIG, value);
        }
        void disableBulb(int device)
        {
            this->selectDevice(device);

            int value = this->virtualReadRegister(LED_CONFIG);
            value &= 0b11110111;
            this->virtualWriteRegister(LED_CONFIG, value);
        }
        void setBulbCurrent(int current, int device)
        {
            this->selectDevice(device);
            current = 0b11 ? current > 0b11 : current;
            int value = this->virtualReadRegister(LED_CONFIG);
            value &= 0b11001111;
            value |= (current << 4);
            this->virtualWriteRegister(LED_CONFIG, value);
        }
        void selectDevice(int device)
        {
            this->virtualWriteRegister(DEV_SELECT_CONTROL, device);
        }
        void enableIndicator()
        {
            int value = this->virtualReadRegister(LED_CONFIG);
            value |= 0b00000001;

            this->selectDevice(NIR);
            this->virtualWriteRegister(LED_CONFIG, value);
        }
        void disableIndicator()
        {
            int value = this->virtualReadRegister(LED_CONFIG);
            value &= 0b11111110;

            this->selectDevice(NIR);
            this->virtualWriteRegister(LED_CONFIG, value);
        }
        void setIndicatorCurrent(int current)
        {
            current = 0b11 ? current > 0b11 : current;
            int value = this->virtualReadRegister(LED_CONFIG);
            value &= 0b11111001;
            value |= (current << 1);

            this->selectDevice(NIR);
            this->virtualWriteRegister(LED_CONFIG, value);
        }
        int getTemperature(int deviceNumber)
        {
            this->selectDevice(deviceNumber);
            return this->virtualReadRegister(DEVICE_TEMP);
        }
        float getTemperatureAverage()
        {
            float average = 0;
            for(int x=0;x<3;x++)
            {
                average += this->getTemperature(x);
            }
                
            return average/3;
        }
        void softReset()
        {
            int value = this->virtualReadRegister(CONFIG);
            value |= 0x80;
            this->virtualWriteRegister(CONFIG, value);
        }
        int virtualReadRegister(int virtualAddr)
        {
            
            int status = this->readRegister(STATUS_REG);
            if ((status & RX_VALID) != 0)
                this->readRegister(READ_REG);
            
            while(1)
            {
                status = this->readRegister(STATUS_REG);
                if ((status & TX_VALID) == 0)
                    break;
                delay(POLLING_DELAY);
            }
            
            this->writeRegister(WRITE_REG, virtualAddr);
            
            while(1)
            {
                status = this->readRegister(STATUS_REG);
                if ((status & RX_VALID) != 0)
                    break;
                delay(POLLING_DELAY);
            }
            
            return this->readRegister(READ_REG);
            
        }
        void virtualWriteRegister(int virtualAddr, int dataToWrite)
        {
            
            while(1)
            {
                int status = this->readRegister(STATUS_REG);
                if ((status & TX_VALID) == 0)
                    break;
                delay(POLLING_DELAY);
            }
            
            this->writeRegister(WRITE_REG, virtualAddr | 0x80);
            
            while(1)
            {
                int status = this->readRegister(STATUS_REG);
                if ((status & TX_VALID) == 0)
                    break;
                delay(POLLING_DELAY);
            }
            
            this->writeRegister(WRITE_REG, dataToWrite);
            
        }
        int readRegister(int addr)
        {
            Wire.beginTransmission(I2C_ADDR);
            Wire.write(addr);
            Wire.endTransmission();
            Wire.requestFrom(I2C_ADDR, 1);
            return Wire.read();
            
        }     
        void writeRegister(int addr, int val)
        {
            Wire.beginTransmission(I2C_ADDR);
            Wire.write(addr);
            Wire.write(val);
            Wire.endTransmission();
        }
    };
    private:
        bool active;
        AS7265X as7265x;
    public:
        As7265x()
        {
            active=false;
        }
        ~As7265x()
        {}
        bool start()
        {  
            active=as7265x.begin();
            return active;  
        }
        bool get_active()
        {
            return active;
        }
        _18float get_datas()
        {
            if(!active)
                return _18float();
            as7265x.takeMeasurementsWithBulb();
            return as7265x.getCalibrateds();
        }
};
