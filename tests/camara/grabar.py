import cv2
import cv2.cv as cv 
import os
import time

i_cam = 1

#cmd = "/usr/bin/uvcdynctrl --device=video"+str(i_cam)+" -s 'White Balance Temperature, Auto' 0"
#print cmd
#os.system(cmd)


camera = cv2.VideoCapture(i_cam)
#video  = cv2.VideoWriter('video.avi', -1, 25, (640, 480));
#video = cv2.VideoWriter()
#video.open('video.avi',-1,25,(640,480))

frame_size = (640,480)
filename = "video-" + str(time.time()) + ".avi"
codecid = "XVID"
#codecid = "DIVX"
#codecid = "FLV1"
#codecid = 'I420'
#codecid = 'IYUV'
#codecid = 'MJPG'
codec = cv2.cv.FOURCC(*codecid)
#print codec

writer = cv2.VideoWriter(filename, codec, 10, frame_size)
#video = cv2.VideoWriter(filename, -1, 10, frame_size)
#video = cv2.VideoWriter(filename,cv2.CV_FOURCC_PROMPT, 10, frame_size)
#writer = cv2.VideoWriter(filename,cv.CV_FOURCC('i','Y', 'U', 'V'),15, frame_size)

# Check OpenCV was able to open the video
if not writer.isOpened():
    raise RuntimeError('Output file not open')
while True:
    f,img = camera.read()
    img = cv2.resize(img, (640,480))
    writer.write(img)
    cv2.imshow("webcam",img)
    if (cv2.waitKey(5) != -1):
        break

writer.release() 



