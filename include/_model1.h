// #include <TensorFlowLite_ESP32.h>
// #include <tensorflow/lite/micro/micro_error_reporter.h>
// #include <tensorflow/lite/micro/micro_interpreter.h>
// #include <tensorflow/lite/micro/all_ops_resolver.h>
// #define inputSize 18
// #define outputSize 5
// class Model_1
// {
//     private:
//         const tflite::Model* model_;
//         float input_tensor_buffer_[inputSize];
//         float output_tensor_buffer_[outputSize];
//     public:
//         Model_1() : model_(nullptr) {}
//         ~Model_1() 
//         {
//             // if (model_) 
//             // {
//             //     TfLiteModelDelete(model_);
//             //     model_ = nullptr;
//             // }
//         }
//         bool LoadModel(const char* model)
//         {
//             model_ = tflite::GetModel(model);
//             return (model_ != nullptr);
//         }

//         bool Predict(const float* input_data, float* output_data) {
//         if (!model_) 
//         {
//             return false;
//         }

//         tflite::MicroErrorReporter error_reporter;
//         tflite::AllOpsResolver resolver;
//         tflite::MicroInterpreter interpreter(model_, resolver, input_tensor_buffer_, output_tensor_buffer_, &error_reporter);

//         TfLiteTensor* input_tensor = interpreter.input(0);
//         TfLiteTensor* output_tensor = interpreter.output(0);

//         // Copiar los datos de entrada al tensor de entrada
//         const int input_tensor_size = input_tensor->bytes / sizeof(float);
//         memcpy(input_tensor->data.f, input_data, input_tensor_size * sizeof(float));

//         // Realizar la inferencia
//         interpreter.Invoke();

//         // Copiar los resultados de salida al arreglo de salida
//         const int output_tensor_size = output_tensor->bytes / sizeof(float);
//         memcpy(output_data, output_tensor->data.f, output_tensor_size * sizeof(float));

//         return true;
//     }
//     uint8_t probaToClass(float *output) {
//         uint8_t classIdx = 0;
//         float maxProba = output[0];

//         for (uint8_t i = 1; i < outputSize; i++) {
//             if (output[i] > maxProba) {
//                 classIdx = i;
//                 maxProba = output[i];
//             }
//         }

//         return classIdx;
//     }

// };