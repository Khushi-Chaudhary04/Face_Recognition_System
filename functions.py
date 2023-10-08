# functions.py
import pymysql
import cv2
import os
import dlib

def authenticate_user(db_password):
    # Change these credentials to match your MySQL server setup
    db_host = "localhost"
    db_user = "Khushi"
    db_name = "Face_RecognitionDB"

    try:
        # Connect to the MySQL database
        connection = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)

        # Check if the connection was successful
        if connection:
            return True

    except pymysql.MySQLError as e:
        print("Error:", e)
        return False

    finally:
        # Close the database connection if it was established
        if connection:
            connection.close()

def capture_image():
    # Use OpenCV to capture an image from the webcam
    camera = cv2.VideoCapture(0)  # 0 represents the default camera (usually the built-in webcam)

    # Capture a single frame
    ret, frame = camera.read()

    # Save the captured frame as an image file (you can modify the filename as needed)
    image_path = "captured_image.jpg"
    cv2.imwrite(image_path, frame)

    # Release the camera
    camera.release()

    return image_path

def upload_image():
    # Get the filename of the image to upload
    image_filename = input("Enter the filename of the image to upload (e.g., my_image.jpg): ")

    # Check if the file exists in the project folder
    if os.path.exists(image_filename):
        return image_filename
    else:
        print(f"The file '{image_filename}' does not exist in the project folder.")
        return None

def save_to_database(name, dob, image_path):
    # Change these credentials to match your MySQL server setup
    db_host = "your_db_host"
    db_user = "your_db_user"
    db_password = "your_db_password"
    db_name = "your_db_name"

    try:
        # Connect to the MySQL database
        connection = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)

        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        # Insert the details into the database
        sql = "INSERT INTO FaceDetails (name, dob, image_path) VALUES (%s, %s, %s)"
        cursor.execute(sql, (name, dob, image_path))

        # Commit the changes to the database
        connection.commit()
        print("Details saved to the database.")

    except pymysql.MySQLError as e:
        print("Error:", e)

    finally:
        # Close the database connection
        cursor.close()
        connection.close()

def recognize_face(image_path):
    # Load a pre-trained face recognition model (e.g., dlib's face_recognition model)
    detector = dlib.get_frontal_face_detector()
    face_recognizer = dlib.face_recognition_model_v1("shape_predictor_68_face_landmarks.dat")

    # Load the image and convert it to grayscale
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale image
    faces = detector(gray)

    if len(faces) == 0:
        print("No faces found in the image.")
        return

    # Load the database connection and cursor
    # You may need to modify these database credentials
    db_host = "your_db_host"
    db_user = "your_db_user"
    db_password = "your_db_password"
    db_name = "your_db_name"

    try:
        connection = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
        cursor = connection.cursor()

        for face in faces:
            # Get facial landmarks for the detected face
            landmarks = face_recognizer(image, face)

            # Retrieve the stored face embeddings from the database
            cursor.execute("SELECT id, name, dob, image_path FROM FaceDetails")
            results = cursor.fetchall()

            for row in results:
                stored_image_path = row[3]

                # Load the stored image
                stored_image = cv2.imread(stored_image_path)

                # Detect faces in the stored image
                stored_faces = detector(stored_image)

                for stored_face in stored_faces:
                    stored_landmarks = face_recognizer(stored_image, stored_face)

                    # Calculate the face distance to check for a match
                    face_distance = dlib.face_distance([landmarks], [stored_landmarks])

                    # A lower face distance means a closer match
                    if face_distance < 0.6:
                        print("Match found!")
                        print("Name:", row[1])
                        print("DOB:", row[2])

        # Close the database connection
        cursor.close()
        connection.close()

    except pymysql.MySQLError as e:
        print("Error:", e)

if __name__ == "__main__":
    db_password = input("Enter the MySQL database password: ")
    if authenticate_user(db_password):
        print("Authentication successful.")

        # Offer options to the user
        print("Choose an option:")
        print("1. Capture an image using the webcam")
        print("2. Upload an image from your device")
        user_choice = input("Enter your choice (1 or 2): ")

        if user_choice == "1":
            # Capture an image using the webcam
            image_path = capture_image()
            print("Image captured and saved as:", image_path)

            # Prompt the user for details
            name = input("Enter the person's name: ")
            dob = input("Enter the person's date of birth (YYYY-MM-DD): ")

            # Save details to the database
            save_to_database(name, dob, image_path)

            # Recognize faces in the captured image
            recognize_face(image_path)
        elif user_choice == "2":
            # Upload an image from the project folder
            image_path = upload_image()
            if image_path:
                print(f"Image '{image_path}' uploaded successfully.")

                # Prompt the user for details
                name = input("Enter the person's name: ")
                dob = input("Enter the person's date of birth (YYYY-MM-DD): ")

                # Save details to the database
                save_to_database(name, dob, image_path)

                # Recognize faces in the uploaded image
                recognize_face(image_path)
            else:
                print("Image upload failed.")
        else:
            print("Invalid choice. Exiting.")
    else:
        print("Authentication failed. Access denied.")
