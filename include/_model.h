#pragma once
#define NUMBER_OF_INPUTS 18
#define NUMBER_OF_OUTPUTS 5
#define TENSOR_ARENA_SIZE 5*1024
#include <_eloquentTinyML.h>
#include "_object.h"
#include "_spiffs.h"


class Model
{
	private:
        bool active;
		String model_name;
		_18float data;
		Spiffs*spiffs;
		float y_pred[NUMBER_OF_OUTPUTS];
		_Eloquent::_TinyML::_TfLite<NUMBER_OF_INPUTS, NUMBER_OF_OUTPUTS, TENSOR_ARENA_SIZE> tf;
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
			tf.clear();
		}
		void init(Spiffs*spiffs)
		{
			this->spiffs=spiffs;
		}
		bool start(Object&obj)
		{
			active=tf.begin(obj.get_data());
			return active;
		}
		bool restart()
		{
			this->clear();
			Object obj;
			spiffs->load_data("/model",obj);
			return this->start(obj);
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
			
			//Serial.println("B");
			tf.predict(data.get_18(), y_pred);
			//Serial.println("B");
			//Serial.print("Predicted proba are: ");
			
			//for (int i = 0; i < NUMBER_OF_OUTPUTS; i++) {
			//	Serial.print(y_pred[i]);
			//	Serial.print(i == NUMBER_OF_OUTPUTS ? '\n' : ',');
			//}
			
			//Serial.print("\nPredicted class is: ");
			//Serial.println(tf.probaToClass(y_pred));
			
			return _2data(tf.probaToClass(y_pred),y_pred[tf.probaToClass(y_pred)]);
		}
};
