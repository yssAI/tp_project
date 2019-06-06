from grpc.beta import implementations
import tensorflow as tf

from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2


tf.app.flags.DEFINE_string('server', 'localhost:9000',
                           'PredictionService host:port')
tf.app.flags.DEFINE_string('image', '', 'path to image in JPEG format')
FLAGS = tf.app.flags.FLAGS

from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.imagenet_utils import preprocess_input
import numpy as np


def load_preprocess_img(img_path, target_size=(224, 224)):
    img = load_img(img_path, target_size=target_size)
    x = img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return x


def main(_):
    host, port = FLAGS.server.split(':')
    channel = implementations.insecure_channel(host, int(port))
    stub = prediction_service_pb2.beta_create_PredictionService_stub(channel)
    img = load_preprocess_img(FLAGS.image)
    request = predict_pb2.PredictRequest()
    request.model_spec.name = 'vgg19'
    request.model_spec.signature_name = 'predict'
    request.inputs['inputs'].CopyFrom(tf.contrib.util.make_tensor_proto(img))

    result = stub.Predict(request, 10.0)  # 10 secs timeout
    print(result)
    to_decode = np.expand_dims(result.outputs['scores'].float_val, axis=0)
    from tensorflow.contrib.keras.python.keras.applications.vgg19 import \
        decode_predictions
    decoded = decode_predictions(to_decode)
    print(decoded)


if __name__ == '__main__':
    tf.app.run()
