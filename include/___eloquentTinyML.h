#pragma once

#include <Arduino.h>
#include <math.h>
#include "tensorflow/lite/micro/micro_mutable_op_resolver.h"
#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/micro/system_setup.h"
#include "tensorflow/lite/schema/schema_generated.h"

namespace _Eloquent {
    namespace _TinyML {

        enum _TfLiteError {
            OK,
            VERSION_MISMATCH,
            CANNOT_ALLOCATE_TENSORS,
            NOT_INITIALIZED,
            INVOKE_ERROR
        };

        /**
         * _Eloquent interface to Tensorflow Lite for Microcontrollers
         *
         * @tparam inputSize
         * @tparam outputSize
         * @tparam tensorArenaSize how much memory to allocate to the tensors
         */
        template<size_t inputSize, size_t outputSize, size_t tensorArenaSize>
        class _TfLite {
        protected:
            bool failed,active;
            _TfLiteError error;
            uint8_t tensorArena[tensorArenaSize];
            tflite::MicroInterpreter *interpreter;
            tflite::MicroMutableOpResolver<5>*resolver;
            TfLiteTensor *input;
            TfLiteTensor *output;
            const tflite::Model *model;
        public:
            /**
             * Contructor
             * @param modelData a model as exported by tinymlgen
             */
            _TfLite() :
                failed(false) {
                    active=false;
            }
            ~_TfLite()
            {
                clear();
            }
            
            /**
             * Inizialize NN
             *
             * @param modelData
             * @return
             */
            void clear()
            {
                //delete reporter;
                delete interpreter;
                delete resolver;
                active=false;
            }
            bool begin(const unsigned char *modelData) {
                
                if (active)
                    return false;
                
                model = tflite::GetModel(modelData);
                
                this->resolver=new tflite::MicroMutableOpResolver<5>();
                if (resolver->AddFullyConnected() != kTfLiteOk) {
                    MicroPrintf("AddFullyConnected failed");
                    return false;
                }
                if (resolver->AddSoftmax() != kTfLiteOk) {
                    MicroPrintf("AddSoftmax failed");
                    return false;
                }
                // assert model version and runtime version match
                if (model->version() != TFLITE_SCHEMA_VERSION) {
                    failed = true;
                    error = VERSION_MISMATCH;

                    MicroPrintf("Model provided is schema version %d not equal to supported "
                        "version %d.", model->version(), TFLITE_SCHEMA_VERSION);
                    return false;
                }
                

                //tflite::MicroInterpreter interpreter(model, resolver, tensorArena, tensorArenaSize, reporter);
                
                this->interpreter=new tflite::MicroInterpreter(model, *resolver, tensorArena, tensorArenaSize);
                if (interpreter->AllocateTensors() != kTfLiteOk) {
                    failed = true;
                    error = CANNOT_ALLOCATE_TENSORS;
                    MicroPrintf("AllocateTensors() failed");
                    return false;
                }
            

                input = interpreter->input(0);
                output = interpreter->output(0);
                error = OK;
                
                //this->interpreter = &interpreter;
                active=true;
                return true;
            }
            // void clear()
            // {
            //     interpreter->~MicroInterpreter();
            //     model-();
            // }
            /**
             * Test if the initialization completed fine
             */
            bool initialized() {
                return !failed;
            }

            /**
             *
             * @param input
             * @param output
             * @return
             */
            uint8_t predict(uint8_t *input, uint8_t *output = NULL) {
                // abort if initialization failed
                if (!initialized())
                    return sqrt(-1);

                memcpy(this->input->data.uint8, input, sizeof(uint8_t) * inputSize);

                if (interpreter->Invoke() != kTfLiteOk) {
                    MicroPrintf("Inference failed");

                    return sqrt(-1);
                }

                // copy output
                if (output != NULL) {
                    for (uint16_t i = 0; i < outputSize; i++)
                        output[i] = this->output->data.uint8[i];
                }

                return this->output->data.uint8[0];
            }

            /**
             * Run inference
             * @return output[0], so you can use it directly if it's the only output
             */
            float predict(float *input, float *output = NULL) {
                // abort if initialization failed
                if (!initialized()) {
                    error = NOT_INITIALIZED;

                    return sqrt(-1);
                }

                // copy input
                for (size_t i = 0; i < inputSize; i++)
                    this->input->data.f[i] = input[i];

                if (interpreter->Invoke() != kTfLiteOk) {
                    error = INVOKE_ERROR;
                    MicroPrintf("Inference failed");

                    return sqrt(-1);
                }

                // copy output
                if (output != NULL) {
                    for (uint16_t i = 0; i < outputSize; i++)
                        output[i] = this->output->data.f[i];
                }

                return this->output->data.f[0];
            }

            /**
             * Predict class
             * @param input
             * @return
             */
            uint8_t predictClass(float *input) {
                float output[outputSize];

                predict(input, output);

                return probaToClass(output);
            }

            /**
             * Get class with highest probability
             * @param output
             * @return
             */
            uint8_t probaToClass(float *output) {
                uint8_t classIdx = 0;
                float maxProba = output[0];

                for (uint8_t i = 1; i < outputSize; i++) {
                    if (output[i] > maxProba) {
                        classIdx = i;
                        maxProba = output[i];
                    }
                }

                return classIdx;
            }

            /**
             * Get error message
             * @return
             */
            const char* errorMessage() {
                switch (error) {
                    case OK:
                        return "No error";
                    case VERSION_MISMATCH:
                        return "Version mismatch";
                    case CANNOT_ALLOCATE_TENSORS:
                        return "Cannot allocate tensors";
                    case NOT_INITIALIZED:
                        return "Interpreter has not been initialized";
                    case INVOKE_ERROR:
                        return "Interpreter invoke() returned an error";
                    default:
                        return "Unknown error";
                }
            }

        
        };
    }
}
