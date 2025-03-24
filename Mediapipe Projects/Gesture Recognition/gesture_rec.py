import cv2
import mediapipe as mp
import math

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# Start webcam
cap = cv2.VideoCapture(0)

# Initialize Hands model
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=2,
                       min_detection_confidence=0.5,
                       min_tracking_confidence=0.5)

# Gesture detection function
def detect_gesture(landmarks):
    # Get landmarks of thumb and index finger
    thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_tip = landmarks[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = landmarks[mp_hands.HandLandmark.PINKY_TIP]

    # Measure distances between thumb and other fingers
    thumb_index_dist = math.hypot(index_tip.x - thumb_tip.x, index_tip.y - thumb_tip.y)
    thumb_middle_dist = math.hypot(middle_tip.x - thumb_tip.x, middle_tip.y - thumb_tip.y)
    thumb_ring_dist = math.hypot(ring_tip.x - thumb_tip.x, ring_tip.y - thumb_tip.y)
    thumb_pinky_dist = math.hypot(pinky_tip.x - thumb_tip.x, pinky_tip.y - thumb_tip.y)

    # Thumb Up Gesture: If thumb is far from all other fingers
    if thumb_index_dist > 0.15 and thumb_middle_dist > 0.15 and thumb_ring_dist > 0.15 and thumb_pinky_dist > 0.15:
        return "Thumbs Up"

    # Victory Sign Gesture: If index and middle fingers are far apart, and other fingers are close
    if thumb_index_dist > 0.15 and thumb_middle_dist > 0.15 and thumb_ring_dist < 0.1 and thumb_pinky_dist < 0.1:
        return "Victory Sign"

    return None

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.flip(frame, 1)  # Mirror effect
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the frame with MediaPipe Hands
    results = hands.process(rgb_frame)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw hand landmarks
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Detect gesture
            gesture = detect_gesture(hand_landmarks.landmark)
            if gesture:
                # Display gesture text on screen
                cv2.putText(frame, gesture, (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Show the frame
    cv2.imshow("Gesture Recognition", frame)

    # Break loop with 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
