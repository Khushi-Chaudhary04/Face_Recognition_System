import tkinter as tk
from tkinter import Entry, PhotoImage, Label, Button, Toplevel, filedialog
import functions
import cv2
import camera
def capture_image_with_name():
    # Create a new window to get the user's name
    name_window = Toplevel(root)
    name_window.title("Enter Your Name")
    name_window.geometry("200x100+500+100")
    name_window.resizable(width=False, height=False)
    name_label = tk.Label(name_window, text="Please enter your name:")
    name_label.pack()
    
    name_entry = Entry(name_window)
    name_entry.pack()

    def capture_image():
        user_name = name_entry.get()
        if user_name:
            name_window.destroy()  # Close the name input window
            image_path = functions.capture_image(user_name)
            print("Image captured and saved as:", image_path)
        else:
            print("Please enter your name.")

    capture_button = Button(name_window, text="Capture Image", command=capture_image)
    capture_button.pack()

def upload_image():
    # Call the upload_image function from functions.py
    image_path = filedialog.askopenfilename()
    functions.upload_image()
    if image_path:
        print(f"Image '{image_path}' uploaded successfully.")
    else:
        print("Image upload failed.")

def recognize_face():
    # Call the recognize_face function from functions.py
    image_path = "dataset"  # Set the initial image path to an empty string
    functions.recognize_face(image_path)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Face Recognition App")

    # Load the background image
    background_image = PhotoImage(file='back.png')  # Replace with your image file path
    label = Label(root, image=background_image)
    label.place(relwidth=1, relheight=1)

    # Adding buttons to the window
    capture_button = Button(root, text="Capture Image", command=capture_image_with_name, bg="white", font=10)
    upload_button = Button(root, text="Upload Image", command=upload_image, bg="white", font=10)
    recognize_button = Button(root, text="Recognize Face", command=recognize_face, bg="white", font=10)

    capture_button.place(x=400, y=475)
    upload_button.place(x=600, y=475)
    recognize_button.place(x=800, y=475)

    root.geometry("1000x570+500+100")
    root.resizable(width=False, height=False)
    root.mainloop()
