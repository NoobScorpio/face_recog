import face_recognition
import os
import cv2
import datetime as dt
import numpy as np
import sys
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
import dlib
import pickle
import shutil


with open("../ENGINE/models/known_names.txt", "rb") as fp:
        known_names = pickle.load(fp)

for name in known_names:
    print(name)