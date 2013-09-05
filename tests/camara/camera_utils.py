import numpy as np
import cv2


def to_3d(img):
    if len(img.shape) == 2 :
        return cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
    return img

def join_images(img1,img2):
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]
    vis = np.zeros((max(h1, h2), w1+w2,3), np.uint8)
    #vis = np.zeros((max(h1, h2), w1+w2), np.uint8)
    vis[:h1, :w1] = to_3d(img1)
    vis[:h2, w1:w1+w2] = to_3d(img2)
    return vis

def test_join_images():
    camera = cv2.VideoCapture(0);
    camera.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 640);
    camera.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 480);
    cv2.namedWindow("test");
    while True:
        f,image = camera.read();
        if f:
            cv2.imshow("test", join_images(image,image))
            if cv2.waitKey(10) % 0x100 == 27:
                break

if __name__ == "__main__":
    test_join_images()

