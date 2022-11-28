import cv2

cap = cv2.VideoCapture(0)

while cv2.waitKey(1) != ord("q"):
    # read the frame
    ret, frame = cap.read()

    # get the eyes start and end points on frame
    frame_h, frame_w, _ = frame.shape

    # calculate the region of interest limits (right eye)
    roi_h_start = int(frame_h / 3)
    roi_h_end = int((frame_h / 3) * 2)
    roi_w_start = int(frame_w / 3)
    roi_w_end = int(frame_w / 2)

    # create the region of interest (roi)
    roi = frame[roi_h_start:roi_h_end, roi_w_start:roi_w_end]

    # get the roi sizes
    roi_h, roi_w, _ = roi.shape

    # create grayscale blured roi
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    gray_roi = cv2.GaussianBlur(gray_roi, (7, 7), 0)

    # create black & white version (threshold)
    _, threshold = cv2.threshold(gray_roi, 25, 255, cv2.THRESH_BINARY_INV)

    # finds the edges
    edge_points, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # gets the biggest area
    edge_points = sorted(edge_points, key=lambda x: cv2.contourArea(x), reverse=True)

    for point in edge_points:
        (x, y, w, h) = cv2.boundingRect(point)
        # draws the rectangle of the iris
        cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 0, 255), 2)
        # draws the vertical line
        cv2.line(roi, (x + int(w / 2), 0), (x + int(w / 2), roi_h), (0, 255, 0), 2)
        # draws the horizontal line
        cv2.line(roi, (0, y + int(h / 2)), (roi_w, y + int(h / 2)), (0, 255, 0), 2)

    # show the images
    cv2.imshow("roi", roi)

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
