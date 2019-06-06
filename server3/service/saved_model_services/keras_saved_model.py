import os
import sys

from tensorflow.python.saved_model import builder as saved_model_builder
from tensorflow.python.saved_model import tag_constants
from tensorflow.python.saved_model.signature_def_utils_impl import \
    predict_signature_def
from tensorflow.python.lib.io import file_io

from server3.lib import K
from server3.lib import tf


# very important to do this as a first thing
K.set_learning_phase(0)


def export(new_model, export_path_base, weights_dir):
    """

    :param new_model: model structure load from json
    :param export_path_base: path to export model
    :param weights_dir: path where weights stored, h5 file
    :return:
    """
    # Exporting the model
    # new_model.load_weights(weights_dir)
    model_version = 1
    # tf.app.flags.DEFINE_integer('model_version', 1,
    #                             'version number of the model.')
    # tf.app.flags.DEFINE_string('work_dir', working_dir, 'Working directory.')
    FLAGS = tf.app.flags.FLAGS
    export_path = os.path.join(
        tf.compat.as_bytes(export_path_base),
        tf.compat.as_bytes(str(model_version)))

    # if version path exists, create a new version
    while file_io.file_exists(export_path):
        model_version += 1
        export_path = os.path.join(
            tf.compat.as_bytes(export_path_base),
            tf.compat.as_bytes(str(model_version)))

    builder = saved_model_builder.SavedModelBuilder(export_path)

    # with K.get_session() as sess:

    sess = tf.InteractiveSession()
    sess.run(tf.global_variables_initializer())
    K.set_session(sess)
    with sess.as_default():
        new_model.load_weights(weights_dir)

        signature = predict_signature_def(inputs={'inputs': new_model.input},
                                          outputs={'scores': new_model.output})
        builder.add_meta_graph_and_variables(sess=sess,
                                             tags=[tag_constants.SERVING],
                                             signature_def_map={
                                                 'predict': signature})
        builder.save()
        return model_version


def save_model(result_dir, model):
    model.save_weights(os.path.join(result_dir, 'final.hdf5'))
    with open(os.path.join(result_dir, 'model.json'), 'w') as f:
        f.write(model.to_json())