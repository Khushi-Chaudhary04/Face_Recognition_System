import face_recognition
import cv2
import os
import sys

def recognition_with_auto_entries(dataset):
    def add_entries_from_directory(dataset):
        known_face_images = {}

        for root, dirs, files in os.walk(dataset):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')):
                    name = os.path.splitext(file)[0]
                    image_path = os.path.join(root, file)
                    known_face_images[name] = image_path

        return known_face_images

    known_face_images = add_entries_from_directory(dataset)

    # Initialize known_face_encodings as an empty dictionary
    known_face_encodings = {}

    for name, image_path in known_face_images.items():
        image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image)

        if face_encodings:
            # Store the list of face encodings
            known_face_encodings[name] = face_encodings
        else:
            print(f"No face detected in '{image_path}'")

    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        for face_encoding in face_encodings:
            match_name = "Unknown"

            for name, known_encodings in known_face_encodings.items():
                for known_encoding in known_encodings:
                    match = face_recognition.compare_faces([known_encoding], face_encoding, tolerance=0.6)
                    if match[0]:
                        match_name = name
                        break
                if match_name != "Unknown":
                    break

            for (top, right, bottom, left) in face_locations:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, match_name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    image_directory = "dataset"
    recognition_with_auto_entries(image_directory)
