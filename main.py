import numpy as np
import cv2

import serial
import pymodbus
from pymodbus.pdu import ModbusRequest
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.transaction import ModbusRtuFramer
import time

###############################
import mysql
import mysql.connector    
mydb = mysql.connector.connect(host='127.0.0.1',user = "root",password = "123456",database = "gherkin")
mycursor = mydb.cursor()
mycursor.execute("SELECT z FROM gherkin_table")               
myresult = mycursor.fetchall()
size_sel=int(myresult[0][0])

##### mv ##################################

import cam0
import cam1
import cam2
import thirty_plus
import thirty_minus
##############################################
cap0 = cv2.VideoCapture(2)
# cap0.set(cv2.CAP_PROP_AUTO_WB,1.0)
 # cap0.set(3,1280)
# cap0.set(4,720)
print("C0")
cap1 = cv2.VideoCapture(1)
# cap1.set(3,1280)
# cap1.set(4,720)
print("C1")
cap2 = cv2.VideoCapture(0)
# cap2.set(3,1280)
# cap2.set(4,720)

print("C2")
i=0
j=0
k=0
###############################################

  
client = ModbusClient (method='ascii',port='COM3',parity="E",stopbits=1,bytesize=7,baudrate=9600,timeout=5000)
client.connect()

  
      
client.write_register(6400, 8, unit=1)	#Gate 1 Delay , 18
client.write_register(6401, 15, unit=1)	#Gate 2 Delay 
client.write_register(6402, 20, unit=1)	#Gate 3 delay
client.write_register(6403, 25, unit=1)	#Gate 1 Delay 
# client.write_register(6404, 46, unit=1)	#Gate 2 Delay 
client.write_register(6405, 32, unit=1)	#Gate 3 delay Not used[]


client.write_register(6406, 5, unit=1)	#Gate Open TIme
client.write_register(4116, 100, unit=1)	#Image Capture Delay
client.write_register(4097,5, unit=1)   #Delay for sensor sginal



time.sleep(1)
Left_out=0   
Right_out=0
var=0
skip_first_capture=0
print("IN While")

while True:
       
    
    if (True):
        try: 
            Result_St_Analysis = client.read_coils(2348,1, unit=0x01)		#START CAPTURE IF RESULT IS TRUE
            St_Analysis = str((Result_St_Analysis .bits[0]))
        except:
            pass
                
        '''try:
            Delete_images.Delete_All_Images()
        except:
            pass'''
        if skip_first_capture==0:
            
            start=time.time()
            ret0, frame0 = cap0.read()
            ret1, frame1 = cap1.read()
            ret2, frame2 = cap2.read()
            end=time.time()
            #print(frame0)
            #print("time",end-start)
            i=0
            j=0
            k=0
            skip_first_capture=1
        if St_Analysis== "True": 
            #print(i)
            #print("if_st_analysis")
            start=time.time()
            #Capture
           
            ret0, frame0 = cap0.read()
            ret1, frame1 = cap1.read()
            ret2, frame2 = cap2.read()

            cv2.imwrite('E:/Gherkin/cam0/i%d.jpg'%i,frame0)
            cv2.imwrite('E:/Gherkin/cam1/j%d.jpg'%j,frame1)
            cv2.imwrite('E:/Gherkin/cam2/k%d.jpg'%k,frame2)
            
            
            Image0 = cv2.imread("E:/Gherkin/cam0/i"+str(i)+".jpg")
            Image1 = cv2.imread("E:/Gherkin/cam1/j"+str(j)+".jpg")
            Image2 = cv2.imread("E:/Gherkin/cam2/K"+str(k)+".jpg")
            i+=1
            j+=1
            k+=1
            ####################################################
            #image processing
            #print(Image0)
            #print('a' )
            
        
            if size_sel==1:
                size_r=thirty_plus.size(Image1)
            else:
                size_r=thirty_minus.size(Image1)
                
            if size_r=='C':
              
                import mysql.connector
                mydb = mysql.connector.connect(host='127.0.0.1',user = "root",password = "123456",database = "gherkin")
                mycursor = mydb.cursor()                                        
                command=  "UPDATE gherkin_table SET f =f+1" 
                mycursor.execute(command)
                mydb.commit()
                print('Result =  C')
                client.write_register(4096,3, unit=1)
                client.write_coils(2349, [True]*1, unit=1)
            else:
                try:
                    
                    result0=cam0.Infested(Image0,0)
                except:
                    result0='G'
                try:
                    result1=cam1.Infested(Image1,1)
                except:
                    result1='G'  
                try:
                    result2=cam2.Infested(Image2,2)
                except:
                    result2='G'                
                
                
                print(result0,result1,result2)
                
                if result0=='M' or result1=='M' or result2=='M':
                        import mysql.connector
                        mydb = mysql.connector.connect(host='127.0.0.1',user = "root",password = "123456",database = "gherkin")
                        mycursor = mydb.cursor()                                        
                        command=  "UPDATE gherkin_table SET e =e+1" 
                        mycursor.execute(command)
                        mydb.commit()
                        print('Result =  M')
                        client.write_register(4096,1, unit=1)
                        client.write_coils(2349, [True]*1, unit=1)
                elif result0=='I' or result1=='I' or result2=='I':
                        import mysql.connector
                        mydb = mysql.connector.connect(host='127.0.0.1',user = "root",password = "123456",database = "gherkin")
                        mycursor = mydb.cursor()                                        
                        command=  "UPDATE gherkin_table SET d =d+1" 
                        mycursor.execute(command)
                        mydb.commit()
                        print('Result =  I')
                        client.write_register(4096,1, unit=1)
                        client.write_coils(2349, [True]*1, unit=1)
    
                elif result0=='G' or result1=='G' or result2=='G':
                    if size_sel==1:
                        size_r=thirty_plus.size(Image1)
                    else:
                        size_r=thirty_minus.size(Image1)
                    #size_r=thirty_minus.size(Image1)
                    # if size_r=='C' :
                    #    import mysql.connector
                    #    mydb = mysql.connector.connect(host='127.0.0.1',user = "root",password = "123456",database = "gherkin")
                    #    mycursor = mydb.cursor()                                        
                    #    command=  "UPDATE gherkin_table SET f =f+1" 
                    #    mycursor.execute(command)
                    #    mydb.commit()
                    #    print('Result =  C')
                    #    client.write_register(4096,3, unit=1)
                    #    client.write_coils(2349, [True]*1, unit=1)
                    if size_r=='s' :
                          import mysql.connector
                          mydb = mysql.connector.connect(host='127.0.0.1',user = "root",password = "123456",database = "gherkin")
                          mycursor = mydb.cursor()                                        
                          command=  "UPDATE gherkin_table SET c =c+1" 
                          mycursor.execute(command)
                          mydb.commit()
                          print('Result =  Gs')
                          client.write_register(4096,4, unit=1)
                          client.write_coils(2349, [True]*1, unit=1)
                    elif size_r=='m' :
                            import mysql.connector
                            mydb = mysql.connector.connect(host='127.0.0.1',user = "root",password = "123456",database = "gherkin")
                            mycursor = mydb.cursor()                                        
                            command=  "UPDATE gherkin_table SET b =b+1" 
                            mycursor.execute(command)
                            mydb.commit()
                            print('Result =  Gm')
                            #client.write_register(4096,5, unit=1)
                            #client.write_coils(2349, [True]*1, unit=1)
                    elif size_r=='l' :
                            import mysql.connector
                            mydb = mysql.connector.connect(host='127.0.0.1',user = "root",password = "123456",database = "gherkin")
                            mycursor = mydb.cursor()                                        
                            command=  "UPDATE gherkin_table SET a =a+1" 
                            mycursor.execute(command)
                            mydb.commit()
                            print('Result =  Gl')
                            client.write_register(4096,6, unit=1)
                            client.write_coils(2349, [True]*1, unit=1)
                    else:
                        #print("CCCCCCCCCCCCCC")
                        pass
                else:
                    pass
            
            
                
                

            ############################################################
           
            end=time.time()
            
            print(end-start)
            try:
                
                time.sleep(0.3-(end-start))
            except:
                pass
                #print("A")
            # client.write_register(4096,1, unit=1)	
            # client.write_coils(2349, [True]*1, unit=1)
            client.write_coils(2148, [False]*1, unit=1)
            
            time.sleep(0.1)
            # print("as")
cap0.release()
cap1.release()
cap2.release()         
client.close()
