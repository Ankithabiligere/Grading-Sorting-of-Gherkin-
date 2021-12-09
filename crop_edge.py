# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 10:10:40 2021

@author: 91872
"""
import time
import cv2
import cv2 as cv
import numpy as np

import os


def crop_edge(image):
   
   
    # image= image[10:300, 80:560]
    image1a=image
    image11=image
    #image= image[20:500, 200:1056]
    #image= image[220:700,80:500]
    # image= image[100:950,0:1200]
    #print(filename)Z
    # image= image[10:350, 65:550]
    # cv2.imshow("crop", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
     
    hsv= cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    lower_color = np.array([0,53,0]) #45  #binary detection 12/11/2021
    upper_color = np.array([63,255,255])#70 
    
    binary = cv2.inRange(hsv, lower_color, upper_color)
    # cv2.imshow('binary', binary)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    contours,hierarchy = cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #Dis_count=len(contours)
    
    s=0
    m=0
    l=0
    q=0
    for cnt in contours:
        hull = cv2.convexHull(cnt)
        aaa=cv2.contourArea(hull)
        #print(aaa)
        rect = cv2.minAreaRect(cnt)             # rect = ((center_x,center_y),(width,height),angle)
        l=rect[1][0]
        w=rect[1][1]
        ll=rect[0][0]
        ww=rect[0][1]
       
        area=l*w
        if l>w:
            length=l
            width=w
        else:
            length=w
            width=l
        area=length*width
      
        
        if  aaa>1000:
            points = cv2.boxPoints(rect)         # Find four vertices of rectangle from above rect
            points = np.int0(np.around(points))     # Round the values and make it integers
            
            # print(type(points))
            # print("x1",points[0][0])
            # print("y1",points[0][1])
            # print("x2",points[1][0])
            # print("y2",points[1][1])
            # print("x3",points[2][0])
            # print("y3",points[2][1])
            # print("x4",points[3][0])
            # print("y4",points[3][1])
            x1=points[0][0]
            y1=points[0][1]
            x2=points[1][0]
            y2=points[1][1]
            x3=points[2][0]
            y3=points[2][1]
            x4=points[3][0]
            y4=points[3][1]
                       
            image = cv2.circle(image, (616, 378), radius=0, color=(0, 0, 255), thickness=5)
#

            
        
            image11= image[int(y2):int(y4),int(x1)+20:int(x3)-20]
            
            # image12= binary[int(y2)+10:int(y4),int(x1)+10:int(x11)]
       
            # cv2.imshow('a1',image11)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

   
          
        
    
    # cv2.imshow('output',image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return image11
    
    
# for filename in os.listdir(folder):
#     image = cv2.imread(os.path.join(folder,filename))
#     a=size_nibble(image)
# Image = cv2.imread("E:/Gherkin/cam0/i27.jpg")
# print(Image)
# a=crop_edge(Image)
# print(a)
# Image = cv2.imread("E:/Gherkin/cam1/j0.jpg")
# b=crop_edge(Image)