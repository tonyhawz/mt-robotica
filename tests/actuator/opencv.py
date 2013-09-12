#! /usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import numpy as np
import matplotlib.pyplot as plt

def diffImg(t0, t1, t2):
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1, t0)
    return cv2.bitwise_and(d1, d2)


def testDiff():
    cam = cv2.VideoCapture(0)
    winName = "Movement Indicator"
    cv2.namedWindow(winName, cv2.CV_WINDOW_AUTOSIZE)
    
    # Read three images first:
    t_minus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
    t = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
    t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
    
    while True:
        cv2.imshow( winName, diffImg(t_minus, t, t_plus) )
        # Read next image
        t_minus = t
        t = t_plus
        t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
        #key = cv2.waitKey(10)
        #if key == 27:
        if cv2.waitKey(10) == 27:
            cv2.destroyWindow(winName)
            break
    
    print "Goodbye"

def draw_hist(img):
    fig = plt.figure()
    ax = fig.add_subplot(3,1,1)
    ax.set_title('H')
    hist_hue = cv2.calcHist([img], [0], None, [180], [0,180])
    ax.plot(hist_hue)

    ax = fig.add_subplot(3,1,2)
    ax.set_title('S')
    hist_hue = cv2.calcHist([img], [1], None, [256], [0,255])
    ax.plot(hist_hue)

    ax = fig.add_subplot(3,1,3)
    ax.set_title('V')
    hist_hue = cv2.calcHist([img], [2], None, [256], [0,255])
    ax.plot(hist_hue)

    plt.show()

def testCam():
    winName = "Movement Indicator"
    cv2.namedWindow(winName, cv2.CV_WINDOW_AUTOSIZE)
    cam = cv2.VideoCapture(0)
    
    # OpenCV uses 0-180 for hue values - green is ~50
    #min_green = np.array([30,50,50])
    #max_green = np.array([70,256,250])
    min_green = np.array((0.,0.,0.))
    max_green = np.array((180.,180.,50.))
    
    ok, img = cam.read() 
    # Blur it
    if ok:
        img_blur = cv2.GaussianBlur(img, (5, 5), 0)
        # Convert to HSV
        img_hsv = cv2.cvtColor(img_blur, cv2.COLOR_BGR2HSV)
        # Show HSV histograms
        #draw_hist(img_hsv)
        
        while True:      
            img_green_bw = cv2.inRange(img_hsv, min_green, max_green)
            
            cv2.imshow(winName,img_green_bw)
            
            ok, img = cam.read() 
            
            img_blur = cv2.GaussianBlur(img, (5, 5), 0)
            # Convert to HSV
            img_hsv = cv2.cvtColor(img_blur, cv2.COLOR_BGR2HSV)
            
            if (cv2.waitKey (5) != -1):
                cv2.destroyWindow(winName)
                break;    
        else :
            print "not ok"

testCam()

