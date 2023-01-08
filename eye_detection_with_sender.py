import cv2
import dlib
import socket
import time

HOST = "192.168.4.1"  # Standard loopback interface address (localhost)
PORT = 50000  # Port to listen on (non-privileged ports are > 1023)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

cap = cv2.VideoCapture(0)

detect_faces = dlib.get_frontal_face_detector()

set_face_landmark = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

while cv2.waitKey(1) != ord("q"):
    # eye status (which way it is looking)
    status = "None"

    # read the frame
    ret, frame = cap.read()

    # turn it to gray scale
    gray_scale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # detect faces
    faces = detect_faces(gray_scale)
    for face in faces:
        face_landmarks = set_face_landmark(gray_scale, faces[0])

        # set eye limits to first point
        eye_left = face_landmarks.part(36).x
        eye_right = face_landmarks.part(36).x
        eye_top = face_landmarks.part(36).y
        eye_bottom = face_landmarks.part(36).y

        # for every point
        for i in range(0, 68):
            # set x and y values
            x = face_landmarks.part(i).x
            y = face_landmarks.part(i).y

            # if the point id is between 36 and 41, it is a right eye's point
            if i >= 36 and i <= 41:
                # get the limits of the eye
                if x < eye_left:
                    eye_left = x
                if x > eye_right:
                    eye_right = x
                if y < eye_top:
                    eye_top = y
                if y > eye_bottom:
                    eye_bottom = y

            # make the point red
            cv2.circle(frame, (x, y), 1, (255, 255, 255), 2)

        eye_vertical_mid = (eye_bottom + eye_top) // 2
        eye_horizontal_mid = (eye_right + eye_left) // 2
        center_limit = (face_landmarks.part(39).x - face_landmarks.part(36).x) // 6

        # draw a rectangle to the eye
        cv2.rectangle(
            frame, (eye_left, eye_top), (eye_right, eye_bottom), (255, 255, 255), 1
        )
        # draw a rectangle to the center of the eye
        cv2.rectangle(
            frame,
            (eye_horizontal_mid - center_limit, eye_vertical_mid - center_limit),
            (eye_horizontal_mid + center_limit, eye_vertical_mid + center_limit),
            (0, 0, 255),
            1,
        )
        # draw a vertical line
        cv2.line(
            frame,
            (eye_horizontal_mid, eye_top),
            (eye_horizontal_mid, eye_bottom),
            (0, 0, 255),
            1,
        )
        # draw a horizontal line
        cv2.line(
            frame,
            (eye_left, eye_vertical_mid),
            (eye_right, eye_vertical_mid),
            (0, 0, 255),
            1,
        )

        # get the eye into another frame
        eye_frame = frame[eye_top:eye_bottom, eye_left:eye_right]

        # create grayscale blured roi
        gray_eye_frame = cv2.cvtColor(eye_frame, cv2.COLOR_BGR2GRAY)
        gray_eye_frame = cv2.GaussianBlur(gray_eye_frame, (7, 7), 0)

        # get the darkest value
        darkest_value = gray_eye_frame[0][0]
        for i in gray_eye_frame:
            for j in i:
                if j < darkest_value:
                    darkest_value = j
        color_limit = darkest_value + 30

        # create threshold due to darkest area
        _, threshold = cv2.threshold(
            gray_eye_frame, color_limit, 255, cv2.THRESH_BINARY_INV
        )
        threshold = cv2.erode(threshold, None, iterations=2)
        threshold = cv2.dilate(threshold, None, iterations=4)
        threshold = cv2.medianBlur(threshold, 3)

        # find the contour of the darkest area
        contours, _ = cv2.findContours(
            threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
        )

        # if there is a dark area
        if len(contours) != 0:
            # get the darkest area (iris)
            cnt = max(contours, key=cv2.contourArea)
            (x, y, w, h) = cv2.boundingRect(cnt)

            # get the iris values
            iris_left = eye_left + x
            iris_right = iris_left + w
            iris_top = eye_top + y
            iris_bottom = iris_top + h

            iris_vertical_mid = (iris_bottom + iris_top) // 2
            iris_horizontal_mid = (iris_right + iris_left) // 2

            # draw a rectangle to the iris
            cv2.rectangle(
                frame,
                (iris_left, iris_top),
                (iris_right, iris_bottom),
                (0, 255, 0),
                1,
            )

            # draw a vertical line
            cv2.line(
                frame,
                (iris_horizontal_mid, eye_top),
                (iris_horizontal_mid, eye_bottom),
                (0, 255, 0),
                1,
            )

            # draw a horizontal line
            cv2.line(
                frame,
                (eye_left, iris_vertical_mid),
                (eye_right, iris_vertical_mid),
                (0, 255, 0),
                1,
            )

            # set the status of the eye
            if (eye_bottom - eye_top) < int(center_limit * 1.5):
                status = "Bottom"
            elif iris_vertical_mid < eye_vertical_mid - center_limit // 3:
                status = "Top"
            elif iris_horizontal_mid > eye_horizontal_mid + center_limit:
                status = "Left"
            elif iris_horizontal_mid < eye_horizontal_mid - center_limit:
                status = "Right"
            else:
                status = "Middle"

    sock.send(status[0].encode())

    print(status)
    frame = cv2.putText(
        frame,
        status,
        (5, 90),
        cv2.FONT_HERSHEY_SIMPLEX,
        3,
        (0, 0, 255),
        2,
        cv2.LINE_AA,
    )
    cv2.imshow("Frame", frame)

sock.close()
cap.release()
cv2.destroyAllWindows()

"""
Detect Eye Pupil Better:
https://towardsdatascience.com/real-time-eye-tracking-using-opencv-and-dlib-b504ca724ac6

Face Landmark:
https://www.kaggle.com/datasets/sergiovirahonda/shape-predictor-68-face-landmarksdat
"""
