import cv2
import face_recognition
import numpy as np
import os, math
from ugot import ugot

got = ugot.UGOT()
got.initialize('192.168.1.217')
got.open_camera()

def face_confidence(face_distance, face_match_threshold=0.6):
    range = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (range * 2.0)

    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + '%'
    else:
        value = (linear_val + ((1.0 - linear_val)
                * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + '%'

class FaceRecognition:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.process_current_frame = True
        self.encode_faces()

    def encode_faces(self):
        # Load and encode each image under `faces/`, store name without extension
        for image in os.listdir('faces'):
            if image.lower().endswith(('.jpg', '.png')):
                # strip off extension so we get 'elon' not 'elon.jpg'
                name = os.path.splitext(image)[0]
                path = os.path.join('faces', image)
                img = face_recognition.load_image_file(path)
                enc = face_recognition.face_encodings(img)
                if enc:
                    self.known_face_encodings.append(enc[0])
                    self.known_face_names.append(name)
        print("Loaded faces for:", self.known_face_names)

    def run_recognition(self):
        while True:
            frame_data = got.read_camera_data()
            if not frame_data:
                break

            # decode and mirror
            nparr = np.frombuffer(frame_data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            frame = cv2.flip(frame, 1)

            if self.process_current_frame:
                small = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                rgb_small = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

                locations = face_recognition.face_locations(rgb_small)
                encodings = face_recognition.face_encodings(rgb_small, locations)

                face_labels = []
                for face_encoding in encodings:
                    # find best match
                    distances = face_recognition.face_distance(
                        self.known_face_encodings, face_encoding)
                    best_idx = np.argmin(distances)
                    match = distances[best_idx] <= 0.6

                    if match:
                        name = self.known_face_names[best_idx]
                    else:
                        name = 'Unknown'

                    confidence = face_confidence(distances[best_idx])

                    # parse out numeric confidence
                    try:
                        conf_val = float(confidence.strip('%'))
                    except ValueError:
                        conf_val = 0.0

                    if name == 'elon' and conf_val > 80.0:
                        got.mecanum_move_speed(0, 25)
                    elif name == 'jensen' and conf_val > 80.0:
                        got.mecanum_move_speed(1, 25)

                    face_labels.append(f'{name} ({confidence})')

                self.face_locations = locations
                self.face_names = face_labels

                if not self.face_names or all(label.startswith('Unknown') for label in self.face_names):
                    got.mecanum_stop()

            self.process_current_frame = not self.process_current_frame

            # draw boxes & labels
            for (top, right, bottom, left), label in zip(
                    self.face_locations, self.face_names):
                top, right, bottom, left = [v * 4 for v in (top, right, bottom, left)]
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35),
                              (right, bottom), (0, 0, 255), cv2.FILLED)
                cv2.putText(frame, label, (left + 6, bottom - 6),
                            cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

            cv2.imshow('Face Recognition', frame)
            if cv2.waitKey(1) == ord('q'):
                break

        cv2.destroyAllWindows()

if __name__ == '__main__':
    FaceRecognition().run_recognition()
