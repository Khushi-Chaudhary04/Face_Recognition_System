# main.py
import functions

def main():
    print("Welcome to the Face Recognition System!")

    while True:
        print("\nChoose an option:")
        print("1. Add new data")
        print("2. Recognize face")
        print("3. Quit")
        choice = input("Enter your choice (1, 2, or 3): ")

        if choice == "1":
            # Authenticate the user with the MySQL database password
            db_password = input("Enter the MySQL database password: ")
            if functions.authenticate_user(db_password):
                print("Authentication successful.")

                # Offer options for adding new data
                print("Choose an option:")
                print("1. Capture an image using the webcam")
                print("2. Upload an image from your device")
                user_choice = input("Enter your choice (1 or 2): ")

                if user_choice == "1":
                    # Capture an image using the webcam
                    image_path = functions.capture_image()
                    print("Image captured and saved as:", image_path)

                    # Prompt the user for details
                    name = input("Enter the person's name: ")
                    dob = input("Enter the person's date of birth (YYYY-MM-DD): ")

                    # Save details to the database
                    functions.save_to_database(name, dob, image_path)
                elif user_choice == "2":
                    # Upload an image from the project folder
                    image_path = functions.upload_image()
                    if image_path:
                        print(f"Image '{image_path}' uploaded successfully.")

                        # Prompt the user for details
                        name = input("Enter the person's name: ")
                        dob = input("Enter the person's date of birth (YYYY-MM-DD): ")

                        # Save details to the database
                        functions.save_to_database(name, dob, image_path)
                    else:
                        print("Image upload failed.")
                else:
                    print("Invalid choice. Exiting.")
            else:
                print("Authentication failed. Access denied.")

        elif choice == "2":
            # Authenticate the user with the MySQL database password
            db_password = input("Enter the MySQL database password: ")
            if functions.authenticate_user(db_password):
                print("Authentication successful.")

                # Offer options for face recognition
                print("Choose an option:")
                print("1. Capture an image using the webcam for recognition")
                print("2. Recognize faces in a pre-existing image")
                user_choice = input("Enter your choice (1 or 2): ")

                if user_choice == "1":
                    # Capture an image using the webcam for recognition
                    image_path = functions.capture_image()
                    print("Image captured and saved as:", image_path)

                    # Recognize faces in the captured image
                    functions.recognize_face(image_path)
                elif user_choice == "2":
                    # Recognize faces in a pre-existing image
                    image_path = input("Enter the filename of the image for recognition: ")
                    functions.recognize_face(image_path)
                else:
                    print("Invalid choice. Exiting.")
            else:
                print("Authentication failed. Access denied.")

        elif choice == "3":
            print("Thank you for using the Face Recognition System. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a valid option (1, 2, or 3).")

if __name__ == "__main__":
    main()
