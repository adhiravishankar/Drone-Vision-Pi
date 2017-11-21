import numpy as np
import cv2
import timeit

cap = cv2.VideoCapture(0)
w = 800
h = 448
cap.set(3,w);
cap.set(4,h);

face_cascade = cv2.CascadeClassifier('/home/pi/opencv-3.3.0/data/haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('/home/pi/opencv-3.3.0/data/haarcascades/haarcascade_eye.xml')
cont = 1001
get_face = 1
contains_faces = 1

output_list = []
if get_face:
    file_name = "detect_"
else:
    file_name = "basic_"
if contains_faces:
    file_name = file_name + "faces_"
else:
    file_name = file_name + "nothing_"
file_name = file_name + "{}_{}.txt".format(w,h)
output_file = open(file_name, 'w')
while(cont):
    # Capture frame-by-frame
    start_time = timeit.default_timer()
    ret, img = cap.read()
    
    # Our operations on the frame come here
    if get_face:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

    # Display the resulting frame
    cv2.imshow('frame',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
##    cont = False
    run_time = timeit.default_timer() - start_time
    cont = cont - 1
    output_list.append(run_time)
    
for time in output_list:
    output_file.write("{}\n".format(time))
output_file.close()

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
