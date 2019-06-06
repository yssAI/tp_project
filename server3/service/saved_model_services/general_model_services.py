# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

# !/usr/bin/env python2.7

"""Send JPEG image to tensorflow_model_server loaded with inception model.
"""
from __future__ import print_function

# This is a placeholder for a Google-internal import.

from grpc.beta import implementations
import tensorflow as tf

from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2
from tensorflow.python.framework import tensor_util
from tensorflow_serving.apis import classification_pb2
import numpy as np


def get_prediction_by_id(server, model_name, input_value,features):
    host, port = server.split(':')
    print('host')
    print(host)
    print('port')
    print(port)
    regression_models = ['Linear Regressor']
    classification_models = ['Linear Classifier', 'SVM']
    cluster_models = ['Kmeans Clustering', 'Gaussian Mixture Models Cluster']
    keras_models = ['Multilayer Perceptron', 'Image Classifier VGG16',
                    'Image Classifier VGG19', 'General Neural Network',
                    'Image Classifier Inception V3',
                    'Image Classifier Xception']

    if model_name in keras_models:
        channel = implementations.insecure_channel(host, int(port))
        stub = prediction_service_pb2.beta_create_PredictionService_stub(
            channel)
        request = predict_pb2.PredictRequest()
        request.model_spec.name = model_name
        request.model_spec.signature_name = 'predict'
        request.inputs['inputs'].CopyFrom(
            tf.contrib.util.make_tensor_proto(input_value))

        result = stub.Predict(request, 10.0)  # 10 secs timeout
        result = tensor_util.MakeNdarray(result.outputs['scores'])
        return str(result)
    else:
        channel = implementations.insecure_channel(host, int(port))
        stub = prediction_service_pb2.beta_create_PredictionService_stub(channel)
        request = predict_pb2.PredictRequest()
        request.model_spec.name = model_name
        input_value = np.asarray(input_value, dtype=np.float32)
        for idx, each_feature in enumerate(features):
            print(idx)
            print(each_feature)
            print(input_value[:, idx, np.newaxis])
            request.inputs[each_feature].CopyFrom(tf.contrib.util.make_tensor_proto(input_value[:, idx, np.newaxis]))
        result = stub.Predict(request, 10.0)  # 10 secs timeout
        print(result)
        if model_name == 'Kmeans Clustering':
            result = tensor_util.MakeNdarray(result.outputs['cluster_idx'])
        elif model_name == 'Gaussian Mixture Models Cluster':
            result = tensor_util.MakeNdarray(result.outputs['assignments'])
        elif model_name in classification_models:
            result = tensor_util.MakeNdarray(result.outputs['probabilities'])
            result = np.argmax(result, axis=1)
        else:
            result = tensor_util.MakeNdarray(result.outputs['scores'])
        return str(result)

