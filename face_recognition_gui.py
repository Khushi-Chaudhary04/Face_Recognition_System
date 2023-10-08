# face_recognition_gui.py
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import main  # Import the main.py script

class FaceRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition App")

        # Create a label for the title
        title_label = tk.Label(root, text="Face Recognition System", font=("Helvetica", 16))
        title_label.pack(pady=20)

        # Create buttons for the two main options
        capture_button = tk.Button(root, text="Capture Image", command=self.capture_image)
        upload_button = tk.Button(root, text="Upload Image", command=self.upload_image)
        recognize_button = tk.Button(root, text="Recognize Face", command=self.recognize_face)

        capture_button.pack()
        upload_button.pack()
        recognize_button.pack()

    def capture_image(self):
        # Call the capture_image function from main.py
        main.capture_image()

    def upload_image(self):
        # Call the upload_image function from main.py
        main.upload_image()

    def recognize_face(self):
        # Call the recognize_face function from main.py
        main.recognize_face()

if __name__ == "__main__":
    root = tk.Tk()
    app = FaceRecognitionApp(root)
    root.mainloop()
