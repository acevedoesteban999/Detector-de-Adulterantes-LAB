// #include <Arduino.h>
// #define LED_PIN 2
// #include "m.h"
// void setup() {
//   ddd();
//   pinMode(LED_PIN, OUTPUT);
// }

// void loop() {
//   digitalWrite(LED_PIN,HIGH);
//   delay(1000);
//   digitalWrite(LED_PIN,LOW);
//   delay(1000);
// }
#include <Arduino.h>
#include"as7265x.h"
#include <EloquentTinyML.h>
// copy the printed code from tinymlgen into this file
#include "_model_.h"
#include <WiFi.h>
#include ""
#define LED_PIN 2
#define NUMBER_OF_INPUTS 1
#define NUMBER_OF_OUTPUTS 1
#define TENSOR_ARENA_SIZE 1*1024
AS7265X as7265x;
//Eloquent::TinyML::TfLite<NUMBER_OF_INPUTS, NUMBER_OF_OUTPUTS, TENSOR_ARENA_SIZE> tf;
void setup() {
    ////////////////////////AP//////////////////////////
    //WiFi.mode(WIFI_AP)
    //WiFi.softAP("ESP32", "ESP32");


    
    ////////////////////////SCAN//////////////////////////
    // Serial.println("scan start");
    // WiFi.scanNetworks will return the number of networks found
    //   int n = WiFi.scanNetworks();
    //   Serial.println("scan done");
    //   if (n == 0) {
    //       Serial.println("no networks found");
    //   } else {
    //     Serial.print(n);
    //     Serial.println(" networks found");
    //     for (int i = 0; i < n; ++i) {
    //       // Print SSID and RSSI for each network found
    //       Serial.print(i + 1);
    //       Serial.print(": ");
    //       Serial.print(WiFi.SSID(i));
    //       Serial.print(" (");
    //       Serial.print(WiFi.RSSI(i));
    //       Serial.print(")");
    //       Serial.println((WiFi.encryptionType(i) == WIFI_AUTH_OPEN)?" ":"*");
    //       delay(10);
    //     }
    //   }
    //   Serial.println("");

    //   // Wait a bit before scanning again
    //   delay(5000);
    /////////////////////////CONNECT///////////////////////
    WiFi.mode(WIFI_STA);
    WiFi.disconnect();
    WiFi.begin("iPhone 6 Plus", "melon123445");
    Serial.print("Connecting to WiFi ..");
    while (WiFi.status() != WL_CONNECTED)
    {
        Serial.print('.');  
        delay(1000);
    }
    Serial.println(WiFi.localIP());
    //WiFi.disconnect()
    Serial.begin(9600);
    pinMode(LED_PIN, OUTPUT);
    //tf.begin(digits_model);
}

void loop() {
    ////////////////////////AS7265X///////////////////////////
    // Serial.println(String(as7265x.isConnected()).c_str());
    // as7265x.begin();
    // as7265x.takeMeasurementsWithBulb();
    // Serial.println(as7265x.getCalibratedA());
    
    ////////////////////////MLP///////////////////////////
    // // a random sample from the MNIST dataset (precisely the last one)
    // float x_test[NUMBER_OF_INPUTS] = { 5 };
    // // the output vector for the model predictions
    
    // float y_pred[NUMBER_OF_OUTPUTS] = {0};
    // // the actual class of the sample
    // float y_test = 0.127;

    // // let's see how long it takes to classify the sample
    // uint32_t start = micros();

    // tf.predict(x_test, y_pred);

    // uint32_t timeit = micros() - start;

    // Serial.print("It took ");
    // Serial.print(timeit);
    // Serial.println(" micros to run inference");

    // // let's print the raw predictions for all the classes
    // // these values are not directly interpretable as probabilities!
    // Serial.print("Test output is: ");
    // Serial.println(y_test);
    // Serial.print("Predicted proba are: ");

    // for (int i = 0; i < NUMBER_OF_OUTPUTS; i++) {
    //     Serial.print(y_pred[i]);
    //     Serial.print(i == NUMBER_OF_OUTPUTS ? '\n' : ',');
    // }

    // // let's print the "most probable" class
    // // you can either use probaToClass() if you also want to use all the probabilities
    // Serial.print("Predicted class is: ");
    // Serial.println(tf.probaToClass(y_pred));
    // // or you can skip the predict() method and call directly predictClass()
    // Serial.print("Sanity check: ");
    // Serial.println(tf.predictClass(x_test));

    // delay(5000);

    digitalWrite(LED_PIN,HIGH);
    delay(1000);
    digitalWrite(LED_PIN,LOW);
    delay(1000);
}