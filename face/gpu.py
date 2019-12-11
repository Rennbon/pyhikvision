from numba import jit, uint8, i8, vectorize
import numba as nb
import numpy as np
import datetime
import cv2
import array

url = "rtsp://admin:Aa123456@192.168.254.6:554/Streaming/Channels/101"


@jit([nb.void(i8, i8)], nopython=True)
def add_with_vec(yy, c):
    print(yy, c)


@jit([nb.void(uint8[:, :, ::1])], forceobj=True)
def checkPic(frame):
    print(nb.typeof(frame))


add_with_vec(i8(10), i8(2))

video_capture = cv2.VideoCapture(url)
ret, frame = video_capture.read()

# print(nb.typeof(frame))

checkPic(frame)
