import cv2

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

while cv2.waitKey(1) != ord("q"):
    # read the frame
    ret, frame = cap.read()

    # turn it to gray scale
    gray_scale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # detect the face
    faces = face_cascade.detectMultiScale(gray_scale, 1.3, 5)
    for (x, y, w, h) in faces:

        # draw a rectangle to face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # copy the face region of interest and turn it to gray scale
        gray_face_roi = gray_scale[y : y + (int)(h / 3) * 2, x : x + (int)(w / 2)]
        color_face_roi = frame[y : y + (int)(h / 3) * 2, x : x + (int)(w / 2)]

        # detect the face
        eyes = eye_cascade.detectMultiScale(gray_face_roi, 1.3, 5)
        for (ex, ey, ew, eh) in eyes:
            # draw a rectangle to eyes
            cv2.rectangle(color_face_roi, (ex, ey), (ex + ew, ey + eh), (255, 0, 0), 2)
            # draws the vertical line
            cv2.line(
                color_face_roi,
                (ex + int(ew / 2), ey),
                (ex + int(ew / 2), ey + eh),
                (255, 0, 0),
                2,
            )
            # draws the horizontal line
            cv2.line(
                color_face_roi,
                (ex, ey + int(eh / 2)),
                (ex + ew, ey + int(eh / 2)),
                (255, 0, 0),
                2,
            )

    cv2.imshow("frame", frame)

cap.release()
cv2.destroyAllWindows()


"""
Links:
- OpenCV Pretrained Cascade Example: https://www.youtube.com/watch?v=mPCZLOVTEc4
- Eye Motion Trackin OpenCV Example: https://www.youtube.com/watch?v=kbdbZFT9NQI
Others:
- Eye Dataset: https://www.kaggle.com/datasets/kayvanshah/eye-dataset
- Darknet: https://github.com/pjreddie/darknet
- Darknet: https://github.com/AlexeyAB/darknet
"""

# cap = cv2.VideoCapture(0)
# face_cascade = cv2.CascadeClassifier(
#     cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
# )
# eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

# while True:
#     ret, frame = cap.read()

#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     faces = face_cascade.detectMultiScale(gray, 1.3, 5)
#     for (x, y, w, h) in faces:
#         cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 5)
#         roi_gray = gray[y : y + w, x : x + w]
#         roi_color = frame[y : y + h, x : x + w]
#         eyes = eye_cascade.detectMultiScale(roi_gray, 1.3, 5)
#         for (ex, ey, ew, eh) in eyes:
#             cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 5)

#     cv2.imshow("frame", frame)

#     if cv2.waitKey(1) == ord("q"):
#         break

# cap.release()
# cv2.destroyAllWindows()
