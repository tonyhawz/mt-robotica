import numpy as np

refresh_rate = .01

#refresh_rate = 1

# variables de configuracion para la camara
camara      = 0
#camara = '../videos/video-1378342226.29.avi'
#camara = '../videos/video-1379160469.34.avi'
#camara = '../videos/video-1379159783.25.avi'

display = False
dual_display = False

ancho       = 160
alto        = 120

# variables para el control de la posicion de la latita
camara_min_ratio_area = 0.015

camara_ratio_mascaras_laterales = 0.05

camara_mask_area_ratio = 0.02

min_area    = 200
#area_lata   = 1000000
area_lata   = 1000
area_tacho   = 7000
#min_x       = (ancho / 2.0) - (ancho / 9.0)
#max_x       = (ancho / 2.0) + (ancho / 4.0)
min_x       = ancho * 0.2
max_x       = ancho * 0.8
min_y       = alto*0.8


#min_x = 0
#max_x = ancho
#min_y = alto * .50


#min_x = 0
#max_x = 640
#min_y = 100


# variables para el control de los colores en HSV
min_range   = (0, 0, 0)
max_range   = (360, 256, 56)
#max_range   = (360, 12, 10)
#max_range   = (360, 256, 50)

# variables para el control de los motores
#en arena
VEL         = 400
vgiro       = 900
#vgiromenor       = 400
vgiromenor  = 200

vgirobusqueda  = 800

# en piso
#VEL         = 400
#vgiro       = 800
#vgiromenor  = 200

delante     = 0
atras       = 1


#negro lata arena :S
min_hsv_negro = np.array((0, 0, 0), np.int32)
max_hsv_negro = np.array((256, 256, 90), np.int32)

#negro bien
#min_hsv_negro = np.array((0, 0, 0), np.int32)
#max_hsv_negro = np.array((256, 256, 50), np.int32)

#min_hsv_arena = np.array((0, 14, 80), np.int32) #arena fing
#max_hsv_arena = np.array((100, 224, 256), np.int32)#arena fing

#min_hsv_arena = np.array((0, 42, 100), np.int32)#alfombra lab
#max_hsv_arena = np.array((100, 224, 256), np.int32)#alfombra lab


#color de la arena !!!
min_hsv_blanc = np.array((0, 0, 60), np.int32)
max_hsv_blanc = np.array((192, 69, 239), np.int32)

#min_hsv_blanc = np.array((0,0,91),np.int32)
#max_hsv_blanc = np.array((256,91,256),np.int32)

min_hsv_tacho = np.array((0,14,10),np.int32)
max_hsv_tacho = np.array((15,256,256),np.int32)

min_hsv_azul = np.array((100,0,0),np.int32)
max_hsv_azul = np.array((150,256,256),np.int32)



# Variables para sensor de distancia - infrarojos
idDistIzq      = 3
idDistDer      = 2
max_len     = 4 # max buffer de mediciones
dist_min    = 8000
cero        = 0
uno         = 1

# Variables para sensores de grises
timeout_ini = 4

grisDer     = 1
grisIzq     = 3
alf_detect  = 20000

idBoton     = 5

# Variables para motores
id_motor_camara_X = 12
id_motor_camara_Y = 11

id_motor_tolva = 99
tolva_pos_init = 545
tolva_pos_final = 800
tolva_vel = 200
tiempo_salida_tacho = 3


motores_timeout_adelante = 10
motores_timeout_girar = 2

motor_pinza_speed = 200
motor_pinza_d_1 = 6
motor_pinza_d_2 = 5
motor_pinza_i_1 = 8
motor_pinza_i_2 = 7

#volvado
motor_volcadora = 13
tiempo_pinza_descarga = 2
tiempo_descarga = 2


vel_paneo = 100
motor_camara_x_pos = 511
motor_camara_y_pos = 0

max_camara_x=611
max_camara_y=1023
min_camara_x=411
min_camara_y=0

alfa_giro = 20

cero_posx_camara = 511
cero_posy_camara = 100
