import cv2
import sys
import os
name=sys.argv[1]
desc=sys.argv[2]
# name="TEST"
FRAME_THICKNESS = 3
FONT_THICKNESS = 2
MODEL = 'hog' 
KNOWN_FACES_DIR = '../ENGINE/known_faces'

if not os.path.exists(f'{KNOWN_FACES_DIR}/{name}_{desc}'):
    os.makedirs(f'{KNOWN_FACES_DIR}/{name}_{desc}')

video= cv2.VideoCapture(0)
save=0
while True:
    ret, image=video.read()
    cv2.rectangle(image, (10,10), (20,20), (0,255,0), cv2.FILLED)
    cv2.putText(image, str("Pics Take "+str(save)), 
                                ( 10, 65), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), FONT_THICKNESS)
    
    cv2.imshow("CAPTURE", image)
    if cv2.waitKey(1) & 0xFF==ord("q"):
        break
    if cv2.waitKey(1) & 0xFF==ord("s"):
        cv2.imwrite(f"{KNOWN_FACES_DIR}/{name}_{desc}/image{save}.jpg",image)
        save+=1
    
# print("Pictures Taken, press save to Train the Pictures.")
# sys.stdout.flush()