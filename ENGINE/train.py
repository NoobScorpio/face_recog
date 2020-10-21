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
import logging
logger = logging.Logger('catch_all')
KNOWN_FACES_DIR = '../ENGINE/known_faces'
TRAINED_FACES_DIR='../ENGINE/trained'

known_names=[]
knownList=[]
known_faces=[]
known_desc=[]

if not os.path.exists(f'{TRAINED_FACES_DIR}'):
    os.makedirs(f'{TRAINED_FACES_DIR}')

if os.path.exists('../ENGINE/models/model.txt') and os.path.exists('../ENGINE/models/known_names.txt') and os.path.exists('../ENGINE/models/known_desc.txt'):
    # print("OPENING")
    with open("../ENGINE/models/model.txt", "rb") as fp:
        known_faces = pickle.load(fp)
    with open("../ENGINE/models/known_names.txt", "rb") as fp:
        known_names = pickle.load(fp)
    with open("../ENGINE/models/known_desc.txt", "rb") as fp:
        known_desc = pickle.load(fp)


else:
    known_faces=[]
    known_names=[]
    known_desc={}



for name in os.listdir(KNOWN_FACES_DIR):
    if not os.path.exists(f'{TRAINED_FACES_DIR}/{name}'):
        os.makedirs(f'{TRAINED_FACES_DIR}/{name}')

    for filename in os.listdir(f'{KNOWN_FACES_DIR}/{name}'):
        print(name)
        print(f"{KNOWN_FACES_DIR}/{name}/{filename}")
        print(f"{filename}")
        # print("DONE")
        image = face_recognition.load_image_file(f'{KNOWN_FACES_DIR}/{name}/{filename}')

        try:
            encoding = face_recognition.face_encodings(image)[0]
            known_faces.append(encoding)
            print("DONE ENCODING")

            name_=name.split("_")[0]
            desc=name.split("_")[1]
            print("DONE SPLITING")
            known_names.append(name_)
            print("DONE NAME APPEND")
            known_desc[name_]=desc    
            print("DONE DESC APPEND")
            
            try:
                os.rename(f"{KNOWN_FACES_DIR}/{name}/{filename}", f"{TRAINED_FACES_DIR}/{name}/{filename}")
            except Exception:
                print(Exception)
        except Exception as e: # work on python 3.x
            logger.error('Failed to upload to ftp: '+ str(e))
            print("ERROR NO FACE")
            # os.remove(f'{KNOWN_FACES_DIR}/{name}/{filename}')


with open("../ENGINE/models/model.txt", "wb") as fp:
    pickle.dump(known_faces, fp)

with open("../ENGINE/models/known_names.txt", "wb") as fp:
    pickle.dump(known_names, fp)

with open("../ENGINE/models/known_desc.txt", "wb") as fp:
    pickle.dump(known_desc,fp)

shutil.rmtree(f"{KNOWN_FACES_DIR}/{name}")

print("Face has been trained.")
sys.stdout.flush()