import shutil
from tkinter import filedialog
import pymysql
import cv2
import os
import numpy as np
import main
import face_recognition
import camera

def authenticate_user(db_password):
    # Change these credentials to match your MySQL server setup
    db_host = "localhost"
    db_user = "chirag"
    db_name = "Face_Recognition_Db"

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

def capture_image(name):
    # Use OpenCV to capture an image from the webcam
    camera = cv2.VideoCapture(0)  # 0 represents the default camera (usually the built-in webcam)

    # Capture a single frame
    ret, frame = camera.read()

    # Save the captured frame as an image file (you can modify the filename as needed)
    
    
    image_path = "dataset/"+name+".jpg"
    cv2.imwrite(image_path, frame)

    # Release the camera
    camera.release()

    return image_path

def upload_image():
    # Use a file dialog box to select an image to upload
    image_path = filedialog.askopenfilename()
    
    # Check if the file was selected
    if image_path:
        # Save the uploaded image to the dataset folder
        filename = os.path.basename(image_path)
        new_image_path = os.path.join("dataset", filename)
        shutil.copyfile(image_path, new_image_path)

        print(f"Image '{filename}' uploaded successfully.")

        # Recognize faces in the uploaded image
        # recognize_face(new_image_path)
        # return new_image_path
    else:
        print("Image upload canceled.")
        return None
    
    
        

def save_to_database(name, dob, image_path):
    # Change these credentials to match your MySQL server setup
    db_host = "localhost"
    db_user = "chirag"
    db_password = "root"
    db_name = "Face_Recognition_Db"

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
    
    # face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # # Load the image
    # image = cv2.imread(image_path)

    # # Convert the image to grayscale
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # # Detect faces in the grayscale image
    # faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # if len(faces) == 0:
    #     print("Match not found")
    #     return

    # # Load the database connection and cursor (you may need to modify these database credentials)
    # db_host = "localhost"
    # db_user = "chirag"
    # db_password = "root"
    # db_name = "Face_Recognition_Db"

    # try:
    #     connection = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
    #     cursor = connection.cursor()

    #     match_found = False  # Flag to indicate if a match has been found

    #     for (x, y, w, h) in faces:
    #         if match_found:
    #             break  # Break the loop if a match has already been found

    #         # Crop the face from the image
    #         face_img = gray[y:y + h, x:x + w]

    #         # Retrieve the stored face embeddings from the database
    #         cursor.execute("SELECT id, name, dob, image_path FROM FaceDetails")
    #         results = cursor.fetchall()

    #         for row in results:
    #             if match_found:
    #                 break  # Break the loop if a match has already been found

    #             stored_image_path = row[3]

    #             # Load the stored image
    #             stored_image = cv2.imread(stored_image_path)
    #             stored_gray = cv2.cvtColor(stored_image, cv2.COLOR_BGR2GRAY)

    #             # Detect faces in the stored image
    #             stored_faces = face_cascade.detectMultiScale(stored_gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    #             for (sx, sy, sw, sh) in stored_faces:
    #                 if match_found:
    #                     break  # Break the loop if a match has already been found

    #                 # Crop the face from the stored image
    #                 stored_face_img = stored_gray[sy:sy + sh, sx:sx + sw]

    #                 # Calculate the face distance to check for a match
    #                 face_distance = calculate_face_distance(face_img, stored_face_img)

    #                 # A lower face_distance means a closer match
    #                 if face_distance < 0.6:  # You can adjust the threshold as needed
    #                     print("Match found!")
    #                     print("Name:", row[1])
    #                     print("DOB:", row[2])
                        
    #                     match_found = True  # Set the flag to indicate a match has been found

    #     if not match_found:
    #         print("No perfect match found.")

    #     # Close the database connection
    #     cursor.close()
    #     connection.close()

    # except pymysql.MySQLError as e:
    #     print("Error:", e)
    camera.recognition_with_auto_entries(image_path)
def calculate_face_distance(face1_hog, face2_hog):
    """Calculate the distance between two faces based on the HOG features"""

    # Make sure both arrays have the same shape before subtracting them
    if face1_hog.shape != face2_hog.shape:
        if face1_hog.shape[0] > face2_hog.shape[0]:
            face2_hog = np.resize(face2_hog, face1_hog.shape)
        else:
            face1_hog = np.resize(face1_hog, face2_hog.shape)

    # Calculate the distance between the two faces
    distance = np.linalg.norm(face1_hog - face2_hog)

    return distance

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
