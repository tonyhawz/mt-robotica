import numpy as np 

refresh_rate = .01

# variables de configuracion para la camara
#camara      = -1
camara = 'video-2013-07-09-1373414462.avi'

ancho       = 160
alto        = 120

# variables para el control de la posicion de la latita
min_area    = 200
area_lata   = 1000000
min_x       = (ancho / 2.0) - (ancho / 10.0)
max_x       = (ancho / 2.0) + (ancho / 10.0)
min_y       = (alto*.75) 

# variables para el control de los colores en HSV
min_range   = (0, 0, 0)
max_range   = (360, 256, 50)
#max_range   = (360, 12, 10)

# variables para el control de los motores
VEL         = 300
vgiro       = 200
delante     = 1
atras       = 0


min_hsv_negro = np.array((0,0,0),np.int32)
max_hsv_negro = np.array((256,256,50),np.int32)
min_hsv_arena = np.array((9,70,0),np.int32)
max_hsv_arena = np.array((28,150,100),np.int32)
min_hsv_blanc = np.array((0,0,91),np.int32)
max_hsv_blanc = np.array((256,91,256),np.int32)
min_hsv_tacho = np.array((0,14,10),np.int32)
max_hsv_tacho = np.array((15,256,256),np.int32)


display = True
dual_display = False

# Variables para sensor de distancia - infrarojos
idDist      = 2
dist_min    = 22000
cero        = 0
uno         = 1

# Variables para sensores de grises
timeout_ini = 4
max_len     = 1 
grisDer     = 1
grisIzq     = 3 
alf_detect  = 20000

idBoton     = 6
