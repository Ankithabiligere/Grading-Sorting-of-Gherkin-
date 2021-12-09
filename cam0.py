
import time
import cv2
import numpy as np
import os
import crop_edge
def Infested(image,cam_sel):
     start=time.time()
     # image = cv2.resize(image, (1280, 1000))
     # cv2.imshow("image1",image)
     cv2.waitKey(0)
     cv2.destroyAllWindows()
     if cam_sel==0:
         
         # image= image[20:350, 100:1000]
         image= image[25:265, 70:620]
     elif cam_sel==1:
         image= image[40:350, 0:500]#[50:650, 0:1200]
     else:
         image= image[10:185, 50:550]
        
     image=crop_edge.crop_edge(image)
     # cv2.imshow("image",image)
     cv2.waitKey(0)
     cv2.destroyAllWindows()
     
     brightness =150
     contrast =200
     image = np.int16(image)
     image = image * (contrast/127+1) - contrast + brightness
     image = np.clip(image, 0, 255)
     image = np.uint8(image) 
     kernel = np.ones((3,3),np.uint8)
     copy=image.copy()
     
     hsv= cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
     lower_color1 = np.array([10,0,0]) #light brown detection 16/11/2021
     upper_color1 = np.array([25,150,150])
     lower_color2 = np.array([0,162,0]) #9  #brown defects detection 16/11/2021
     upper_color2 = np.array([28,255,177])
     lower_color3 = np.array([0,255,88]) #9  #brown defects detection 16/11/2021
     upper_color3 = np.array([28,255,148])
     lower_color4 = np.array([0,95,250]) #9  #very light brown defects detection 19/11/2021
     upper_color4 = np.array([28,103,255])  
                                   
     brown = cv2.inRange(hsv, lower_color1, upper_color1)
     black = cv2.inRange(hsv, lower_color2, upper_color2)
     black1 = cv2.inRange(hsv, lower_color3, upper_color3)
     brown1 = cv2.inRange(hsv, lower_color4, upper_color4)
    
     mask=brown+black1+black+brown1
     # cv2.imshow("mask",mask)
     cv2.waitKey(0)
     cv2.destroyAllWindows()
     
     
     contours,hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
     q=0
     for cnt in contours:
         hull = cv2.convexHull(cnt)
         aaa=cv2.contourArea(hull)
       
         rect = cv2.minAreaRect(cnt)             # rect = ((center_x,center_y),(width,height),angle)
         l=rect[1][0]
         w=rect[1][1]
         area=l*w
         #print (aaa)

         if aaa>=3:
             points = cv2.boxPoints(rect)         # Find four vertices of rectangle from above rect
             points = np.int0(np.around(points))     # Round the values and make it integers
             # cv2.polylines(image,[points],True,(0,255,2),2)# draw rectangle in red color
             # cv2.putText(image, "T{}".format(q),(int(rect[0][0]),int(rect[0][1])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 200, 255), 2)
             q+=1
            
            
         else:
             pass
              
        
     end=time.time()
    #print(end-start)
         
     # cv2.imshow('Infested Gherkin',image)
     cv2.waitKey(0)
     cv2.destroyAllWindows()
     if q>0 and q<3:         
         camera0='I'
         # print("D")
     elif q>2:
         camera0='M'
         # print("M")
     else:
         camera0='G'
         # print("G") 
          
    
     

     
     return camera0
# s=time.time()

# Image = cv2.imread("E:/Gherkin/cam0/i0.jpg")
# a=Infested(Image,0)
# Image = cv2.imread("E:/Gherkin/cam1/j0.jpg")
# b=Infested(Image,1)
# Image = cv2.imread("E:/Gherkin/cam2/k0.jpg")
# c=Infested(Image,2) 
# print(a,b,c) 
# e=time.time()
# print(e-s)  
