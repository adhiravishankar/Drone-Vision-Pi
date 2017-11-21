# Import socket module
import socket
import socket_helper

import numpy as np
import cv2
import timeit
import jsonpickle
import jsonpickle.ext.numpy as jsonpickle_numpy
import json
import cPickle
import struct

jsonpickle_numpy.register_handlers()
cap = cv2.VideoCapture(0)
w = 800
h = 448
cap.set(3,w);
cap.set(4,h);
get_face=0
cont=True

# Create a socket object
s = socket.socket()
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
 
# Define the port on which you want to connect
port = 54321               
 
# connect to the server on local computer
##s.connect(('128.61.15.225', port))
s.connect(('192.168.43.123', port))
 
# receive data from the server
print s.recv(1024)
jsonpickle_numpy.register_handlers()
##test_str = 'm' * 1000
##test_str = struct.pack('>I', len(test_str)) + test_str
img_dims = {'w':w , 'h':h}
img_jsondims = jsonpickle.encode(img_dims)
s.sendall(struct.pack('>I', len(img_jsondims)) + img_jsondims)
while cont:
    # Capture frame-by-frame
    start_time = timeit.default_timer()
    ret, img = cap.read()
    
    # Display the resulting frame
##    cont = False
    
##    Sending image encoded as JSON pickle does not work well:
##    it takes too long to be encoded (~0.1s)
##    img_jsonpickle = jsonpickle.encode(img)
##    print "%d:" % len(img_jsonpickle)
##    s.sendall(struct.pack('>I', len(img_jsonpickle)) + img_jsonpickle)

##    Sending image encoded as cPickle does not work well:
##    bytestream is too large and takes too long to be sent    
##    img_pickle = cPickle.dumps(img, protocol=2)
##    print "%d:" % len(img_pickle)
##    s.sendall(struct.pack('>I', len(img_pickle)) + img_pickle)
    
##    Best solution seems to be to encode image as JPG:
##    completes fast enough and compresses image so its
##    transmission does not take too long
    img_str = cv2.imencode('.jpg',img)[1].tostring()
##    print "%d:" % len(img_str)
    s.sendall(struct.pack('>I', len(img_str)) + img_str)
    
##    Receive coordinates of detected faces
    faces_str = socket_helper.recv_msg(s)
    if len(faces_str) > 1:
##        print "Faces detected!"
        faces = np.fromstring(faces_str, dtype=np.uint32)
        faces = faces.reshape((-1,4))
##        print faces
        for (x, y, w, h) in faces:
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
    
##    Display image with faces detected
    cv2.imshow('frame',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    run_time = timeit.default_timer() - start_time
    print "Runtime:", run_time
# close the connection
s.close() 