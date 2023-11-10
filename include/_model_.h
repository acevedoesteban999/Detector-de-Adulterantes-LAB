#define NUMBER_OF_INPUTS 18
#define NUMBER_OF_OUTPUTS 5
#define TENSOR_ARENA_SIZE 10*1024
#include <EloquentTinyML.h>
#ifndef OBJ_LIB
    #define OBJ_LIB
    #include "_object.h"
#endif
class Model
{
	private:
        bool active;
		String model_name;
		_18float data;
		Eloquent::TinyML::TfLite<NUMBER_OF_INPUTS, NUMBER_OF_OUTPUTS, TENSOR_ARENA_SIZE> tf;
	public:
		Model()
		{
			active=false;
			model_name="------";
		}
		~Model()
		{}
		bool get_active()
		{
			return active;
		}
		void clear()
		{

		}
		bool start(Object&obj)
		{
			active=tf.begin(obj.get_data());
			return active;
		}
		void load_name(String name)
		{
			model_name=name;
		}
		String get_name()
		{
			return model_name;
		}
		String get_list_data()
		{
			String s="";
			for(int i =0;i<18;i++)
				s+=String(data.get_data(i))+ (i!=17?",":"");
			return s;
		}
		void set_datas(_18float data)
		{
			this->data=data;
		}
		_18float get_data()
		{
			return data;
		}
		_2data predict()
		{
			if(active==false)
				return _2data();
			
			// float y_pred[NUMBER_OF_OUTPUTS];
			// float input[18] = {1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0};
			// float output[5];
			// tf.predict(input, y_pred);
			float x_test[NUMBER_OF_INPUTS];
			for(int i=0;i<NUMBER_OF_INPUTS;i++)
				x_test[i]=data.get_data(i);
    		for(int i=0;i<NUMBER_OF_INPUTS;i++)
				Serial.println(x_test[i]);
    		
			float y_pred[NUMBER_OF_OUTPUTS];
			
			uint32_t start = micros();

			tf.predict(x_test, y_pred);

			uint32_t timeit = micros() - start;
			Serial.print("Predicted proba are: ");
			for (int i = 0; i < NUMBER_OF_OUTPUTS; i++) {
				Serial.print(y_pred[i]);
				Serial.print(i == NUMBER_OF_OUTPUTS ? '\n' : ',');
			}
			
			// let's print the "most probable" class
			// you can either use probaToClass() if you also want to use all the probabilities
			Serial.print("\nPredicted class is: ");
			Serial.println(tf.probaToClass(y_pred));
			// or you can skip the predict() method and call directly predictClass()
			//Serial.print("Sanity check: ");
			//Serial.println(tf.predictClass(data.get_18()));
			return _2data(tf.probaToClass(y_pred),y_pred[tf.probaToClass(y_pred)]*100);
		}
};