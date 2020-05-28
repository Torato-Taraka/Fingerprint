from myPackage import preprocess
from myPackage import minutiaeExtraction as minExtract
from enhancementFP import image_enhance as img_e
from os.path import basename, splitext
import os
import time
import numpy as np
from queue import Queue

from enhancementFP.ridge_segment import ridge_segment
from enhancementFP.ridge_orient import ridge_orient
from enhancementFP.ridge_freq import ridge_freq
from enhancementFP.ridge_filter import ridge_filter
from myPackage import tools as tl
import cv2
from os.path import exists, altsep

def image_enhance(gray, name, plot= False, path= None):
    print("Enhancing ridges...")
    blksze = 16
    thresh = 0.1
    normim,mask = ridge_segment(gray,blksze,thresh)           # normalise the image and find a ROI


    gradientsigma = 1
    blocksigma = 7
    orientsmoothsigma = 7
    orientim = ridge_orient(normim, gradientsigma, blocksigma, orientsmoothsigma)              # find orientation of every pixel


    blksze = 38
    windsze = 5
    minWaveLength = 5
    maxWaveLength = 15
    freq,medfreq = ridge_freq(normim, mask, orientim, blksze, windsze, minWaveLength,maxWaveLength)   #find the overall frequency of ridges
    
    freq = medfreq*mask
    kx = 0.65;ky = 0.65
    newim = ridge_filter(normim, orientim, freq, kx, ky)      # create gabor filter and do the actual filtering
    
    img_enhanced = (newim < -3).astype(float)

    if path is not None:
        new_path = altsep.join((path, "Enhanced"))
        if not exists(new_path):
            tl.makeDir(new_path)
        dst = altsep.join((new_path, (name + ".png")))
        img_color = cv2.cvtColor(img_enhanced, cv2.COLOR_GRAY2BGR)
        cv2.imwrite(dst, img_color)

    if plot:
        cv2.imshow("Enhanced '{}'".format(name), img_enhanced)
        cv2.waitKey(2000)
        cv2.destroyAllWindows()

    return img_enhanced

def cut(img):
    maxi, mini, maxj, minj = 0, len(img), 0, len(img[0])
    for i in range(len(img)):
        for j in range(len(img[0])):
            if img[i, j] > 0:
                if i > maxi:
                    maxi = i
                if i < mini:
                    mini = i
                if j > maxj:
                    maxj = j
                if j < minj:
                    minj = j
    return img[mini:maxi+1, minj:maxj+1]

def minutiae_extract(path, results):
    plot = True
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
        print("\nProcessing image '{}'".format(name))
        cleaned_img = preprocess.blurrImage(image, name, plot)
        enhanced_img = cut(image_enhance(cleaned_img, name, plot))
        cleaned_img = preprocess.cleanImage(enhanced_img, name, plot)
        #skeleton = preprocess.zhangSuen(cleaned_img, name, plot)
        skeleton = preprocess.thinImage(cleaned_img, name, plot)
        minExtract.process(skeleton, name, plot, results)
        all_times.append((time.time()-start))
    mean, std = 0, 0
    mean = np.mean(all_times)
    std = np.std(all_times)
    print("\n\nAlgorithm takes {:2.3f} (+/-{:2.3f}) seconds per image".format(mean, std))

    
if __name__ == "__main__" :
    minutiae_extract("test\\", "test_result\\")