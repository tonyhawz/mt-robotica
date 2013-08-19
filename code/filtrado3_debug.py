import cv
import config

def main ():
    pr_window = "imagen"
    capture = cv.CaptureFromCAM (-1)
    cv.NamedWindow (pr_window, 1)

#    seteo tamanio de la ventana |-| comentar cuando no se necesite mostrar ventana
    cv.SetCaptureProperty (capture, cv.CV_CAP_PROP_FRAME_WIDTH, config.ancho)
    cv.SetCaptureProperty (capture, cv.CV_CAP_PROP_FRAME_HEIGHT, config.alto)
    delay = 0 
    while True:
        if (not(delay == 20)):
            delay += 1
            img = cv.QueryFrame (capture)
            cv.ReleaseCapture( img )
        else:
            delay = 0
            frame = cv.QueryFrame (capture)
            maskN = cv.CreateImage (cv.GetSize (frame), 8, 1)
            hsvN = cv.CloneImage (frame)

            cv.Smooth (frame, frame, cv.CV_BLUR, 3)

            cv.CvtColor (frame, hsvN, cv.CV_BGR2HSV)
            cv.InRangeS (hsvN, config.min_range, config.max_range, maskN)

            moment = cv.Moments (cv.GetMat (maskN), 0)
            a = cv.GetCentralMoment (moment, 0, 0)

            if a > config.min_area:
                X = int(cv.GetSpatialMoment (moment, 1, 0) / a)
                print "X: " + str (X)
                print "min: " + str (config.min_x)
                print "max: " + str (config.max_x)
            #Y = int(cv.GetSpatialMoment (moment, 0, 1) / a)
                if X > config.max_x:
                    print "derecha"
                elif X < config.min_x:
                    print "izquierda"
                else:
                    print "centrado"
            else:
                print "objeto no detectado o muy pequeno"

            cv.ShowImage (pr_window, maskN)

#        descomentar para debug
#        X = int(cv.GetSpatialMoment (moment, 1, 0) / a)
#        print 'x: ' + str (X)  + ' area: ' + str (a)

        # Con esto corto y salgo
#        if cv.WaitKey (100) != -1:
#            break
 
    return;

if __name__ == "__main__":
    main ()
