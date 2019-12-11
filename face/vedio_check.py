import _thread
import asyncio
import os
import time
from numba import jit, uint8
import numba as nb
import face_recognition
import cv2
import numpy as np
import datetime

url = "rtsp://admin:Aa123456@192.168.254.6:554/Streaming/Channels/101"
# loop = asyncio.get_event_loop()
# Get a reference to webcam #0 (the default one)

video_capture = cv2.VideoCapture(url)
# Load a sample picture and learn how to recognize it.
rennbon_image1 = face_recognition.load_image_file("rennbon.jpg")
ec1 = face_recognition.face_encodings(rennbon_image1)[0]

rennbon_image2 = face_recognition.load_image_file("rennbon2.jpg")
ec2 = face_recognition.face_encodings(rennbon_image2)[0]
# Load a second sample picture and learn how to recognize it.
# Create arrays of known face encodings and their names
known_face_encodings = [
    ec1,
    ec2
]
known_face_names = [
    "Rennbon Zhu",
    "Rennbon Zhu"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True


# http://numba.pydata.org/numba-doc/0.12/tutorial_numpy_and_numba.html
@jit([nb.void(uint8[:, :, ::1])], forceobj=True, parallel=True)
def checkPic(frame):
    t1 = np.datetime64(datetime.datetime.now())
    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        # Or instead, use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
        face_names.append(name)

    if face_names.__len__() > 0:
        print(face_names)
    t2 = np.datetime64(datetime.datetime.now())
    print((t2 - t1))


previous = int(round(time.time() * 1000))

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()
    current = int(round(time.time() * 1000))
    if current - previous > 1000:
        # loop.run_until_complete(checkPic(frame))
        previous = current
        _thread.start_new_thread(checkPic, (frame,))
        # checkPic(frame)
    # Resize frame of video to 1/4 size for faster face recognition processing
    # small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    # rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    # if process_this_frame:
    #     # Find all the faces and face encodings in the current frame of video
    #     face_locations = face_recognition.face_locations(rgb_small_frame)
    #     face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    #
    #     face_names = []
    #     for face_encoding in face_encodings:
    #         # See if the face is a match for the known face(s)
    #         matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
    #         name = "Unknown"
    #
    #         # # If a match was found in known_face_encodings, just use the first one.
    #         # if True in matches:
    #         #     first_match_index = matches.index(True)
    #         #     name = known_face_names[first_match_index]
    #
    #         # Or instead, use the known face with the smallest distance to the new face
    #         face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
    #         best_match_index = np.argmin(face_distances)
    #         if matches[best_match_index]:
    #             name = known_face_names[best_match_index]
    #
    #         face_names.append(name)

    # process_this_frame = not process_this_frame

    # Display the results
    # for (top, right, bottom, left), name in zip(face_locations, face_names):
    #     # Scale back up face locations since the frame we detected in was scaled to 1/4 size
    #     top *= 4
    #     right *= 4
    #     bottom *= 4
    #     left *= 4
    #
    #     # Draw a box around the face
    #     cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
    #
    #     # Draw a label with a name below the face
    #     cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
    #     font = cv2.FONT_HERSHEY_DUPLEX
    #     cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
