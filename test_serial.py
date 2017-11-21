import numpy as np
import cv2
import timeit
import cPickle
import jsonpickle
import jsonpickle.ext.numpy as jsonpickle_numpy
import json

jsonpickle_numpy.register_handlers()
img_standard = cv2.imread("testframe.jpg")

img_pickle = open("img_pickle", 'rb')
img_json = open("img_json", 'rb')
img_from_pickle = cPickle.load(img_pickle)
img_json_str = json.load(img_json)
img_from_json = jsonpickle.decode(img_json_str)

cv2.imshow('Standard frame',img_standard)
cv2.imshow('Pickled frame',img_from_pickle)
cv2.imshow('JSON frame',img_from_json)
while 1:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

img_pickle.close()
img_json.close()
cv2.destroyAllWindows()