#pragma once
#define NUMBER_OF_INPUTS 18
#define NUMBER_OF_OUTPUTS 5
#define TENSOR_ARENA_SIZE 3*1024
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
		Eloquent::TinyML::TfLite<NUMBER_OF_INPUTS, NUMBER_OF_OUTPUTS, TENSOR_ARENA_SIZE> tf;
	public:
		Model()
		{
			active=false;
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
		uint8_t predict(_18float datas)
		{
			datas.print();
			if(active==false)
				return 0;
			float x_test[NUMBER_OF_INPUTS];
			for(int i=0;i<NUMBER_OF_INPUTS;i++)
				x_test[i]=datas.get_data(i);
    		// // the output vector for the model predictions
    
			float y_pred[NUMBER_OF_OUTPUTS];
			// // the actual class of the sample
			// float y_test = 0.127;

			// // let's see how long it takes to classify the sample
			uint32_t start = micros();

			tf.predict(x_test, y_pred);

			uint32_t timeit = micros() - start;

			Serial.print("It took ");
			Serial.print(timeit);
			Serial.println(" micros to run inference");
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
			Serial.print("Sanity check: ");
			Serial.println(tf.predictClass(x_test));
			return tf.probaToClass(y_pred);
		}
};