import sys,os
import shutil
name=sys.argv[1]
desc=sys.argv[2]
# name="test"

FILES_PATHS_DIR='../GUI/picsData.txt'
FILES_NAMES_DIR='../GUI/picsNames.txt'
KNOWN_FACES_DIR = '../ENGINE/known_faces'
TRAINED_FACES_DIR='../ENGINE/trained'
try:
    text = open(FILES_PATHS_DIR,'r').read()
    filesPath= text.split(",")

    text = open(FILES_NAMES_DIR,'r').read()
    filesNames=text.split(",")
except :
    print("NO SUCH FILE OR DIRECTORY")

try:
    if not os.path.exists(f'{KNOWN_FACES_DIR}/{name}_{desc}'):
        os.makedirs(f'{KNOWN_FACES_DIR}/{name}_{desc}')
except:
    print("ERROR MAKING DIRR")

for fileName,filePath in zip(filesNames,filesPath):
    # os.rename(f"{filePath}", f"{KNOWN_FACES_DIR}/{name}/{fileName}")
    try:
        shutil.move(f"{filePath}", f"{KNOWN_FACES_DIR}/{name}_{desc}/{fileName}")
        print("MOVED")
    except :
        print("ERROR")
os.remove(FILES_PATHS_DIR)
os.remove(FILES_NAMES_DIR)






