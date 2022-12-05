# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 19:16:19 2022

@author: timle
"""

import numpy as np
import cv2
import os
from os import listdir
from pathlib import Path
import glob

#Initialize folder directories
folder_dir = "C:/Users/timle/Box/Easy Calibration toolbox/3 Final Report/Extrinsic Calibration/Source Image"
images = Path(folder_dir).glob('*.png')
path = glob.glob("C:/Users/timle/Box/Easy Calibration toolbox/3 Final Report/Extrinsic Calibration/Source Image/*.png")

#Define amount of each type
noiseCount = 0
targetCount = 0
count = 0
unidtfyCount = 0


#Set up red laser HSV range
lower_red1 = np.array([0,0,200])
upper_red1 = np.array([35,255,255])

lower_red2 = np.array([340,0,200])
upper_red2 = np.array([359,255,255])



for image in path:
    print(count)#Let the user know the image processing progress
    
    imageState = 0#Initialize image state, state = 0 means target image, otherwise noise image
    
    input_image = cv2.imread(image)
    retval, corners = cv2.findChessboardCorners(input_image, (7,10), flags=cv2.CALIB_CB_FAST_CHECK);
    
    input_image_HSV = cv2.cvtColor(input_image,cv2.COLOR_BGR2HSV)
    

    mask1 = cv2.inRange(input_image_HSV, lower_red1, upper_red1)
    mask2 = cv2.inRange(input_image_HSV, lower_red2, upper_red2)
    
    red_pixels = np.argwhere(mask1)
    #red_pixels = np.vstack((np.argwhere(mask1),np.argwhere(mask2)))
    
   
    if retval == True:
        #cv2.drawChessboardCorners(input_image, (7, 10), corners, retval)
        for px, py in red_pixels:
            find = False
            for cy, cx in corners.reshape(70,2):
                diffx = abs(px-cx)
                diffy = abs(py-cy)
                if diffx <= 50 and diffy <= 50:
                    find = True #Make sure quit both for-loop with crossing is find
                    imageState += 1
                    cv2.circle(input_image, (py, px), 5, (0, 255, 255), 1)
                    break
            if find:
                break #Make sure quit both for-loop with crossing is find

                    
        if imageState == 0:
            os.chdir("C:/Users/timle/Box/Easy Calibration toolbox/3 Final Report/Extrinsic Calibration/Target Image")
            cv2.imwrite("target-" + str(targetCount) + ".png",input_image)
            targetCount += 1
        else:
            os.chdir("C:/Users/timle/Box/Easy Calibration toolbox/3 Final Report/Extrinsic Calibration/Noise Image")
            cv2.imwrite("noise-" + str(noiseCount) + ".png",input_image)
            noiseCount += 1
        
    elif retval == False:
        os.chdir("C:/Users/timle/Box/Easy Calibration toolbox/3 Final Report/Extrinsic Calibration/Unidentified")
        cv2.imwrite("unidentified-" + str(unidtfyCount) + ".png",input_image)
        unidtfyCount += 1
    
    count += 1


#D & E image processing-currently unused--------------------------------------
#k_e = cv2.getStructuringElement(cv2. MORPH_CROSS,(3,3))

#for i in range (3):
#    input_image_BIN = cv2.dilate(input_image_BIN, k_e)
    
#for i in range (7):
#    input_image_BIN = cv2.erode(input_image_BIN, k_e)
    
#for i in range (5):
#    input_image_BIN = cv2.dilate(input_image_BIN, k_e)
       

#cv2.waitKey()
#cv2.destroyAllWindows()