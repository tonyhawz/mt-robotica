import cv2 
import numpy as np 
import conf as conf
import camera_utils as cu


route = 'video7.avi'

video = cv2.VideoCapture(route)
video.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, conf.w);
video.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, conf.h);

if not video.isOpened():
    raise RuntimeError('Input file not open')

f, img = video.read()

if not f :
    raise RuntimeError('error de lectura de imagen')

zeros = np.zeros(img.shape,np.uint8)


while True:
    f, img = video.read()
    # Reached end of video
    #print '.'
    if not f:
        video = cv2.VideoCapture(route)
    else:
        old_zeros = zeros 
        zeros = np.zeros(img.shape,np.uint8)
    	img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        img_blur = cv2.GaussianBlur(img, (5, 5), 0)
            
        img_hsv = cv2.cvtColor(img_blur, cv2.COLOR_BGR2HSV)
        img_bw = cv2.inRange(img_hsv, conf.min_hsv_arena,conf.max_hsv_arena)
        img_eroded = cv2.erode(img_bw,cv2.getStructuringElement(cv2.MORPH_RECT,(3,3)))
        img_dilated = cv2.erode(img_eroded,cv2.getStructuringElement(cv2.MORPH_RECT,(10,3)))
        ret,thresh = cv2.threshold(img_dilated,127,255,0)
        contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        mask = np.zeros(img_bw.shape,np.uint8)
        cajas = []
        for cnt in contours:
            rect = cv2.minAreaRect(cnt)
            w,h = rect[1]
            rect = (rect[0],(w*1.5,h*1.5),rect[2])
            box = cv2.cv.BoxPoints(rect)
            box = np.int32(np.around(box))
            #cv2.drawContours(mask,[box],0,255,-1)
            #cv2.drawContours(img,[box],0,255,1)
            cv2.drawContours(img_hsv,[box],0,(255,255,255),-1)
            cajas.append(box)
        #mean = cv2.mean(img,mask = img_bw)
        #mask = cv2.bitwise_not(mask)
        #masked = cv2.bitwise_and(img_hsv,img_hsv,mask=mask)
        #cv2.drawContours(masked,cajas,-1,(255,255,255),-1)
        cv2.drawContours(img_hsv,cajas,-1,(255,255,255),-1) 
        #img_bw = cv2.inRange(masked, conf.min_hsv_negro,conf.max_hsv_negro)
        img_bw = cv2.inRange(img_hsv, conf.min_hsv_negro,conf.max_hsv_negro)
        img_eroded = cv2.erode(img_bw,cv2.getStructuringElement(cv2.MORPH_RECT,(5,5)))
        img_dilated = cv2.erode(img_eroded,cv2.getStructuringElement(cv2.MORPH_RECT,(5,5)))
        ret,thresh = cv2.threshold(img_dilated,127,255,0)
        contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)	
        cv2.drawContours(img,contours,-1,(0,0,0),-1)
        c = contours[0]
        x_old,y_old = (0,0)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 600:
                rect = cv2.minAreaRect(cnt)
                #w,h = rect[1]
                #rect = (rect[0],(w*1.5,h*1.5),rect[2])
                box = cv2.cv.BoxPoints(rect)
                box = np.int32(np.around(box))
                cv2.drawContours(img,[box],0,(0,0,255),1) 
                #cv2.drawContours(zeros,[box],0,(255,255,255),-1)
                cv2.drawContours(zeros,[box],0,255,-1)
                x,y = rect[0]
                if y > y_old :
                    c = box
                    y_old = y
                    x_old = x
        
        mask =  cv2.bitwise_and(zeros,old_zeros)
        #masked = cv2.bitwise_and(img_hsv,img_hsv,mask=mask)
        #ret,thresh = cv2.threshold(masked,127,255,0)
        #contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(img,[c],0,(0,255,0),3)
        v = cv2.waitKey(50) % 0x100
        if v == 27:
            break
        #cv2.imshow("ventana",cu.join_images(img_dilated,masked))
        #cv2.imshow("ventana",cu.join_images(img,masked))
        cv2.imshow("ventana",cu.join_images(img,mask))

