import argparse
from myPackage import tools as tl
from myPackage import preprocess
from myPackage import minutiaeExtraction as minExtract
from enhancementFP import image_enhance as img_e
from os.path import basename, splitext
import os
import time
import cv2
import matplotlib.pyplot as plt
import numpy as np


def minutiae_extract(path, results):
    plot = False
    # ratio = 0.2
    # Extract names
    all_images = []
    for f in os.listdir(path):
        all_images.append(os.path.join(path, f))
    # Split train and test data
    # train_data, test_data = tl.split_train_test(all_images, ratio)
    print("\nAll_images size: {}\n".format(len(all_images)))
    all_times= []
    for image in all_images:
        start = time.time()
        name = splitext(basename(image))[0]
        print(image)
        print("\nProcessing image '{}'".format(name))
        cleaned_img = preprocess.blurrImage(image, name, plot)
        enhanced_img = img_e.image_enhance(cleaned_img, name, plot)
        print(type(enhanced_img))
        cleaned_img = preprocess.cleanImage(enhanced_img, name, plot)
        skeleton = preprocess.thinImage(cleaned_img, name, plot)
        minExtract.process(skeleton, name, plot, results)
        all_times.append((time.time()-start))
    mean, std = 0, 0
    mean = np.mean(all_times)
    std = np.std(all_times)
    print("\n\nAlgorithm takes {:2.3f} (+/-{:2.3f}) seconds per image".format(mean, std))

    
if __name__ == "__main__" :
    minutiae_extract("test\\", "test_result\\")