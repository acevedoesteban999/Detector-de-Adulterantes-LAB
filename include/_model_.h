#define NUMBER_OF_INPUTS 18
#define NUMBER_OF_OUTPUTS 5
#define TENSOR_ARENA_SIZE 5*1024
#include <EloquentTinyML.h>
#include "M1.h"

class Model
{
	private:
		Eloquent::TinyML::TfLite<NUMBER_OF_INPUTS, NUMBER_OF_OUTPUTS, TENSOR_ARENA_SIZE> tf;
	public:
		Model()
		{}
		~Model()
		{}
		bool start()
		{
			//unsigned char model_data[] __attribute__((aligned(4)))={}	;
			//tf.begin(model_data);
			return true;
		}
		void predict()
		{
			float x_test[NUMBER_OF_INPUTS] = { 1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3};
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
			Serial.print("Predicted class is: ");
			Serial.println(tf.probaToClass(y_pred));
			// or you can skip the predict() method and call directly predictClass()
			Serial.print("Sanity check: ");
			Serial.println(tf.predictClass(x_test));
		}
};