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


def size(image):
    result='e'
    #image = cv2.imread("E:/Gherkin/1/Cam2/k82.jpg")
    #image = cv2.resize(image, (1000, 1000))
    # image= image[300:900,80:900]
    #image= image[00:1000,0:1200]
    #print(filename)
    # cv2.imshow("image", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
     
    hsv= cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    lower_color = np.array([8,23,0]) #45  #binary detection 12/11/2021
    upper_color = np.array([57,255,255])#70 
    
    binary = cv2.inRange(hsv, lower_color, upper_color)
    #cv2.imshow('binary', binary)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    contours,hierarchy = cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #Dis_count=len(contours)
    
    s=0
    m=0
    l=0
    for cnt in contours:
        hull = cv2.convexHull(cnt)
        aaa=cv2.contourArea(hull)
        rect = cv2.minAreaRect(cnt)             # rect = ((center_x,center_y),(width,height),angle)
        l=rect[1][0]
        w=rect[1][1]
        
        if l>w:
            length=l
            width=w
        else:
            length=w
            width=l
        area=length*width
        # print('length',length) 
        # print('width',width) 
        #print('area',aaa)
        
        #if  length>=100 and length<250 and width<180:
        if aaa>=8000 and aaa<16000:#length>=250 and length<370 and width>=50:
            print(aaa)
            points = cv2.boxPoints(rect)         # Find four vertices of rectangle from above rect
            points = np.int0(np.around(points))     # Round the values and make it integers
            cv2.polylines(image,[points],True,(0,0,255),3)# draw rectangle in red color
            print('SMALL',round(aaa))
            #print("area",aaa)
            l_b=length/width
            #print('l_b',round(l_b,2))
            if l_b<2.3:
                print("CURVED")
                result='C'
            else:
                result='s'
            
            
            #print('length',length) 
            #print('width',width)
            
            s+=1
        #elif length>=250 and length<370 and width>=50:  
        #elif length>=250 and length<370 and width>=50:
        elif aaa>=16000 and aaa<31000:#length>=370 and length<500 and width>=50:
            print(aaa)
            points = cv2.boxPoints(rect)         # Find four vertices of rectangle from above rect
            points = np.int0(np.around(points))     # Round the values and make it integers
            cv2.polylines(image,[points],True,(0,255,0),3)# draw rectangle in green color
            print('MEDIUM',round(aaa))
            #print("area",aaa)
            l_b=length/width
            print('l_b',round(l_b,2))
            if l_b<2.3:
                print("CURVED")
                result='C'
            else:
                result='m'
            #print('length',length) 
            #print('width',width)
            m+=1
        
        #elif length>=370 and length<2000 and width>=50:
        elif aaa>=31000 and aaa<=1000000:#length>=500 and length<2000 and width>=50:
            print(aaa)
            points = cv2.boxPoints(rect)         # Find four vertices of rectangle from above rect
            points = np.int0(np.around(points))     # Round the values and make it integers
            cv2.polylines(image,[points],True,(255,0,0),3)# draw rectangle in blue color
            print('LARGE',round(aaa))
            #print("area",aaa)
            l_b=length/width
            #print('l_b',round(l_b,2))
            if l_b<2.3:
                print("CURVED")
                result='C'
            else:
                result='l'
            #print('length',length) 
            #print('width',width)
            l+=1    
                
        else:
                pass
      
    
    #cv2.imshow('output',image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return result
    
#folder="C:/Users/DELL/Desktop/30 minus 19.11/good_30minus/cam1"    
#for filename in os.listdir(folder):
#    image = cv2.imread(os.path.join(folder,filename))
#     a=size(image)
# Image = cv2.imread("E:/Gherkin/cam1/j30.jpg")
# a=size(Image)
# print(a)
