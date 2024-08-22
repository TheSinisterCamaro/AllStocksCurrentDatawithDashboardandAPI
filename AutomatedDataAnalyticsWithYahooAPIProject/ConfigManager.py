import os
import tensorflow as tf
import logging
import warnings

class ConfigManager:
    def __init__(self):
        self.setup_environment()

    def setup_environment(self):
        # Disable oneDNN custom operations
        os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
        print("TF_ENABLE_ONEDNN_OPTS:", os.environ.get('TF_ENABLE_ONEDNN_OPTS'))

        # Suppress TensorFlow logs
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
        tf.get_logger().setLevel(logging.ERROR)

        warnings.filterwarnings("ignore")
