# Vehicle Control with Eye Detection

This project is for the people who has spinal cord paralysis. These peope use wheelchairs and cannot control the chair without any help. The aim is to able the person control the chair with eye movements.

## How It Works?

To detect eye movement, OpenCV and Dlib libraries were used.
- Dlib was used to detect the eye on the face.
- OpenCV was used to detect the pupil position.

Also, a small prototype of the wheelchair was build in order to test the movements. It has an ESP32 microcontroller with WiFi module. With the a computer, the prototype can be connected to its access point (AP) and controlled via eye movements (looking to top, bottom, left and right).

## How To Run?

"shape_predictor_68_face_landmarks.dat" file must be downloaded and copied to the same directory with eye detection codes. The link: https://www.kaggle.com/datasets/sergiovirahonda/shape-predictor-68-face-landmarksdat

The final code of the eye detection is "eye_detection_with_sender.py". But it will not work if you cannot connect to a host. If you only want to test eye detection, run "eye_detection_v4.py" instead. Make sure you have the required libraries, you can install them with "requirements.txt".

The prototype's code is in the "receiver" folder. Run "eye_detection_with_sender.py" after running and connecting to the prototype (if you have one). It was developed for ESP32 but may be work on other microdevices too.

If you have a prototype, follow these steps:
- Set your prototype (if you have one).
- Copy the prototype code with Ardunio IDE.
- Start the prototype with the code.
- Connect to the prototype's AP with WiFi.

After setting the prototype or else, run the proper eye detection code on a computer.
