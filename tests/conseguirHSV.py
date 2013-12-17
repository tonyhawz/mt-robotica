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

#configuracion, captura de camara o archivo.
captureFromCam = True
fileName = "capture2.jpg" # Usado en caso que captureFromCam sea False
cameraId = 1 # Usado en caso que captureFromCam sea True

#Cuando se estรกn calibrando colores con Hue cercano a 0, por ejemplo rojo. Por defecto, dejar en False
#Si estรก en true, la discontinuidad del hue se mueve a los 90 grados.
hueNearZero = False

#Variables
x_co = 0
y_co = 0
dragging = False
#minHSV = list((0, 4, 23))
#maxHSV = list((174, 205, 83))

minHSV = list((0, 100, 100))
maxHSV = list((100, 2, 54))

#min_hsv_arena = np.array((0, 100, 100), np.int32)
#max_hsv_arena = np.array((100, 224, 256), np.int32)

def on_mouse(event,x,y,flag,param):
  global x_co
  global y_co
  global dragging
  global minHSV
  global maxHSV
  x_co=x
  y_co=y
  if event == cv.CV_EVENT_LBUTTONDOWN:
      dragging = True
  if event == cv.CV_EVENT_LBUTTONUP:
      dragging = False
      print("minHSV",minHSV)
      print("maxHSV",maxHSV)
  if event == cv.CV_EVENT_RBUTTONDOWN:
    minHSV = None
    maxHSV = None
#----------------#----------------#----------------#----------------#----------------
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



cv.NamedWindow("camera", 0)
if captureFromCam:
  capture = cv.CaptureFromCAM(cameraId)
font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 0.5, 1, 0, 2, 8)
cv.SetMouseCallback("camera",on_mouse, 0);
while True:
    if captureFromCam:
      src = cv.QueryFrame(capture)
    else:
      src = cv.LoadImageM(fileName, True)
    cv.Smooth(src, src, cv.CV_BLUR, 3)
    hsv = cv.CreateImage(cv.GetSize(src), 8, 3)
    cv.CvtColor(src, hsv, cv.CV_BGR2HSV)
    if dragging:
      s=list(cv.Get2D(hsv,y_co,x_co))
      if hueNearZero and s[0] > 90:
        s[0] = s[0] - 180
      print "H:",s[0],"      S:",s[1],"       V:",s[2]
      if(minHSV == None):
        minHSV = list((s[0],s[1],s[2]))
        maxHSV = list((s[0],s[1],s[2]))
      for i in range(3):
        if s[i] < minHSV[i]:
          minHSV[i] = s[i]
        if s[i] > maxHSV[i]:
          maxHSV[i] = s[i]

    if minHSV != None:
      hsv = thresholdImage(hsv,minHSV[0],maxHSV[0],minHSV[1],maxHSV[1],minHSV[2],maxHSV[2])
      cv.ShowImage("threshold", hsv)

    cv.ShowImage("camera", src)
    if cv.WaitKey(1) == 27:
        break