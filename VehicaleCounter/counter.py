
from tkinter import CENTER
import cv2

import numpy as np

def centre_handle(x,y,w,h):
    x1 = int(w/2)
    y1 = int(h/2)
    cx = x+x1
    cy = y+y1

    return cx,cy

detect = []
offset = 6 # Allowable error between pixcel
counter = 0

# Input Data

cap = cv2.VideoCapture("VehicaleCounter\highway.mp4")

count_line_position = 550

# to remove backgroung
algo = cv2.bgsegm.createBackgroundSubtractorMOG()

min_weight_rec = 80
min_height_rec = 80
print("Program running")

while True:
    ret,frame1 = cap.read()

    
    # to grayscale the image
    grey = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey,(3,3),5)
        
        #Apply to each frame
    img_sub = algo.apply(blur)
    dilat = cv2.dilate(img_sub,np.ones((5,5)))
    kernal = cv2.getStructuringElement(cv2.MORPH_ELLIPSE ,(5,5))
    dilatada = cv2.morphologyEx(dilat , cv2.MORPH_CLOSE , kernal)
    dilatada = cv2.morphologyEx(dilatada , cv2.MORPH_CLOSE , kernal)
        
    Countershape,h = cv2.findContours(dilatada,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    cv2.line(frame1,(25,count_line_position),(1200,count_line_position),(255,122,0),3)
    cv2.line(dilatada,(25,count_line_position),(1200,count_line_position),(255,122,0),3)

    for (i,c) in enumerate(Countershape):
        (x,y,w,h) = cv2.boundingRect(c)
        validate_counter = (w>=min_weight_rec and h>=min_height_rec)

        if not validate_counter:
            continue
        else:
            cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),(2))
            cv2.rectangle(dilatada,(x,y),(x+w,y+h),(255,255,255),(2))

            center = centre_handle(x,y,w,h)
            detect.append(center)
            cv2.circle(frame1,center,4,(0,0,255),-1)
            cv2.circle(dilatada,center,4,(0,0,0),-1)

            for (x,y) in detect:
                if y<(count_line_position+offset) and y>(count_line_position-offset):
                    counter+=1
                cv2.line(frame1,(25,count_line_position),(1200,count_line_position),(255,122,0),3)
                detect.remove((x,y))
                print("Vehicale Counter:"+str(counter))

    cv2.putText(frame1,"Counter:"+str(counter),(450,70),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),5)




    cv2.imshow('Detector',dilatada)
    cv2.imshow('Video Original',frame1)

    if cv2.waitKey(1) == 13:
        break
    

cv2.destroyAllWindows()
cap.release()