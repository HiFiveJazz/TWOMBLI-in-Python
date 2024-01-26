#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 21:28:31 2024

@author: jazz
"""

# Anamorf Paramaters:
    
# <entry key="Noise Reduction Filter Radius (µm)">1</entry>
# <entry key="Background Filter Radius (µm^2)">50.0</entry>
# <entry key="Image Resolution (µm/pixel)">1.0</entry>
# <entry key="Curvature Window">20</entry>
# <entry key="Maximum Circularity">1.0</entry>
# <entry key="Minimum Area (µm^2)">10.0</entry>
# <entry key="Image Format">PNG</entry>
# <entry key="Minimum Branch Length (µm)">10.0</entry>

# General Parameters:
# Contrast Saturation,0.35
# Min Line Width,5
# Max Line Width,5
# Min Curvature Window,50
# Max Curvature Window,50
# Minimum Branch Length,10
# Maximum Display HDM,200
# Minimum Gap Diameter,39
import numpy as np
from pathlib import Path
from PIL import Image, ImageEnhance
import os
import cv2
def import_image(file_path):
    try:
        image = Image.open(file_path)
        #Implement cropping image below?
        # image = image.resize((width, height))

        return image
    except Exception as e:
        print(f"Error: {e}")
        return None

def convert_to_8bit(image):
    try:
        converted_image = image.convert("L")
        return converted_image
    except Exception as e:
        print(f"Error: {e}")
        return None

#Implement overwriting an image
#Include adjusting contrast, saturation 

def user_adjusts_saturationcontrast(image, saturation, contrast):
    try:
        # Saturation Adjuster (Default = 0.33)
        saturation_enhancer = ImageEnhance.Color(image)
        image = saturation_enhancer.enhance(saturation*3)
        
        # Constrast Adjuster (Default = 0.1)
        contrast_enhancer = ImageEnhance.Contrast(image)
        adjusted_image = contrast_enhancer.enhance((contrast*10))
        return adjusted_image
    except Exception as e:
        print(f"Error: {e}")
        return None 

def create_mask_image(image, threshold=128):

    # Apply threshold to create a black and white image
    mask_image = image.point(lambda x: 0 if x < threshold else 255, '1')

    return mask_image

def mkdir_and_save_image(folder_name, image_name, image_content):
    desktop_path = str(Path.home() / "Desktop")
    folder_path = os.path.join(desktop_path, folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder '{folder_name}' created on the desktop.")

    image_path = os.path.join(folder_path, image_name)
    image_content.save(image_path)

    print(f"Image '{image_name}' saved in '{folder_name}' on the desktop.")

def enhance_branches(image):
    """Apply top-hat transform to enhance branches in the image."""
    
    image = np.array(image)
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Define a structuring element for morphological operation
    kernel_size = 15  # Adjust the kernel size based on the size of branches
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    
    # Apply top-hat transform
    top_hat = cv2.morphologyEx(gray_image, cv2.MORPH_TOPHAT, kernel)
    
    top_hat = Image.fromarray(top_hat)
    
    return top_hat


file_path = "/Users/jazz/Desktop/2L_2D.png"
output_path = "/Users/jazz/Desktop/"
image_variable = import_image(file_path)
image_8bit = convert_to_8bit(image_variable)


#Settings for User
#Saturation range (Default = 0.33) Does not impact gray scale
saturation = 1

#Contrast Ranges 0 - 1 (Default = 0.1)
contrast = 0.1
adjusted_image = user_adjusts_saturationcontrast(image_8bit, saturation, contrast)

# adjusted_image.save(f"{output_path}/image_variable.png")
adjusted_image = enhance_branches(image_variable)
mkdir_and_save_image('TWOMBLI Photos','masa.png',adjusted_image)

if image_variable:
    print("Image imported successfully.")
else:
    print("Failed to import the image.")

#Parameters:

#Constrast Saturation:
#Saturates this percentage of pixels

# Line Width
# Ridge detection will trace a mask looking for matrix  fibre bundles of approximately this width.

# Curvature Window
# The length over which the change in angle will be measured

# Minimum Branch Length
# Branches on mask below this length will be ignored (set by default to 10% of Curvature Window) by AnaMorf

# Minimum gap diameter
# For optional gap analysis 

# Maximum Display HDM
# Pixel intensities above this value will be ignored.

#Image Analysis Begins
#Implement the following steps to image analysis
#Ridge Detection
#Canny-Edge Detection
#Generating HDM images
#Cropping down of Images for ROIs

#Statistics
#Total Length
#Number of End Points
#Average Fiber Length



#fiber_length = 0.5*(endpoints + branchpoints)

#Creating mask images from TWOMBLI






# mask_image = image_variable.convert("L")
# mask_image.save(f"{output_path}/image_variable.png")

   
