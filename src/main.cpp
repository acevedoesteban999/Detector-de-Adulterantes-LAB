#include <Arduino.h>
//#include"as7265x.h"
//#include <EloquentTinyML.h>
// copy the printed code from tinymlgen into this file
//#include "_model_.h"
#include <WiFi.h>
//#include "WebServer.h"
#define LED_PIN 2
//#define NUMBER_OF_INPUTS 1
//#define NUMBER_OF_OUTPUTS 1
//#define TENSOR_ARENA_SIZE 1*1024
//AS7265X as7265x;
#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>
#include "SPIFFS.h"
//WebServer ws;
AsyncWebServer server(80);
//Eloquent::TinyML::TfLite<NUMBER_OF_INPUTS, NUMBER_OF_OUTPUTS, TENSOR_ARENA_SIZE> tf;
void setup() {
    Serial.begin(115200);
    pinMode(LED_PIN, OUTPUT);
    
    if(!SPIFFS.begin(true))
    {
        Serial.println("An Error has occurred while mounting SPIFFS");
        return;
    }



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
    server.on("/a", HTTP_GET, [](AsyncWebServerRequest *request){
        request->send(SPIFFS, "/index.html");
    });
    server.on("/hi", HTTP_GET, [](AsyncWebServerRequest *request)
    {
        request->send(200, "text/plain", "Hello AsyncWebServer!");
    });
    server.begin();

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






/*
// Importing necessary libraries
#include <WiFi.h>
#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>

// Setting network credentials
const char* ssid = "iPhone 6 Plus";
const char* password = "melon123445";

const char* input_parameter1 = "output";
const char* input_parameter2 = "state";

// Creating a AsyncWebServer object 
AsyncWebServer server(80);


const char index_html[] PROGMEM = R"rawliteral(
<!DOCTYPE HTML><html>
<head>
  <title>ESP32 WEB SERVER</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,">
  <style>
    html {font-family: Arial; display: inline-block; text-align: center;}
    p {font-size: 3.0rem;}
    body {max-width: 600px; margin:0px auto; padding-bottom: 25px;}
    .switch {position: relative; display: inline-block; width: 120px; height: 68px} 
    .switch input {display: none}
    .slider {position: absolute; top: 0; left: 0; right: 0; bottom: 0; background-color: #ccc; border-radius: 6px}
    .slider:before {position: absolute; content: ""; height: 52px; width: 52px; left: 8px; bottom: 8px; background-color: #fff; -webkit-transition: .4s; transition: .4s; border-radius: 3px}
    input:checked+.slider {background-color: #b30000}
    input:checked+.slider:before {-webkit-transform: translateX(52px); -ms-transform: translateX(52px); transform: translateX(52px)}
  </style>
</head>
<body>
  <h2>ESP32 WEB SERVER</h2>
  %BUTTONPLACEHOLDER%
<script>function toggleCheckbox(element) {
  var xhr = new XMLHttpRequest();
  if(element.checked){ xhr.open("GET", "/update?output="+element.id+"&state=1", true); }
  else { xhr.open("GET", "/update?output="+element.id+"&state=0", true); }
  xhr.send();
}
</script>
</body>
</html>
)rawliteral";

// Replaces placeholder with button section in your web page
String outputState(int output){
  if(digitalRead(output)){
    return "checked";
  }
  else {
    return "";
  }
}
String processor(const String& var){
  //Serial.println(var);
  if(var == "BUTTONPLACEHOLDER"){
    String buttons = "";
    buttons += "<h4>Output - GPIO 32</h4><label class=\"switch\"><input type=\"checkbox\" onchange=\"toggleCheckbox(this)\" id=\"32\" " + outputState(32) + "><span class=\"slider\"></span></label>";

    buttons += "<h4>Output - GPIO 25</h4><label class=\"switch\"><input type=\"checkbox\" onchange=\"toggleCheckbox(this)\" id=\"25\" " + outputState(25) + "><span class=\"slider\"></span></label>";

    buttons += "<h4>Output - GPIO 27</h4><label class=\"switch\"><input type=\"checkbox\" onchange=\"toggleCheckbox(this)\" id=\"27\" " + outputState(27) + "><span class=\"slider\"></span></label>";

   buttons += "<h4>Output - GPIO 13</h4><label class=\"switch\"><input type=\"checkbox\" onchange=\"toggleCheckbox(this)\" id=\"13\" " + outputState(13) + "><span class=\"slider\"></span></label>";

    return buttons;
  }
  return String();
}



void setup(){
  // Serial port for debugging purposes
  Serial.begin(115200);

pinMode(32,OUTPUT);
digitalWrite(32, LOW);
pinMode(25, OUTPUT);
digitalWrite(25, LOW);
pinMode(27, OUTPUT);
digitalWrite(27, LOW);
pinMode(13, OUTPUT);
digitalWrite(13, LOW);

  
  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi");
  }

  // Print ESP Local IP Address
  Serial.println(WiFi.localIP());

  // Route for root / web page
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send_P(200, "text/html", index_html, processor);
  });

  // Send a GET request to <ESP_IP>/update?output=<inputMessage1>&state=<inputMessage2>
  server.on("/update", HTTP_GET, [] (AsyncWebServerRequest *request) {
    String inputMessage1;
    String inputMessage2;
    // GET input1 value on <ESP_IP>/update?output=<inputMessage1>&state=<inputMessage2>
    if (request->hasParam(input_parameter1) && request->hasParam(input_parameter2)) {
      inputMessage1 = request->getParam(input_parameter1)->value();
      inputMessage2 = request->getParam(input_parameter2)->value();
      digitalWrite(inputMessage1.toInt(), inputMessage2.toInt());
    }
    else {
      inputMessage1 = "No message sent";
      inputMessage2 = "No message sent";
    }
    Serial.print("GPIO: ");
    Serial.print(inputMessage1);
    Serial.print(" - Set to: ");
    Serial.println(inputMessage2);
    request->send(200, "text/plain", "OK");
  });

  // Start server
  server.begin();
}

void loop() {

}
*/