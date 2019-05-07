import cv2
import numpy as np
import  RPi.GPIO as GPIO
import time
PWMA = 18
AIN1   =  22
AIN2   =  27
PWMB = 23
BIN1   = 25
BIN2  =  24
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM)
GPIO.setup(AIN2,GPIO.OUT)
GPIO.setup(AIN1,GPIO.OUT)
GPIO.setup(PWMA,GPIO.OUT)
GPIO.setup(BIN1,GPIO.OUT)
GPIO.setup(BIN2,GPIO.OUT)
GPIO.setup(PWMB,GPIO.OUT)
GPIO.output(AIN2,False)#AIN2
GPIO.output(AIN1,True) #AIN1
GPIO.output(BIN2,False)#BIN2
GPIO.output(BIN1,True) #BIN1
L_Motor= GPIO.PWM(PWMA,100)
R_Motor = GPIO.PWM(PWMB,100)
cap = cv2.VideoCapture(0)
while( cap.isOpened() ):
    center=320
    kernel = np.ones((2,2),np.uint8)
    kernel2 = np.ones((5,5),np.uint8)
    #USB摄像头工作时,读取一帧图像
    ret, frame = cap.read()
    #显示图像窗口在树莓派的屏幕上
    cv2.imshow('frame',frame)
    # 转化为灰度图
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 大津法二值化
    retval, dst = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
    cv2.imshow('dst',dst)
    # 单看第400行的像素值
    color = dst[400]
    # 找到heise的像素点个数
    count = np.sum(color == 0)
    if count != 0:
        index = np.where(color == 0)
        center= (index[0][0]+index[0][count -1])/2
    print(center)
    direction=center-320
    L_Motor.start(40)
    R_Motor.start(40)
    if direction<-70:
        L_Motor.start(10)
        R_Motor.start(50)
    if direction>70:
        L_Motor.start(50)
        R_Motor.start(40)
    if abs(direction)>250:
        L_Motor.start(0)
        R_Motor.start(0) 
    
    #按下q键退出
    key = cv2.waitKey(1)
    #print( '%08X' % (key&0xFFFFFFFF) )
    if key & 0x00FF  == ord('q'):
        break
# 释放资源和关闭窗口
L_Motor.start(0)
R_Motor.start(0) 
cap.release()
cv2.destroyAllWindows()
GPIO.cleanup()

