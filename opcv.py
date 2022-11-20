import json
import face_recognition
import imutils
import pickle
import time
import cv2
import os
import requests

from deepface import DeepFace

def analyze(url_img):
    try:
        result_dict = DeepFace.analyze(img_path=f"img/face_{url_img}.png", actions=['age', 'gender', 'race', 'emotion'], enforce_detection = False)

        with open(f'face_analyze_{url_img}.json', 'w') as file:
            json.dump(result_dict, file, indent=4, ensure_ascii=False)

        print(f'[+] Age: {result_dict.get("age")}')
        print(f'[+] Gender: {result_dict.get("gender")}')

        print(f'[+] Race:' )
        for k, v in result_dict.get('race').items():
            v = round(v, 2)
            print(f'{k} - {v}%')

        print(f'[+] Emotion:' )
        for k, v in result_dict.get('emotion').items():
            print(f'{k} - {round(v, 2)}%')
        age = result_dict.get("age")
        gender = result_dict.get("gender")
        dict = json.load(open(f'face_analyze_{url_img}.json'))
        race = dict['dominant_race']
        return [age, gender, race]
    except Exception as _ex:
        return _ex

def PrintToPHP(name, age, gender, race):
    # print(name, age, gender, race)
    mydata = [('Name', name), ('Age', age), ('Gender', gender), ('Race', race)]
    userdata = [('Name', name), ('Age', age), ('Gender', gender), ('Race', race)]
    resp = requests.post('https://icm-team.ru/index.php', params = mydata)
    print(mydata)
    print(resp)


def detect():
    otdel = 'alcohol'
    cascPathface = os.path.dirname(
        cv2.__file__) + "/data/haarcascade_frontalface_alt2.xml"
    faceCascade = cv2.CascadeClassifier(cascPathface)
    data = pickle.loads(open('face_enc', "rb").read())

    print("Streaming started")
    video_capture = cv2.VideoCapture('videos/video_4.mov')

    count = 1
    while True:
        ret, frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray,
                                             scaleFactor=1.1,
                                             minNeighbors=5,
                                             minSize=(60, 60),
                                             flags=cv2.CASCADE_SCALE_IMAGE)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(rgb)
        names = []
        for encoding in encodings:
            matches = face_recognition.compare_faces(data["encodings"], encoding)
            name = "Unknown"
            if True in matches:
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}
                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1
                name = max(counts, key=counts.get)

            names.append(name)
            for ((x, y, w, h), name) in zip(faces, names):
                cv2.imwrite(f"img/face_{name}.png", frame)
                if(count == 1):
                    a = analyze(name)
                    count += 1
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, name, (x, y-100), cv2.FONT_HERSHEY_SIMPLEX,
                        0.75, (0, 255, 0), 2)
                cv2.putText(frame, f'Age: {a[0]} years', (x, y-70), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (0, 255, 0), 1)
                cv2.putText(frame, f'Gender: {a[1]}', (x, y-40), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (0, 255, 0), 1)
                cv2.putText(frame, f'Race: {a[2]}', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (0, 255, 0), 1)
                PrintToPHP(name, a[0], a[1], a[2])
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video_capture.release()
    cv2.destroyAllWindows()
detect()