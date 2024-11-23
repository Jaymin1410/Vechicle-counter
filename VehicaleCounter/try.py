import cv2
import numpy as np
# web cam

cap = cv2.VideoCapture("D:\\Progarmming\\Vehicale Counter\\abc.mp4")
ret,frame1 = cap.read()
cv2.imshow('Video Original',frame1)
