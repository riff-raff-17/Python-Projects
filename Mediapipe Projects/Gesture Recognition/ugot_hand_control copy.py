import cv2
import mediapipe as mp
from ugot import ugot
import numpy as np

# Connect to UGOT and open camera
got = ugot.UGOT()
ip_add = input("What is the UGOT IP address? >")
got.initialize(ip_add)
got.open_camera()

# Initialize Mediapipe Hands
mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False, model_complexity=1,
                      min_detection_confidence=0.75,
                      min_tracking_confidence=0.75, max_num_hands=2)

Draw = mp.solutions.drawing_utils

def calculate_angle(tip, base):
    """ Calculate angle between index finger tip and base """
    dx = tip[1] - base[1]  # Horizontal difference
    dy = tip[2] - base[2]  # Vertical difference
    angle = np.arctan2(dy, dx) * (180 / np.pi)  # Convert radians to degrees
    return angle

def calculate_distance(point1, point2):
    """ Calculate Euclidean distance between two points """
    return np.sqrt((point1[1] - point2[1])**2 + (point1[2] - point2[2])**2)

while True:
    frame = got.read_camera_data()

    if not frame:  # If no camera data, break the loop
        break

    nparr = np.frombuffer(frame, np.uint8)
    data = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    frame = cv2.flip(data, 1)  # Flip image
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
    Process = hands.process(frameRGB)

    landmarkList = []
    direction = ""

    if Process.multi_hand_landmarks:
        for handlm in Process.multi_hand_landmarks:
            for _id, landmarks in enumerate(handlm.landmark):
                height, width, _ = frame.shape
                x, y = int(landmarks.x * width), int(landmarks.y * height)
                landmarkList.append([_id, x, y])

            Draw.draw_landmarks(frame, handlm, mpHands.HAND_CONNECTIONS)

        # Detect index finger position
        if landmarkList:
            index_tip = landmarkList[8]  # Index finger tip
            index_base = landmarkList[5]  # Index finger base
            hand_center = landmarkList[0] # Palm center (wrist landmark)

            angle = calculate_angle(index_tip, index_base)
            distance = calculate_distance(index_tip, hand_center)

            # Define minimum threshold distance
            min_distance_threshold = 50  # Adjust based on camera setup

            if distance > min_distance_threshold:  # Only detect if above threshold
                if -30 <= angle <= 30:  # Right
                    direction = "Right"
                elif 60 <= angle <= 120:  # Up
                    direction = "Up"
                elif 150 <= angle or angle <= -150:  # Left
                    direction = "Left"
                elif -120 <= angle <= -60:  # Down
                    direction = "Down"

                print(direction)  # Print direction to console

    # Display detected direction on screen
    cv2.putText(frame, direction, (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 255, 0), 2, cv2.LINE_AA)

    # Show video frame and exit on 'q'
    cv2.imshow('Image', frame)
    if cv2.waitKey(1) & 0xff == ord('q'):
        cv2.destroyAllWindows()
        break
