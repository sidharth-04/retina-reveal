import tensorflow as tf
import numpy as np

class RetinaGenerator:
    def __init__(self):
        return
    
    def load_model(self):
        self.generator = tf.keras.models.load_model('./static/models/generatorFinal.keras')
    
    def load(self, image_file):
        file_content = image_file.read()
        image_tensor = tf.convert_to_tensor(file_content)
        # image = tf.io.read_file('./static/images/RetinaSample.png')
        image = image_tensor
        image = tf.io.decode_jpeg(image)
        image = tf.cast(image, tf.float32)
        return image

    def resize(self, image, width, height):
        image = tf.image.resize(image, [height, width], method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
        return image

    def normalize(self, image):
        image = (image / 127.5) - 1
        return image

    def process_img(self, image_file):
        image = self.load(image_file)
        image = self.resize(image, 256, 256)
        image = self.normalize(image)
        image = np.expand_dims(image, axis=0)
        image = image[:, :, :, :3]
        return image

    def generate(self, image_file):
        image = self.process_img(image_file)
        prediction = self.generator(image, training=True)
        prediction = tf.squeeze(prediction)
        prediction = prediction.numpy()
        prediction = (prediction * 0.5 + 0.5) * 255
        return prediction

