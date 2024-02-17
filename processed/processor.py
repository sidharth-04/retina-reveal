import os
import cv2
import numpy as np
import random

def apply_blur(image, n):
    processed_image = image
    for _ in range(n):
        processed_image = cv2.GaussianBlur(processed_image, (15, 15), 0)
    return processed_image

def apply_expose(image):
    if random.randint(0, 100) < 50:
        processed_image = np.clip(image * 0.7, 0, 255).astype(np.uint8) 
    else:
        processed_image = np.clip(image * 1.5, 0, 255).astype(np.uint8) 
    return processed_image

def process_image(image):
    processed_image = image
    processed_image = cv2.resize(processed_image, (256, 256))
    # real_image = processed_image
    processed_image = apply_blur(processed_image, 1)
    if random.randint(0, 100) < 80:
        processed_image = apply_blur(processed_image, 2)
    if random.randint(0, 100) < 40:
        processed_image = apply_expose(processed_image)
    if random.randint(0, 100) < 100:
        processed_image = apply_expose(processed_image) 
        processed_image = apply_blur(processed_image, 1)
    # final_image = np.concatenate([real_image, processed_image], axis=1)
    return processed_image

def process_images(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    i = 1
    for filename in os.listdir(input_folder):
        image_path = os.path.join(input_folder, filename)
        image = cv2.imread(image_path) 
        try:
            processed_image = process_image(image)
            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, processed_image)
        except:
            print("Something went wrong with: "+image_path)
        print(i)
        i += 1

process_images("OriginalTestData", "testSamples")
