import face_recognition
import os
import cv2
import datetime as dt
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
import dlib
import pickle
import numpy as np
dlib.DLIB_USE_CUDA = True

# details=["Data Scientist","Ai Engineer","Ui/Ux Lead","Director","PHP Dev"]

# ###############################################
#####   DEFINING BASIC PARAMETERS    ####
# ###############################################


KNOWN_FACES_DIR = '../ENGINE/known_faces'
UNKNOWN_FACES_DIR='../ENGINE/unknownFaces'
TOLERANCE = 0.5
FRAME_THICKNESS = 3
FONT_THICKNESS = 2
MODEL = 'hog'  # default: 'hog', other one can be 'cnn' - CUDA accelerated (if available) deep-learning pretrained model



# ###############################################
#####   LOADING EMOTION MODEL    ####
# ###############################################


#loading the model
json_file = open('../ENGINE/models/fer.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)


# load weights into new model
loaded_model.load_weights("../ENGINE/models/fer.h5")
print("Loaded model from disk")

labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

video= cv2.VideoCapture(0)
print('Loading known faces...')


# ###############################################
#####   OPEINING THE KNOW FACES ENCODINGS    ####
# ###############################################

known_faces = []
known_names = []
knownList={}
known_desc=[]
checkin_list=[]

with open("../ENGINE/models/model.txt", "rb") as fp:
    known_faces = pickle.load(fp)

with open("../ENGINE/models/known_names.txt", "rb") as fp:
    known_names = pickle.load(fp)

with open("../ENGINE/models/known_desc.txt", "rb") as fp:
    known_desc = pickle.load(fp)

for name in known_names:
    knownList[name]=[]

print('Processing unknown faces...')

j=0
prevUnknown=None
multinowUnknown=[]
first=True
ukiter=0
process=0
print(dlib.DLIB_USE_CUDA)


# ################################################################################
#####    METHOD THAT COUNTS TOTAL UNKNOWN AND REFACTORS THEM AFTER 5 FRAMES   ####
# ################################################################################

def totalUnknown():
    unknown_faces=[]
    k=0
    for filename in os.listdir(f'{UNKNOWN_FACES_DIR}/'):
        image = face_recognition.load_image_file(f'{UNKNOWN_FACES_DIR}/{filename}')
        try:
            print(f"K IS {k}")
            locations = face_recognition.face_locations(image, model=MODEL)
            encodings = face_recognition.face_encodings(image, locations)
            for face_encoding, face_location in zip(encodings, locations):
                results = face_recognition.compare_faces(known_faces, face_encoding, TOLERANCE)
                unknown_faces.append(face_encoding)
                if True in results: 
                    os.remove(f'{UNKNOWN_FACES_DIR}/{filename}')
        except:

            os.remove(f'{UNKNOWN_FACES_DIR}/{filename}')
            continue
        print(f'{UNKNOWN_FACES_DIR}/{filename}  AND ENCODINGS {encodings}')
    uk=0
    for filename in os.listdir(f'{UNKNOWN_FACES_DIR}/'):
        uk+=1
    print(f"UNKNOWN PEOPLE {uk}") 

# #################################################################################
#####   METHOD THAT APPENDS THE DATETIME AT WHICH THE PERSON WAS RECOGNIZED    ####
# ################################################################################

def appendKnownPeople(name,dateDetected):
    for key in knownList:
        if name==key:
            arr=knownList[key]
            arr.append(dateDetected)
            knownList[key]=arr

# #########################################################################################
#####   METHOD THAT CALCUALTES THE TOTAL TIME A PERSON WAS IN SCREEN BEFORE QUITING    ####
# #########################################################################################

def totalTime(name,dateArray):
    s1 = dateArray[0]
    s2 = dateArray[-1] # for example
    FMT = '%Y-%m-%d %H-%M-%S-%f'
    tdelta = dt.datetime.strptime(s2, FMT) - dt.datetime.strptime(s1, FMT) 
    from datetime import timedelta  
    if tdelta.days < 0:
        tdelta = timedelta(days=0,hours=tdelta.hours,
            seconds=tdelta.seconds, microseconds=tdelta.microseconds)
    print(f"{name} "+f"Entered at {s1} and left at {s2}, Hence total time: "+str(tdelta))

# ######################################################
#####   METHOD THAT GETS DESIGNATION OF A PERSON    ####
# ######################################################

def checkInPerson(name,dateArray):
    if name not in checkin_list:
        with open('../ENGINE/models/checkin.txt', 'w') as f:
                f.write(f"{name} checked in at {dateArray[0]}/")
        checkin_list.append(name)
    
# ###################################################################
#####   METHOD THAT TELLS AT THE END IF A PERSON CAME OR NOT    ####
# ##################################################################

def checkPeople(peopleArray):
    for key in peopleArray:
        if peopleArray[key]==[]:
            print(f"{peopleArray[key]} didnot come")
            
        else:
            print(f"{peopleArray[key]} came")
            totalTime(key,peopleArray[key])

# #########################################
#####   METHOD THAT CHECKS EMOTIONS    ####
# #########################################

def emotion(face_location,image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    x,y=face_location[3],face_location[0]
    roi_gray = gray[int(y):int(face_location[2]), int(x):int(face_location[1])]
    cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
    yhat= loaded_model.predict(cropped_img)
    if int(np.argmax(yhat))==0 or int(np.argmax(yhat))==1 or int(np.argmax(yhat))==2 or int(np.argmax(yhat))==5 :
        emot=0
    elif int(np.argmax(yhat))==3:
        emot=3
    elif int(np.argmax(yhat))==4 or int(np.argmax(yhat))==6:
        emot=4
    return emot

# ######################################################
#####   METHOD THAT GETS DESIGNATION OF A PERSON    ####
# ######################################################

def getDetails(name):
    for key in known_desc:
        if name==key:
            return known_desc[key]

#############################################################################
#####   MAIN LOOP THAT STARTS THE VIDEO STREAM AND CAPTURES ENCODINGS    ####
# ###########################################################################

while True:
    ret,image=video.read()
    new_frame=image
    emot=0
    roi_gray=None
    gray=None
    locations = face_recognition.face_locations(image, model=MODEL)
    encodings = face_recognition.face_encodings(image, locations) ##### FACE ENCODINGS #####

    for face_encoding, face_location in zip(encodings, locations):
        
        results = face_recognition.compare_faces(known_faces, face_encoding, TOLERANCE) 
        match = None
        date=dt.datetime.now().strftime('%Y-%m-%d %H-%M-%S-%f')
        if True in results: 
            emot=emotion(face_location,image)
            nowKnown=results
            match = known_names[results.index(True)] #THIS IS THE MATCHED NAME
            top_left = (face_location[3], face_location[0])
            bottom_right = (face_location[1], face_location[2])
            cv2.rectangle(image, top_left, bottom_right, (0,255,0), FRAME_THICKNESS) ##### FACE BOX
            
            top_left = (face_location[3], face_location[2])
            bottom_right = (face_location[1], face_location[2] + 22)
            cv2.rectangle(image, top_left, bottom_right, (0,255,0), cv2.FILLED) ##### NAME BOX
            
            cv2.putText(image, str(match+" "+labels[emot]), (face_location[3] + 10, face_location[2] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), FONT_THICKNESS) #NAME TEXT
            
            detail=getDetails(match)
            top_left = (face_location[3], face_location[2]+22)
            bottom_right = (face_location[1], face_location[2] + 50)
            cv2.rectangle(image, top_left, bottom_right, (0,255,0), cv2.FILLED) #DESIGNATION BOX
            
            cv2.putText(image, str(detail), (face_location[3] + 10, face_location[2] + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), FONT_THICKNESS) #DESIGNATION NAME
            
            appendKnownPeople(match,date)
            checkInPerson(match,knownList[match])
      
        elif False in results:
            process+=1   ###### THIS VARIABEL DEFINES IF HE PERSON IS UNKNOWN FOR 5 FRAMES, IT WILL LET IT BE DECLARED UNKNOWN
            if process>=5 or process==0:
                top_left = (face_location[3], face_location[0])
                print(f' - {match} from {results}')
                bottom_right = (face_location[1], face_location[2])
                cv2.rectangle(image, top_left, bottom_right, (0,0,255), FRAME_THICKNESS)
                top_left = (face_location[3], face_location[2])
                bottom_right = (face_location[1], face_location[2] + 22)
                cv2.rectangle(image, top_left, bottom_right, (0,0,255), cv2.FILLED)
                cv2.putText(image, 'UNKNOWN', (face_location[3] + 10, face_location[2] + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), FONT_THICKNESS)
                detail=getDetails("None")
                top_left = (face_location[3], face_location[2]+22)
                bottom_right = (face_location[1], face_location[2] + 44)
                cv2.rectangle(image, top_left, bottom_right, (0,0,255), cv2.FILLED)
                cv2.putText(image, str(detail), (face_location[3] + 10, face_location[2] + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), FONT_THICKNESS)
                
                if j>0:
                    ukiter+=1  ##### THIS VARIABLE TRIGGERS THE RECHECKS METHOD totalUnknown() IF UNKNOWN PERSON WAS RECOGNIZED in MORE THEN 10 FRAMES
                    unknownResult=face_recognition.compare_faces(multinowUnknown,face_encoding, TOLERANCE)

                    if True in unknownResult:
                        print("PREVIOUS UNKNOWN")
                    else:
                        cv2.imwrite('./unknownFaces/UNKNOWN'+str(date)+'.jpg',new_frame)
                        j+=1
                        if ukiter>=10:
                            totalUnknown()
                            ukiter=0

                multinowUnknown.append(face_encoding)
                prevUnknown=face_encoding
                ####### FIRST UNKNOWN FRAME SHOULD BE SAFED WHICH WILL BE RECHECKED IN THE METHOD
                if j==0:
                    cv2.imwrite('./unknownFaces/UNKNOWN'+str(date)+'.jpg',new_frame)
                    j+=1
                    totalUnknown()
                process=0
            ###### SHOW PROCESSING UNTIL 5 FRAMES HAVE PASSED
            else:
                top_left = (face_location[3], face_location[0])
                bottom_right = (face_location[1], face_location[2])
                cv2.rectangle(image, top_left, bottom_right, (0,0,255), FRAME_THICKNESS)
                top_left = (face_location[3], face_location[2])
                bottom_right = (face_location[1], face_location[2] + 22)
                cv2.rectangle(image, top_left, bottom_right, (0,0,255), cv2.FILLED)
                cv2.putText(image, 'PROCESSING...', (face_location[3] + 10, face_location[2] + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 0, 0), FONT_THICKNESS)

    cv2.imshow("CAPTURE", image)
    if cv2.waitKey(1) & 0xFF==ord("q"):
        break


totalUnknown()
checkPeople(knownList)





