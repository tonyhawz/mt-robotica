import cv2
import numpy as np
from keys import keys
import camera_utils as cu
import conf as conf
import re
import sys
import getopt

class Parametros() :

    def __init__(self):
        pass
    def update(self,v):
        if v == keys.ESC :
            return False
        elif v != -1 and v != 255:
            print v
        return True

def callback_trackbar(value):
    pass

def set_minmax_hsv():
    cv2.setTrackbarPos('min_H','ventana',conf.min_hsv_negro[0])
    cv2.setTrackbarPos('min_S','ventana',conf.min_hsv_negro[1])
    cv2.setTrackbarPos('min_V','ventana',conf.min_hsv_negro[2])
    cv2.setTrackbarPos('max_H','ventana',conf.max_hsv_negro[0])
    cv2.setTrackbarPos('max_S','ventana',conf.max_hsv_negro[1])
    cv2.setTrackbarPos('max_V','ventana',conf.max_hsv_negro[2])

def get_minmax_hsv():
    min_h = cv2.getTrackbarPos("min_H", "ventana")
    max_h = cv2.getTrackbarPos("max_H", "ventana")
    min_s = cv2.getTrackbarPos("min_S", "ventana")
    max_s = cv2.getTrackbarPos("max_S", "ventana")
    min_v = cv2.getTrackbarPos("min_V", "ventana")
    max_v = cv2.getTrackbarPos("max_V", "ventana")
    min_hsv = np.array((min_h,min_s,min_v),np.int32)
    max_hsv = np.array((max_h,max_s,max_v),np.int32)
    return (min_hsv,max_hsv)

route = ''
try:
    opts, args = getopt.getopt(sys.argv[1:], "hi:o:", ["ifile=", "ofile="])
except getopt.GetoptError:
    print ('error')
    sys.exit(2)
for opt, arg in opts:
    if opt == '-i':
        numerico = re.compile("[0-9]").match(arg)
        if numerico:
            route = int(arg)
        else:
            route = arg
if (route == ''):
    print ('falta camara, saliendo')
    sys.exit(2)


#route = './2013-06-02-131200.webm'
#route = '../video-2013-07-09-1373413843.avi'
#route = 'video-1378341835.58.avi'
#route = 'video7.avi'
#route = 'video2.avi'
#route = 'video3.avi'
#route = 1

video = cv2.VideoCapture(route)
video.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 160);
video.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 120);

if not video.isOpened():
    raise RuntimeError('no se pudo abrir el video')

p = Parametros()

cv2.namedWindow("ventana");
cv2.createTrackbar("min_H", "ventana", 0, 256,   callback_trackbar);
cv2.createTrackbar("max_H", "ventana", 256, 256, callback_trackbar);
cv2.createTrackbar("min_S", "ventana", 0, 256,   callback_trackbar);
cv2.createTrackbar("max_S", "ventana", 256, 256, callback_trackbar);
cv2.createTrackbar("min_V", "ventana", 0, 256,   callback_trackbar);
cv2.createTrackbar("max_V", "ventana", 256, 256, callback_trackbar);

set_minmax_hsv()

while True:
    f, img = video.read()
    # Reached end of video
    #print '.'
    if not f:
        video = cv2.VideoCapture(route)
    else:
        minhsv,maxhsv = get_minmax_hsv()
        img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        img_blur = cv2.GaussianBlur(img, (5, 5), 0)
        img_hsv = cv2.cvtColor(img_blur, cv2.COLOR_BGR2HSV)
        img_bw = cv2.inRange(img_hsv, minhsv,maxhsv)

        #element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
        #element = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
        element = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
        img_eroded = cv2.erode(img_bw,element)
        img_dilated = cv2.erode(img_eroded,cv2.getStructuringElement(cv2.MORPH_RECT,(5,5)))

        ret,thresh = cv2.threshold(img_dilated,127,255,0)
        contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(img,contours,-1,(0,255,0),1)
        # print '-------------------------------------------------------'
        for cnt in contours:
            area = cv2.contourArea(cnt)
            #print area
            if area > 500:
                rect = cv2.minAreaRect(cnt)
                # print rect
                w,h = rect[1]
                aspect_ratio = float(w)/h
                # print aspect_ratio
                if aspect_ratio >  .1:
                    box = cv2.cv.BoxPoints(rect)
                    box = np.int32(np.around(box))
                    cv2.drawContours(img,[box],0,(0,0,255),1)
                    #cv2.polylines(img,[box],True,(255,0,0),2)
                    #x,y,w,h = cv2.boundingRect(cnt)
                    #cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        v = cv2.waitKey(50) % 0x100
        if not p.update(v):
            break
        cv2.imshow("ventana",cu.join_images(img,img_dilated))

print p.mins
print p.maxs
print 'fin'

