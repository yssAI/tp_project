import grpc
import requests
import tensorflow as tf
import numpy as np
from sklearn.externals import joblib
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2_grpc

from server3.business.general_business import GeneralBusiness
from server3.constants import TF_SERVING_URL


class GrpcRequestBusiness(GeneralBusiness):

    input_scaler = joblib.load('../model/input_scaler')
    output_scaler = joblib.load('../model/output_scaler')

    @classmethod
    def request_client(cls, input_data):
        '''
        向TensorFlow Serving服务请求predict的函数
        input_data: 输入数据，numpy array，shape：(n, 10, 6)
        server_url: 地址加端口，str，如：'0.0.0.0:8500'
        '''
        # normalization
        input_data_normal = cls.input_scaler.fit_transform(input_data)
        input_data_process = input_data_normal.reshape(1, input_data_normal.shape[0], input_data_normal.shape[1])

        # Request
        channel = grpc.insecure_channel(TF_SERVING_URL)
        stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)
        request = predict_pb2.PredictRequest()
        request.model_spec.name = "temperature"  # 模型名称
        request.model_spec.signature_name = "predict"  # 签名名称
        # "inputs"是导出模型时设置的输入名称
        request.inputs["inputs"].CopyFrom(
            tf.contrib.util.make_tensor_proto(input_data_process, shape=list(input_data_process.shape)))
        response = stub.Predict(request, 5.0)  # 5 secs timeout
        # output Data conversion
        response_content = np.asarray(response.outputs["output"].float_val)
        result = cls.output_scaler.inverse_transform(response_content.reshape(-1, 1))[0, 0]
        return result


if __name__ == '__main__':
    input_data = np.array(
        [[18.9 , 66.1 , 23.09, 44.41,  0.  ,  1.  ],
         [18.9 , 66.1 , 23.  , 44.46,  0.  ,  1.  ],
         [18.9 , 66.21, 23.  , 44.43,  0.  ,  1.  ],
         [18.87, 66.31, 23.  , 44.46,  0.  ,  1.17],
         [18.83, 66.41, 22.99, 44.49,  0.  ,  1.33],
         [18.8 , 66.51, 22.99, 44.52,  0.  ,  0.79],
         [18.77, 66.6 , 22.98, 44.55,  0.  ,  0.67],
         [18.73, 66.7 , 22.98, 44.58,  0.  ,  0.83],
         [18.7 , 66.8 , 22.97, 44.61,  0.  ,  1.  ],
         [18.7 , 66.81, 22.9 , 44.56,  0.  ,  0.83],
         [18.7 , 66.9 , 23.  , 44.5 ,  0.  ,  0.92],
         [18.6 , 66.83, 22.98, 44.43,  0.  ,  1.5 ],
         [18.6 , 66.9 , 22.94, 44.44,  0.  ,  1.33],
         [18.6 , 66.9 , 22.9 , 44.4 ,  0.  ,  1.17],
         [18.6 , 66.82, 22.94, 44.38,  0.  ,  1.  ],
         [18.6 , 66.85, 22.9 , 44.38,  0.  ,  1.  ],
         [18.6 , 66.64, 22.9 , 44.32,  0.  ,  1.55],
         [18.6 , 66.4 , 22.9 , 44.22,  0.  ,  1.  ],
         [18.6 , 66.45, 22.9 , 44.18,  0.  ,  1.  ],
         [18.67, 66.54, 22.9 , 44.19,  0.  ,  1.  ]], dtype=np.float32)

    result = GrpcRequestBusiness.request_client(input_data)
    print(result)

