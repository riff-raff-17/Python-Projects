# Importing Libraries 
import cv2 
import mediapipe as mp 
from ugot import ugot
import numpy as np 

# Connect to UGOT and open camera
got = ugot.UGOT()
ip_add = input("What is the UGOT IP address? >")
got.initialize(ip_add)
got.open_camera()

# Initializing the Model 
mpHands = mp.solutions.hands
hands = mpHands.Hands( 
    static_image_mode=False, 
    model_complexity=1, 
    min_detection_confidence=0.75, 
    min_tracking_confidence=0.75, 
    max_num_hands=2) 

Draw = mp.solutions.drawing_utils 

while True: 
    # Read video frame by frame 
    frame = got.read_camera_data()

    # If no camera, breaks the program
    if not frame:
        break

    # Turns it into a numpy array
    nparr = np.frombuffer(frame, np.uint8)
    data = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
  
    # Flip image 
    frame = cv2.flip(data, 1)
  
    # Convert BGR image to RGB image 
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
  
    # Process the RGB image 
    Process = hands.process(frameRGB) 

    landmarkList = [] 
    # if hands are present in image(frame) 
    if Process.multi_hand_landmarks: 
        # detect handmarks 
        for handlm in Process.multi_hand_landmarks: 
            for _id, landmarks in enumerate(handlm.landmark): 
                # store height and width of image 
                height, width, color_channels = frame.shape 
  
                # calculate and append x, y coordinates 
                # of handmarks from image(frame) to lmList 
                x, y = int(landmarks.x*width), int(landmarks.y*height) 
                landmarkList.append([_id, x, y]) 
  
            # draw Landmarks 
            Draw.draw_landmarks(frame, handlm, 
                                mpHands.HAND_CONNECTIONS) 
            
    # Display Video and when 'q' is entered, destroy  
    # the window 
    cv2.imshow('Image', frame) 
    if cv2.waitKey(1) & 0xff == ord('q'): 
        cv2.destroyAllWindows() 
        break
