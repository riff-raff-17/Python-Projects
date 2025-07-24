'''Contains both face mesh and face detection. Swap out the results 
and initialize the correct model based on usage'''

import cv2
import mediapipe as mp

# Initialize MediaPipe Face Detection
mp_draw = mp.solutions.drawing_utils

# Start video capture
cap = cv2.VideoCapture(0)

# Initialize Face Detection model
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)

# Initialize Face Mesh model
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False,
                                  max_num_faces=2,
                                  refine_landmarks=True,  # Track eye irises
                                  min_detection_confidence=0.5,
                                  min_tracking_confidence=0.5)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Flip the frame horizontally for a mirror effect
    frame = cv2.flip(frame, 1)
    
    # Convert frame to RGB (MediaPipe uses RGB)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the frame
    results = face_detection.process(rgb_frame)

    if results.detections:
        for detection in results.detections:
            # Draw bounding box
            bboxC = detection.location_data.relative_bounding_box
            h, w, c = frame.shape
            x, y, w_box, h_box = int(bboxC.xmin * w), int(bboxC.ymin * h), int(bboxC.width * w), int(bboxC.height * h)
            cv2.rectangle(frame, (x, y), (x + w_box, y + h_box), (0, 255, 0), 2)
            
            # Draw confidence score
            confidence = int(detection.score[0] * 100)
            cv2.putText(frame, f'{confidence}%', (x, y - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Draw all landmarks
            mp_draw.draw_landmarks(frame,
                                   face_landmarks,
                                   mp_face_mesh.FACEMESH_TESSELATION,
                                   landmark_drawing_spec=mp_draw.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1),
                                   connection_drawing_spec=mp_draw.DrawingSpec(color=(0, 255, 255), thickness=1))
            
            # Highlight specific points (e.g., eyes, nose, mouth)
            for id, lm in enumerate(face_landmarks.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                # Example: Highlight nose tip (landmark 1)
                if id == 1:
                    cv2.circle(frame, (cx, cy), 3, (0, 0, 255), -1)  # Red circle

                # Example: Highlight left eye iris (landmark 473)
                if id == 473:
                    cv2.circle(frame, (cx, cy), 3, (255, 0, 0), -1)  # Blue circle'''

    # Display frame
    cv2.imshow("Face Tracking", frame)
    
    # Break loop with 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
