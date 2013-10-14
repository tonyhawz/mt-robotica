#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Calibrador de colores basado en HSV
#
# Obtener HSV maximo y minimo de pixeles clickeados
# Ademรกs hace un threshold para mostrar lo que se selecciona con el rango
# ATENCION: Tener en cuenta que el color rojo es un hue aproximado de 0. Si es menor, los valores retornados pasan por la discontinuidad del hue, retornando un valor aproximado a 180 (maximo hue de opencv).
#           Para este caso se puede correr la discontinuidad de los 180 a los 90 grados, cambiando la variable hueNearZero a true.
#
# Se puede usar con la cรกmara o una imagen.


import cv
import time

cameraId = 1
minHSV = list((0, 100, 100))
maxHSV = list((100, 2, 54))


#Retorna una imagen binaria con los pixeles que cumplen la condicion de los parametros
def thresholdImage(img_hsv, minHue = 0 , maxHue = 180, minSaturation = 0 , maxSaturation = 255, minValue = 0 , maxValue = 255):
  # filtrar por rango:
  thresholded_img =  cv.CreateImage(cv.GetSize(img_hsv), 8, 1)

  # HSV stands for hue, saturation, and value
  cv.InRangeS(img_hsv, (minHue, minSaturation, minValue), (maxHue, maxSaturation, maxValue), thresholded_img)

  if(minHue < 0 ):
    # Si minHue es menor a cero, se calcula 2 veces, uno para valores de hue entre [minHue,maxHue] y otro entre [180+minHue,180]
    thresholded_img2 =  cv.CreateImage(cv.GetSize(img_hsv), 8, 1)

    cv.InRangeS(img_hsv, (180 + minHue, minSaturation, minValue), (180, maxSaturation, maxValue), thresholded_img2)
    cv.Add(thresholded_img,thresholded_img2,thresholded_img) # para imprimir

  return thresholded_img
#----------------#----------------#----------------#----------------#----------------

def onTrackbarSlideMinH(pos):
    minHSV[0]= pos

def onTrackbarSlideMinS(pos):
    minHSV[1]= pos

def onTrackbarSlideMinV(pos):
    minHSV[2]= pos

def onTrackbarSlideMaxH(pos):
    maxHSV[0]= pos

def onTrackbarSlideMaxS(pos):
    maxHSV[1]= pos

def onTrackbarSlideMaxV(pos):
    maxHSV[2]= pos


cv.NamedWindow("camera", 0)
capture = cv.CaptureFromCAM(cameraId)
font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 0.5, 1, 0, 2, 8)
#cv.SetMouseCallback("camera",on_mouse, 0);
frames = long(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_COUNT))
if (frames != 0):
    cv.CreateTrackbar("minH", "camera", 0,255, onTrackbarSlideMinH)
    cv.CreateTrackbar("maxH", "camera", 0,255, onTrackbarSlideMaxH)
    cv.CreateTrackbar("minS", "camera", 0,255, onTrackbarSlideMinS)
    cv.CreateTrackbar("maxS", "camera", 0,255, onTrackbarSlideMaxS)
    cv.CreateTrackbar("minV", "camera", 0,255, onTrackbarSlideMinV)
    cv.CreateTrackbar("maxV", "camera", 0,255, onTrackbarSlideMaxV)
salir = False
while not salir:
    src = cv.QueryFrame(capture)
    cv.Smooth(src, src, cv.CV_BLUR, 3)
    hsv = cv.CreateImage(cv.GetSize(src), 8, 3)
    cv.CvtColor(src, hsv, cv.CV_BGR2HSV)
    #if dragging:
      #s=list(cv.Get2D(hsv,y_co,x_co))
      #if hueNearZero and s[0] > 90:
        #s[0] = s[0] - 180
      #print "H:",s[0],"      S:",s[1],"       V:",s[2]
      #if(minHSV == None):
        #minHSV = list((s[0],s[1],s[2]))
        #maxHSV = list((s[0],s[1],s[2]))
      #for i in range(3):
        #if s[i] < minHSV[i]:
          #minHSV[i] = s[i]
        #if s[i] > maxHSV[i]:
          #maxHSV[i] = s[i]
    print "H:",minHSV[0],"      S:",minHSV[1],"       V:",minHSV[2]
    #if minHSV != None:
      #hsv = thresholdImage(hsv,minHSV[0],maxHSV[0],minHSV[1],maxHSV[1],minHSV[2],maxHSV[2])
      #cv.ShowImage("threshold", hsv)
    hsv = thresholdImage(hsv,minHSV[0],maxHSV[0],minHSV[1],maxHSV[1],minHSV[2],maxHSV[2])
    cv.ShowImage("threshold", hsv)

    cv.ShowImage("camera", src)
    #print cv.WaitKey(1)
    if cv.WaitKey(1) == 1048603:
        salir = True