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


#huadongtiao
trackbar_name7="Blur"#降噪
trackbar_name1="interation_dialte"#膨胀迭代次数
trackbar_name2="dilationSize"#膨胀核大小
trackbar_name3="interation_erode"#侵蚀迭代次数
trackbar_name4="erodeSize"#侵蚀核大小
trackbar_name5="threshold"#二值化阈值
trackbar_name6="choose_line"#所取行
win_name="TrackbarDemo"#图像处理

max_num7 = 10
max_num1 = 10
max_num2 = 5
max_num3 = 10
max_num4 = 5
max_num5 = 255
max_num6 = 479

blur_size=3
dialte_value=0
dialte_size = 0
erode_value=0
erode_size = 0
threshold_value=75
line_value=400

win_name2="SpeedControl"
track1="average_speed"
track2="turn_le_speed"
track3="turn_ri_speed"
track4="sensitivity"

max_t1 = 100
max_t2 = 100
max_t3 = 100
max_s1 = 70
asvalue = 30
tlvalue = 40
trvalue = 40
sevalue = 10
def on_control(arg):
    print('average speed',cv2.getTrackbarPos(track1,win_name2))
    print('turn_le_speed',cv2.getTrackbarPos(track2,win_name2))
    print('turn_ri_speed',cv2.getTrackbarPos(track3,win_name2))
    print('sensitivity',cv2.getTrackbarPos(track4,win_name2))
def on_blur(arg):
    return cv2.getTrackbarPos(trackbar_name7,win_name)*2+1
def on_run(arg):
    # 单看第400行的像素值
    color = res[cv2.getTrackbarPos(trackbar_name6,win_name)]
    # 找到像素点个数
    choose=255
    count = np.sum(color == choose)
    if count != 0:
        index = np.where(color == choose)
        center= (index[0][0]+index[0][count -1])/2
    print(center)
    
def on_threshold(arg):
    value = cv2.getTrackbarPos(trackbar_name5,win_name)
    retval, dst = cv2.threshold(gray, value, 255, cv2.THRESH_OTSU)
def on_erode_and_dialte(arg):
    value2 = cv2.getTrackbarPos(trackbar_name3,win_name)
    size2 = cv2.getTrackbarPos(trackbar_name4,win_name)
    kerner12=cv2.getStructuringElement(cv2.MORPH_RECT,(2*size2+1,2*size2+1))
    res = cv2.erode(dst,kerner12,None,None,value2)
    value1 = cv2.getTrackbarPos(trackbar_name1,win_name)
    size1 = cv2.getTrackbarPos(trackbar_name2,win_name)
    kerner11=cv2.getStructuringElement(cv2.MORPH_RECT,(2*size1+1,2*size1+1))   
    res = cv2.dilate(res,kerner11,None,None,value1)
    cv2.imshow(win_name,res)



cv2.namedWindow(win_name)
cv2.createTrackbar(trackbar_name7,win_name,blur_size,max_num7,on_blur)
cv2.createTrackbar(trackbar_name1,win_name,dialte_value,max_num1,on_erode_and_dialte)
cv2.createTrackbar(trackbar_name2,win_name,dialte_size,max_num2,on_erode_and_dialte)
cv2.createTrackbar(trackbar_name3,win_name,erode_value,max_num3,on_erode_and_dialte)
cv2.createTrackbar(trackbar_name4,win_name,erode_size,max_num4,on_erode_and_dialte)
cv2.createTrackbar(trackbar_name5,win_name,threshold_value,max_num5,on_threshold)
cv2.createTrackbar(trackbar_name6,win_name,line_value,max_num6,on_run)

cv2.namedWindow(win_name2)
cv2.createTrackbar(track1,win_name2,asvalue,max_t1,on_control)
cv2.createTrackbar(track2,win_name2,tlvalue,max_t2,on_control)
cv2.createTrackbar(track3,win_name2,trvalue,max_t3,on_control)
cv2.createTrackbar(track4,win_name2,sevalue,max_s1,on_control)

while( cap.isOpened() ):
    center=320
    #USB摄像头工作时,读取一帧图像
    ret, frame = cap.read()
    #显示图像窗口在树莓派的屏幕上
    #cv2.imshow('frame',frame)
    # 转化为灰度图
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 大津法二值化
    value = cv2.getTrackbarPos(trackbar_name5,win_name)
    retval, dst = cv2.threshold(gray, value, 255, cv2.THRESH_BINARY)
    dst=cv2.medianBlur(dst,on_blur(0))
    #膨胀侵蚀
    value2 = cv2.getTrackbarPos(trackbar_name3,win_name)
    size2 = cv2.getTrackbarPos(trackbar_name4,win_name)
    kerner12=cv2.getStructuringElement(cv2.MORPH_RECT,(2*size2+1,2*size2+1))
    res = cv2.erode(dst,kerner12,None,None,value2)
    
    value1 = cv2.getTrackbarPos(trackbar_name1,win_name)
    size1 = cv2.getTrackbarPos(trackbar_name2,win_name)
    kerner11=cv2.getStructuringElement(cv2.MORPH_RECT,(2*size1+1,2*size1+1))   
    res = cv2.dilate(res,kerner11,None,None,value1)
    cv2.imshow(win_name,res)
    #按下w键退出
    key = cv2.waitKey(1)
    #print( '%08X' % (key&0xFFFFFFFF) )
    if key & 0x00FF  == ord('w'):
        break
while( cap.isOpened() ):
    center=320
    #USB摄像头工作时,读取一帧图像
    ret, frame = cap.read()
    #显示图像窗口在树莓派的屏幕上
    #cv2.imshow('frame',frame)
    # 转化为灰度图
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # 大津法二值化
    value = cv2.getTrackbarPos(trackbar_name5,win_name)
    retval, dst = cv2.threshold(gray, value, 255, cv2.THRESH_BINARY)
    dst=cv2.medianBlur(dst,on_blur(0))
    #膨胀侵蚀
    value2 = cv2.getTrackbarPos(trackbar_name3,win_name)
    size2 = cv2.getTrackbarPos(trackbar_name4,win_name)
    kerner12=cv2.getStructuringElement(cv2.MORPH_RECT,(2*size2+1,2*size2+1))
    res = cv2.erode(dst,kerner12,None,None,value2)
    
    value1 = cv2.getTrackbarPos(trackbar_name1,win_name)
    size1 = cv2.getTrackbarPos(trackbar_name2,win_name)
    kerner11=cv2.getStructuringElement(cv2.MORPH_RECT,(2*size1+1,2*size1+1))   
    res = cv2.dilate(res,kerner11,None,None,value1)
    cv2.imshow(win_name,res) 

    #run
    # 单看第400行的像素值
    color = res[cv2.getTrackbarPos(trackbar_name6,win_name)]
    # 找到heise的像素点个数
    choose=0
    count = np.sum(color == choose)
    if count != 0:
        index = np.where(color == choose)
        center= (index[0][0]+index[0][count -1])/2
    print('center',center)
    direction=(center-320)/4
    print('direction',direction)
    L_Motor.start(cv2.getTrackbarPos(track1,win_name2))
    R_Motor.start(cv2.getTrackbarPos(track1,win_name2))
    if direction<-cv2.getTrackbarPos(track4,win_name2):
        print('Left')
        L_Motor.start(cv2.getTrackbarPos(track1,win_name2))
        R_Motor.start(cv2.getTrackbarPos(track2,win_name2))
    if direction>cv2.getTrackbarPos(track4,win_name2):
        print('Right')
        L_Motor.start(cv2.getTrackbarPos(track3,win_name2))
        R_Motor.start(cv2.getTrackbarPos(track1,win_name2))
        if abs(direction)>100 or direction == 0:
        print('Stop')
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
