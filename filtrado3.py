import cv
import config

def main ():
    capture = cv.CaptureFromCAM (-1)
    cv.SetCaptureProperty (capture, cv.CV_CAP_PROP_FRAME_WIDTH, 160)
    cv.SetCaptureProperty (capture, cv.CV_CAP_PROP_FRAME_HEIGHT, 120)
    fps = cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FPS)

    while True:
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
            print "area: " + str (a)
            print "X: " + str (X)
            #Y = int(cv.GetSpatialMoment (moment, 0, 1) / a)
            if X > config.max_x:
                print "derecha"
            elif X < config.min_x:
                print "izquierda"
            else:
                print "centrado"
        else:
            print "objeto no detectado o muy pequeno"

        # Con esto corto y salgo
        if cv.WaitKey (int(1000/fps)) != -1:
            break
 
    return;

if __name__ == "__main__":
    main ()
