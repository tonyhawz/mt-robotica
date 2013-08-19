import numpy as np 

# variables de configuracion para la camara
camara      = -1
ancho       = 160
alto        = 120

# variables para el control de la posicion de la latita
min_area    = 150000
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

display = True

idDist      = 2
dist_min    = 22000
cero        = 0
uno         = 1
